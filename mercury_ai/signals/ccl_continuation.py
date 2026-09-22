"""CCL Continuation — Continuacao, Consolidacao, Liquidez (SIGNAL-ONLY).

Estrategia validada (2026-09-20, reports/m5_ccl_continuation_probe.json):
  1. CONTINUACAO: 2 velas fortes na mesma direcao antes da caixa.
  2. CONSOLIDACAO: caixa de 3 velas com range <= 0.8 ATR.
  3. LIQUIDEZ: vela atual varre a caixa contra a tendencia e fecha de volta.
  4. ENTRADA: proxima vela na direcao da tendencia (sem lookahead).

Teste final: 87,0% com gale 1+2 (146 sinais); 47,3% sem gale.

Contrato: so velas fechadas; nunca altera decisao/score/ranking; nunca
executa ordens nem faz rede.
"""
from __future__ import annotations

from typing import Any, Dict

BOX_MAX_ATR = 0.8


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def detect_ccl(df_closed: Any) -> Dict[str, Any]:
    """Detecta o padrao CCL na ultima vela fechada."""
    out: Dict[str, Any] = {
        "detected": False, "direction": "NONE", "reason": "sem padrao",
        "box_high": None, "box_low": None,
    }
    try:
        if df_closed is None or len(df_closed) < 20:
            out["reason"] = "df insuficiente"
            return out
        window = df_closed.iloc[-20:]
        opens = [_f(v) for v in window["Open"].tolist()]
        closes = [_f(v) for v in window["Close"].tolist()]
        highs = [_f(v) for v in window["High"].tolist()]
        lows = [_f(v) for v in window["Low"].tolist()]
    except (KeyError, IndexError, TypeError, ValueError):
        out["reason"] = "df invalido"
        return out

    n = len(closes)
    # ATR simples sobre a janela
    trs = []
    for j in range(1, n):
        trs.append(max(highs[j] - lows[j], abs(highs[j] - closes[j - 1]), abs(lows[j] - closes[j - 1])))
    atr = sum(trs[-14:]) / 14.0 if len(trs) >= 14 else 0.0
    if atr <= 0:
        out["reason"] = "ATR nulo"
        return out

    i = n - 1
    # 1) Continuacao: velas i-5..i-3 na mesma direcao
    bull_cont = all(closes[j] > opens[j] for j in range(i - 5, i - 3)) and closes[i - 3] > closes[i - 5]
    bear_cont = all(closes[j] < opens[j] for j in range(i - 5, i - 3)) and closes[i - 3] < closes[i - 5]
    if not (bull_cont or bear_cont):
        out["reason"] = "sem continuacao"
        return out
    # 2) Consolidacao: caixa i-3..i-1 com range estreito
    box_high = max(highs[i - 3:i])
    box_low = min(lows[i - 3:i])
    box_range = box_high - box_low
    if box_range <= 0 or box_range > BOX_MAX_ATR * atr:
        out["reason"] = "caixa larga demais"
        return out
    # 3) Liquidez: vela atual varre a caixa contra a tendencia e fecha de volta
    sweep_low = lows[i] < box_low and closes[i] > box_low
    sweep_high = highs[i] > box_high and closes[i] < box_high
    if bull_cont and sweep_low:
        out.update(detected=True, direction="BUY", box_high=round(box_high, 5),
                   box_low=round(box_low, 5),
                   reason=f"CCL: continuacao compradora + sweep da caixa {box_low:.5f}")
        return out
    if bear_cont and sweep_high:
        out.update(detected=True, direction="SELL", box_high=round(box_high, 5),
                   box_low=round(box_low, 5),
                   reason=f"CCL: continuacao vendedora + sweep da caixa {box_high:.5f}")
        return out
    out["reason"] = "sem sweep da caixa"
    return out
