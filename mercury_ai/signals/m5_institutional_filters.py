"""Filtros institucionais M5 — observáveis puros (SIGNAL-ONLY, sem decisão).

Problema auditado (55 ciclos PASS, 127 TOP3, velas Yahoo reais):
  G0 direcional puro = 49.6% (moeda). Nenhum filtro isolado testado elevou
  G0 a 85%: EMA200 a favor 50.5% vs contra 47.2%; ATR<=2.0 50.6%;
  trigger body>=0.40 54.4%; trigger alinhada 40.3% (PIOR que desalinhada
  60.0%); displacement 25.0%; CONFIRMED 41.3% vs EXPIRED 58.8-63.2%.

Por isso este módulo NÃO bloqueia nada: calcula observáveis sobre df_closed
(velas fechadas, nunca a em formação) para o Signal propagar e o dashboard
exibir/auditar. Gates bloqueantes exigiriam validação forward em 100+
ciclos — ver scripts/top3_m5_audit.py.

Parâmetros exatos (escala M5, medidos na amostra):
  TRIGGER_BODY_MIN = 0.25  (corpo/range da trigger N; p25 WIN 0.439 vs LOSS 0.300)
  ATR_CAP = 2.0            (range_N / ATR14; p75 WIN 1.495 vs LOSS 1.082)
  EMA_SPAN = 200           (tendência principal; alinhamento close_N vs EMA200)
  ATR_SPAN = 14            (TR médio clássico, só fechadas)
  IDM_LOOKBACK = 5         (janela curta p/ inducement; sweep estrutural usa 20)
  ZONE_LOOKBACK = 48       (perna local ~4h p/ fib 50% premium/discount)

Medição 2026-09-14 (128 TOP3, G0 base 49.2% — sem lookahead, só fechadas):
  FVG a favor ............. 55.3% (cob 59%) | FVG+IDM ....... 59.3% (cob 42%)
  FVG+IDM+zona ............ 83.3% (5/6, cob 4.7%, p~0.097 n.s., halves 3/3+2/3)
  => NENHUM vira bloqueio: FVG+IDM+zona é LINHA DE ESTUDO (n=6, 1 dia).
  Bloqueios propostos e REFUTADOS: MTF>=75 (cob 0% — max real 50),
  trigger-alinhada (manter = 40.3% vs bloquear = 60.7%), zona (40.7% vs
  51.5% contra), sweep-ok (44.9%), EMA200 (50.5% vs 47.2%).

Sem rede, sem broker, sem motores. Nunca altera decisão/score/ranking.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

TRIGGER_BODY_MIN = 0.25
ATR_CAP = 2.0
EMA_SPAN = 200
ATR_SPAN = 14
IDM_LOOKBACK = 5
ZONE_LOOKBACK = 48


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def trigger_body_ratio(df_closed: Any) -> Optional[float]:
    """Corpo/range da trigger N (última fechada). None se incalculável."""
    try:
        if df_closed is None or len(df_closed) < 1:
            return None
        row = df_closed.iloc[-1]
        o, h, lo, c = _f(row["Open"]), _f(row["High"]), _f(row["Low"]), _f(row["Close"])
        rng = h - lo
        if rng <= 0:
            return None
        return round(abs(c - o) / rng, 4)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def trigger_aligned(df_closed: Any, decision: str) -> Optional[bool]:
    """True se a trigger N fechou na direção da decisão; None se incalculável."""
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return None
    try:
        if df_closed is None or len(df_closed) < 1:
            return None
        row = df_closed.iloc[-1]
        o, c = _f(row["Open"]), _f(row["Close"])
        if c == o:
            return None  # doji: sem direção
        return (c > o) if dec == "BUY" else (c < o)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def atr14(df_closed: Any, span: int = ATR_SPAN) -> Optional[float]:
    """ATR clássico sobre fechadas. None se incalculável."""
    try:
        if df_closed is None or len(df_closed) < span + 1:
            return None
        h = df_closed["High"].astype(float)
        l = df_closed["Low"].astype(float)
        c = df_closed["Close"].astype(float)
        tr = (h - l).abs().combine(
            (h - c.shift()).abs(), max).combine(
            (l - c.shift()).abs(), max)
        val = float(tr.rolling(span).mean().iloc[-1])
        return val if val > 0 else None
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def trigger_range_atr(df_closed: Any) -> Optional[float]:
    """range_N / ATR14 (pré-entrada, só fechadas). None se incalculável."""
    try:
        atr = atr14(df_closed)
        if atr is None or atr <= 0:
            return None
        row = df_closed.iloc[-1]
        rng = _f(row["High"]) - _f(row["Low"])
        if rng <= 0:
            return None
        return round(rng / atr, 3)
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def ema200_side(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Lado do preço vs EMA200 (tendência principal).

    Retorna {"aligned": bool|None, "dist_atr": float|None}.
    aligned True = preço a favor da decisão (close_N > EMA200 p/ BUY).
    None quando df < 200 fechadas ou incalculável (nunca bloqueia).
    """
    out: Dict[str, Any] = {"aligned": None, "dist_atr": None}
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return out
    try:
        if df_closed is None or len(df_closed) < EMA_SPAN:
            return out
        cl = df_closed["Close"].astype(float)
        ema = float(cl.ewm(span=EMA_SPAN, adjust=False).mean().iloc[-1])
        px = float(cl.iloc[-1])
        out["aligned"] = (px > ema) if dec == "BUY" else (px < ema)
        atr = atr14(df_closed)
        if atr and atr > 0:
            out["dist_atr"] = round(abs(px - ema) / atr, 2)
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        return out


