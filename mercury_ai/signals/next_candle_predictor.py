"""Preditor da PRÓXIMA vela M5 — SMC/ICT estrutural (puro, sem motores).

Problema: o Mercury analisa a vela atual (N fechada) e o operador entra na
PRÓXIMA vela (N+1). O `forward_bias` confirma se a direção SOBREVIVE, mas não
PREDIZ para onde o preço VAI a partir da estrutura de topos/fundos — que é o
que o trader institucional faz ao desenhar linhas de compradores/vendedores.

Este módulo replica essa leitura:
  1. Swings: últimos 2 topos (H) e 2 fundos (L) por pivot (janela 3).
  2. Estrutura: HH+HL -> UP | LH+LL -> DOWN | misto -> RANGE.
  3. Posição do preço vs último swing:
     - Rompeu último topo com corpo (BOS up) -> continuação UP.
     - Falhou no topo (pavio acima + close abaixo) -> reversão DOWN (liquidez).
     - Espelho para fundos.
  4. Sweep + reclaim (wick além do swing + close de volta) -> reversão.
  5. FVG aberto na direção do fluxo -> continuação.
  6. Momentum: 2+ das últimas 3 fechadas na mesma direção -> reforço.

Saída: direction BULLISH/BEARISH/NEUTRAL + confidence 0-100 + reasons +
structure + key_level. NEUTRAL quando estrutura é RANGE sem gatilho.

Contrato SIGNAL-ONLY: só velas FECHADAS; nunca altera decisão/score;
nunca inventa direção (NEUTRAL é resposta válida).
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

BULLISH = "BULLISH"
BEARISH = "BEARISH"
NEUTRAL = "NEUTRAL"


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def _cols(df: Any) -> Tuple[List[float], List[float], List[float], List[float]]:
    o = [_f(v) for v in df["Open"].tolist()]
    h = [_f(v) for v in df["High"].tolist()]
    lo = [_f(v) for v in df["Low"].tolist()]
    c = [_f(v) for v in df["Close"].tolist()]
    return o, h, lo, c


def _swings(h: List[float], lo: List[float], window: int = 3
            ) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
    """Pivots: topo se H[i] é máximo da janela; fundo se L[i] é mínimo."""
    tops, bots = [], []
    n = len(h)
    for i in range(window, n - window):
        seg_h = h[i - window:i + window + 1]
        seg_l = lo[i - window:i + window + 1]
        if h[i] >= max(seg_h) and (seg_h.count(h[i]) == 1 or seg_h.index(h[i]) == window):
            if not tops or i - tops[-1][0] >= window:
                tops.append((i, h[i]))
        if lo[i] <= min(seg_l) and (seg_l.count(lo[i]) == 1 or seg_l.index(lo[i]) == window):
            if not bots or i - bots[-1][0] >= window:
                bots.append((i, lo[i]))
    return tops[-4:], bots[-4:]


def _structure(tops: List[Tuple[int, float]],
               bots: List[Tuple[int, float]]) -> Tuple[str, str]:
    """Estrutura por últimos 2 topos + 2 fundos. Retorna (estrutura, detalhe)."""
    if len(tops) >= 2 and len(bots) >= 2:
        hh = tops[-1][1] > tops[-2][1]
        hl = bots[-1][1] > bots[-2][1]
        lh = tops[-1][1] < tops[-2][1]
        ll = bots[-1][1] < bots[-2][1]
        if hh and hl:
            return "UP", f"HH {tops[-2][1]:.2f}->{tops[-1][1]:.2f} + HL {bots[-2][1]:.2f}->{bots[-1][1]:.2f}"
        if lh and ll:
            return "DOWN", f"LH {tops[-2][1]:.2f}->{tops[-1][1]:.2f} + LL {bots[-2][1]:.2f}->{bots[-1][1]:.2f}"
        return "RANGE", "topos/fundos mistos (sem sequência)"
    return "RANGE", "swings insuficientes (<2 topos/fundos)"


def predict_next_candle(df_closed: Any) -> Dict[str, Any]:
    """Prediz a direção da PRÓXIMA vela M5 a partir da estrutura."""
    out: Dict[str, Any] = {
        "direction": NEUTRAL, "confidence": 0.0, "reasons": [],
        "structure": "RANGE", "structure_detail": "",
        "key_level": None, "key_kind": "NONE",
        "sweep": False, "fvg": False, "bos": False, "momentum": False,
    }
    try:
        if df_closed is None or len(df_closed) < 12:
            out["reasons"] = ["df insuficiente (<12 fechadas)"]
            return out
        df = df_closed.iloc[:-1] if len(df_closed) > 60 else df_closed
        o, h, lo, c = _cols(df)
        n = len(c)
    except (KeyError, IndexError, TypeError, ValueError):
        out["reasons"] = ["df inválido"]
        return out

    reasons: List[str] = []
    bull_votes, bear_votes = 0, 0

    tops, bots = _swings(h, lo)
    struct, detail = _structure(tops, bots)
    out["structure"] = struct
    out["structure_detail"] = detail
    reasons.append(f"estrutura {struct} ({detail})")
    if struct == "UP":
        bull_votes += 2
    elif struct == "DOWN":
        bear_votes += 2

    last_top = tops[-1][1] if tops else None
    last_bot = bots[-1][1] if bots else None
    oN, hN, lN, cN = o[-1], h[-1], lo[-1], c[-1]
    rng = hN - lN
    body = abs(cN - oN)
    if rng <= 0:
        out["reasons"] = ["range nulo na trigger"]
        return out

    # BOS / falha: preço vs último swing (lógica de topos/fundos do trader).
    if last_top is not None:
        if cN > last_top and body >= 0.3 * rng:
            out["bos"] = True
            out["key_level"] = last_top
            out["key_kind"] = "TOPO_ROMPIDO"
            bull_votes += 2
            reasons.append(f"BOS: close {cN:.2f} rompeu topo {last_top:.2f} com corpo")
        elif hN > last_top and cN < last_top:
            out["sweep"] = True
            out["key_level"] = last_top
            out["key_kind"] = "TOPO_VARREDURA"
            bear_votes += 2
            reasons.append(f"sweep de topo: pavio {hN:.2f} além de {last_top:.2f} + close {cN:.2f} de volta (vendedores)")
    if last_bot is not None:
        if cN < last_bot and body >= 0.3 * rng:
            out["bos"] = True
            out["key_level"] = last_bot
            out["key_kind"] = "FUNDO_ROMPIDO"
            bear_votes += 2
            reasons.append(f"BOS: close {cN:.2f} rompeu fundo {last_bot:.2f} com corpo")
        elif lN < last_bot and cN > last_bot:
            out["sweep"] = True
            out["key_level"] = last_bot
            out["key_kind"] = "FUNDO_VARREDURA"
            bull_votes += 2
            reasons.append(f"sweep de fundo: pavio {lN:.2f} além de {last_bot:.2f} + close {cN:.2f} de volta (compradores)")

    # FVG: gap entre N-2 e N (3 velas) — mitigado ou aberto?
    try:
        if n >= 4:
            h2, l2 = h[-3], lo[-3]
            h0, l0 = h[-1], lo[-1]
            gap_up = l0 - h2
            gap_dn = l2 - h0
            atr_proxy = sum(h[i] - lo[i] for i in range(n - 14, n)) / 14.0
            if atr_proxy > 0:
                if gap_up >= 0.2 * atr_proxy:
                    filled = any(lo[j] <= (l0 + h2) / 2 for j in range(n - 2, n))
                    if not filled:
                        out["fvg"] = True
                        bull_votes += 1
                        reasons.append(f"FVG altista aberto gap {gap_up:.2f} (desequilíbrio comprador)")
                elif gap_dn >= 0.2 * atr_proxy:
                    filled = any(h[j] >= (l2 + h0) / 2 for j in range(n - 2, n))
                    if not filled:
                        out["fvg"] = True
                        bear_votes += 1
                        reasons.append(f"FVG baixista aberto gap {gap_dn:.2f} (desequilíbrio vendedor)")
    except (IndexError, ValueError):
        pass

    # Momentum: 2+ das últimas 3 fechadas na mesma direção.
    try:
        ups = sum(1 for i in (-1, -2, -3) if c[i] > o[i])
        dns = sum(1 for i in (-1, -2, -3) if c[i] < o[i])
        if ups >= 2:
            out["momentum"] = True
            bull_votes += 1
            reasons.append(f"momentum comprador ({ups}/3 fechadas)")
        elif dns >= 2:
            out["momentum"] = True
            bear_votes += 1
            reasons.append(f"momentum vendedor ({dns}/3 fechadas)")
    except IndexError:
        pass

    total = bull_votes + bear_votes
    if total == 0 or bull_votes == bear_votes:
        out["direction"] = NEUTRAL
        out["confidence"] = 0.0
        reasons.append("sem edge direcional (RANGE sem gatilho) — sem aposta")
    elif bull_votes > bear_votes:
        out["direction"] = BULLISH
        out["confidence"] = round(50.0 + 50.0 * (bull_votes - bear_votes) / max(total, 1), 1)
    else:
        out["direction"] = BEARISH
        out["confidence"] = round(50.0 + 50.0 * (bear_votes - bull_votes) / max(total, 1), 1)
    out["reasons"] = reasons
    return out


def predictor_agrees(prediction: Dict[str, Any], decision: str) -> Optional[bool]:
    """True se preditor concorda com a decisão; False se discorda; None se NEUTRAL."""
    dec = str(decision or "").upper()
    want = { "BUY": BULLISH, "SELL": BEARISH }.get(dec)
    if want is None:
        return None
    d = str((prediction or {}).get("direction", NEUTRAL)).upper()
    if d == NEUTRAL:
        return None
    return d == want
