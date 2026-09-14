"""Trendlines LTA/LTB — diagonais SMC puras (SIGNAL-ONLY, sem motores).

Problema do operador: topos/fundos + LTA/LTB geram as entradas mais
assertivas no M5, mas o Mercury so media estrutura horizontal
(swing HH/HL, BOS/CHoCH, S/R, premium/discount). Nao havia nenhuma
diagonal — LTA (suporte ascendente) e LTB (resistencia descendente)
nao existiam no codigo (grep: zero implementacao de trendline).

Este modulo fecha o gap como OBSERVAVEL PURO (mesmo padrao de
m5_institutional_filters / next_candle_predictor):
- Opera SEMPRE sobre df_closed (velas fechadas, nunca a em formacao).
- Nunca altera decisao/score/ranking; nunca faz rede/broker.
- Matematica: pivots high/low (janela 3, mesma do next_candle_predictor)
  nos ultimos ~60 fechadas -> ate 4 fundos p/ LTA, ate 4 topos p/ LTB
  -> minimos quadrados (slope/intercept) -> touches (desvio <= 0.15*ATR)
  -> distancia do close a reta em ATRs -> breakout/posicao.
- LTA valida sse slope>0 e >=2 touches; LTB valida sse slope<0 e >=2 touches.
- Tudo None-safe: df curto/sem nivel/ATR => exists=False, nunca levanta.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

PIVOT_WINDOW = 3
LOOKBACK = 60
TOUCH_TOL_ATR = 0.15
MIN_TOUCHES = 2


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def _atr(df: Any, span: int = 14) -> Optional[float]:
    try:
        if df is None or len(df) < span + 1:
            return None
        h = df["High"].astype(float)
        lo = df["Low"].astype(float)
        c = df["Close"].astype(float)
        tr = (h - lo).abs().combine((h - c.shift()).abs(), max).combine(
            (lo - c.shift()).abs(), max)
        val = float(tr.rolling(span).mean().iloc[-1])
        return val if val > 0 else None
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def _pivots(h: List[float], lo: List[float],
            window: int = PIVOT_WINDOW
            ) -> Tuple[List[Tuple[int, float]], List[Tuple[int, float]]]:
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
    return tops[-6:], bots[-6:]


def _fit(points: List[Tuple[int, float]]) -> Tuple[float, float]:
    """Minimos quadrados: retorna (slope, intercept) em preco por indice."""
    n = len(points)
    sx = sum(p[0] for p in points)
    sy = sum(p[1] for p in points)
    sxx = sum(p[0] * p[0] for p in points)
    sxy = sum(p[0] * p[1] for p in points)
    den = n * sxx - sx * sx
    if den == 0:
        return 0.0, sy / n if n else 0.0
    slope = (n * sxy - sx * sy) / den
    intercept = (sy - slope * sx) / n
    return slope, intercept


def _line_state(points: List[Tuple[int, float]], last_idx: int,
                close: float, atr: float, want_up: bool) -> Dict[str, Any]:
    out: Dict[str, Any] = {
        "exists": False, "slope": None, "touches": 0,
        "distance_atr": None, "position": None, "breakout": False,
        "level": None,
    }
    if len(points) < 2 or not atr or atr <= 0:
        return out
    pts = points[-4:]
    slope, intercept = _fit(pts)
    # Valida inclinacao: LTA sobe, LTB desce.
    if want_up and slope <= 0:
        return out
    if not want_up and slope >= 0:
        return out
    level = slope * last_idx + intercept
    tol = TOUCH_TOL_ATR * atr
    touches = sum(1 for (i, p) in pts if abs(p - (slope * i + intercept)) <= tol)
    if touches < MIN_TOUCHES:
        return out
    dist = (close - level) / atr
    if abs(dist) <= TOUCH_TOL_ATR:
        pos = "AT"
    elif dist > 0:
        pos = "ABOVE"
    else:
        pos = "BELOW"
    # Breakout: fechou do outro lado da diagonal com margem.
    breakout = (pos == "BELOW") if want_up else (pos == "ABOVE")
    out.update(exists=True, slope=round(slope, 6), touches=touches,
               distance_atr=round(dist, 3), position=pos,
               breakout=bool(breakout), level=round(level, 5))
    return out


def trendlines(df_closed: Any) -> Dict[str, Any]:
    """LTA + LTB + vies diagonal. Tudo observavel, nunca bloqueia."""
    out: Dict[str, Any] = {
        "lta": {"exists": False}, "ltb": {"exists": False},
        "bias": "NEUTRAL", "detail": "",
    }
    try:
        if df_closed is None or len(df_closed) < 15:
            out["detail"] = "df insuficiente (<15 fechadas)"
            return out
        win = df_closed.iloc[-LOOKBACK:] if len(df_closed) >= LOOKBACK else df_closed
        h = [_f(v) for v in win["High"].tolist()]
        lo = [_f(v) for v in win["Low"].tolist()]
        c = [_f(v) for v in win["Close"].tolist()]
        atr = _atr(df_closed)
        if atr is None:
            out["detail"] = "ATR incalculavel"
            return out
        tops, bots = _pivots(h, lo)
        last_idx = len(win) - 1
        close = c[-1]
        lta = _line_state(bots, last_idx, close, atr, want_up=True)
        ltb = _line_state(tops, last_idx, close, atr, want_up=False)
        bias = "NEUTRAL"
        if lta.get("exists") and lta.get("position") in ("ABOVE", "AT") and not lta.get("breakout"):
            bias = "BULLISH"
        if ltb.get("exists") and ltb.get("position") in ("BELOW", "AT") and not ltb.get("breakout"):
            bias = "BEARISH" if bias == "NEUTRAL" else "NEUTRAL"  # squeeze: ambas ativas
        # Breakout tem precedencia direcional contra a linha rompida.
        if lta.get("exists") and lta.get("breakout"):
            bias = "BEARISH"
        if ltb.get("exists") and ltb.get("breakout"):
            bias = "BULLISH" if bias != "BEARISH" else "NEUTRAL"
        parts = []
        if lta.get("exists"):
            parts.append(f"LTA {lta['touches']} toques slope {lta['slope']} ({lta['position']})")
        if ltb.get("exists"):
            parts.append(f"LTB {ltb['touches']} toques slope {ltb['slope']} ({ltb['position']})")
        out.update(lta=lta, ltb=ltb, bias=bias,
                   detail=" + ".join(parts) if parts else "sem diagonal valida (>=2 toques)")
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        out["detail"] = "df invalido"
        return out


def trendline_flags(df_closed: Any, decision: str) -> Dict[str, Any]:
    """Pacote observavel alinhado a decisao (None-safe, nunca bloqueia).

    aligned True = diagonal a favor (BUY acima da LTA intacta / SELL abaixo
    da LTB intacta); False = rompida/contra; None = sem diagonal.
    """
    out: Dict[str, Any] = {
        "lta_exists": None, "ltb_exists": None, "trendline_bias": None,
        "trendline_aligned": None, "trendline_distance_atr": None,
        "trendline_detail": "",
    }
    dec = str(decision or "").upper()
    try:
        tl = trendlines(df_closed)
    except Exception:
        return out
    lta, ltb = tl.get("lta", {}), tl.get("ltb", {})
    out["lta_exists"] = bool(lta.get("exists"))
    out["ltb_exists"] = bool(ltb.get("exists"))
    out["trendline_bias"] = tl.get("bias", "NEUTRAL")
    out["trendline_detail"] = tl.get("detail", "")
    # Distancia mais relevante (linha do lado da decisao).
    if dec == "BUY" and lta.get("exists"):
        out["trendline_distance_atr"] = lta.get("distance_atr")
    elif dec == "SELL" and ltb.get("exists"):
        out["trendline_distance_atr"] = ltb.get("distance_atr")
    if dec not in ("BUY", "SELL"):
        return out
    if dec == "BUY":
        if lta.get("exists"):
            out["trendline_aligned"] = bool(lta.get("position") in ("ABOVE", "AT")
                                            and not lta.get("breakout"))
        else:
            out["trendline_aligned"] = None
    else:
        if ltb.get("exists"):
            out["trendline_aligned"] = bool(ltb.get("position") in ("BELOW", "AT")
                                            and not ltb.get("breakout"))
        else:
            out["trendline_aligned"] = None
    return out