def institutional_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Pacote observável completo (tudo None-safe).

    Inclui as 4 métricas SMC pedidas (tarefa 2): has_liquidity_sweep,
    in_premium_discount_zone, has_fvg, has_inducement — todas sobre
    df_closed (só fechadas), alinhadas à decisão (BULLISH p/ BUY).
    Sweep usa lookback estrutural 20; inducement usa janela curta 5.
    Zona = fib 50% da perna local (48 fechadas ~4h M5).
    """
    ema = ema200_side(df_closed, decision)
    smc = smc_flags(df_closed, decision)
    return {
        "trigger_body_ratio": trigger_body_ratio(df_closed),
        "trigger_aligned": trigger_aligned(df_closed, decision),
        "trigger_range_atr": trigger_range_atr(df_closed),
        "ema200_aligned": ema.get("aligned"),
        "ema200_dist_atr": ema.get("dist_atr"),
        "has_liquidity_sweep": smc.get("has_liquidity_sweep"),
        "in_premium_discount_zone": smc.get("in_premium_discount_zone"),
        "has_fvg": smc.get("has_fvg"),
        "has_inducement": smc.get("has_inducement"),
    }


def smc_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """4 métricas SMC (observáveis, sem bloquear).

    Retorna Nones honestos quando df insuficiente. Reusa os detectores
    de institutional_confirmation (sem duplicar matemática) + fib 50%
    local. Custo O(n) por detector sobre ~60-500 fechadas: cabe no scan
    sem timeout (sem rede, sem TF extra).
    """
    out: Dict[str, Any] = {
        "has_liquidity_sweep": None,
        "in_premium_discount_zone": None,
        "has_fvg": None,
        "has_inducement": None,
    }
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return out
    want = "BULLISH" if dec == "BUY" else "BEARISH"
    try:
        from mercury_ai.analysis.institutional_confirmation import (
            atr14 as _atr14,
            detect_fvg as _fvg,
            detect_liquidity_sweep as _sweep,
        )
        if df_closed is None or len(df_closed) < 15:
            return out
        atr = _atr14(df_closed)
        if not atr or atr <= 0:
            return out
        sw = _sweep(df_closed, atr)
        out["has_liquidity_sweep"] = bool(sw.get("detected")) and sw.get("direction") == want
        fv = _fvg(df_closed, atr)
        out["has_fvg"] = bool(fv.get("detected")) and fv.get("direction") == want
        win = df_closed.iloc[-12:-1] if len(df_closed) >= 13 else df_closed
        idm = _sweep(win, atr, lookback=IDM_LOOKBACK)
        out["has_inducement"] = bool(idm.get("detected"))
        leg = df_closed.iloc[-ZONE_LOOKBACK:] if len(df_closed) >= ZONE_LOOKBACK else df_closed
        try:
            hi = float(leg["High"].max())
            lo = float(leg["Low"].min())
            px = float(df_closed["Close"].iloc[-1])
        except (KeyError, IndexError, TypeError, ValueError):
            return out
        if hi <= lo:
            return out
        fib50 = (hi + lo) / 2.0
        if px == fib50:
            out["in_premium_discount_zone"] = None  # equilibrium: sem lado
        elif dec == "BUY":
            out["in_premium_discount_zone"] = bool(px < fib50)
        else:
            out["in_premium_discount_zone"] = bool(px > fib50)
        return out
    except Exception:
        return out
