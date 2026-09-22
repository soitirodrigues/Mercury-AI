"""Zone Touch Reversal — reversao em zonas de toque de corpo (SIGNAL-ONLY).

Estrategia validada (2026-09-20, reports/m5_body_touch_zones_fixed.json):
  - Zonas horizontais onde o CORPO (open/close) tocou 2+ vezes na mesma faixa
    (cluster por tolerancia 0.05% sobre janela de 60 fechadas).
  - Entrada no toque da zona com vela de rejeicao (pavio >= 1.2x corpo).
  - Direcao CONTRA o movimento: toque em resistencia -> SELL, suporte -> BUY.
  - Resultado medido na vela SEGUINTE (sem lookahead).
  - Teste final: 86,25% com gale 1+2 (20.721 sinais); 47,5% sem gale.

Contrato:
- Opera SOMENTE sobre df_closed (velas fechadas).
- Nunca altera decisao/score/ranking do pipeline; o signal_builder decide se
  usa como override de WAIT (mesmo padrao do sweep_override).
- Nunca executa ordens, nunca faz rede.
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np

LOOKBACK = 60
TOLERANCE = 0.0005
MIN_TOUCHES = 2
WICK_RATIO_MIN = 1.2
TOUCH_TOL = 0.001


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def detect_zone_reversal(
    df_closed: Any,
    lookback: int = LOOKBACK,
    tolerance: float = TOLERANCE,
    min_touches: int = MIN_TOUCHES,
    wick_ratio_min: float = WICK_RATIO_MIN,
) -> Dict[str, Any]:
    """Detecta terceiro toque em zona de corpo com rejeicao.

    Retorna {detected, direction, zone, touches, wick_ratio, reason}.
    Nones/False honestos quando df insuficiente ou sem padrao.
    """
    out: Dict[str, Any] = {
        "detected": False, "direction": "NONE", "zone": None,
        "touches": 0, "wick_ratio": 0.0, "reason": "sem padrao",
    }
    try:
        if df_closed is None or len(df_closed) < lookback + 1:
            out["reason"] = "df insuficiente"
            return out
        window = df_closed.iloc[-(lookback + 1):]
        opens = [_f(v) for v in window["Open"].tolist()]
        closes = [_f(v) for v in window["Close"].tolist()]
        highs = [_f(v) for v in window["High"].tolist()]
        lows = [_f(v) for v in window["Low"].tolist()]
    except (KeyError, IndexError, TypeError, ValueError):
        out["reason"] = "df invalido"
        return out

    # Zonas: cluster de corpos das velas ANTERIORES (exclui a trigger).
    bodies = np.array(opens[:-1] + closes[:-1])
    if len(bodies) < 4:
        return out
    sorted_b = np.sort(bodies)
    clusters: list[tuple[float, int]] = []
    cluster = [sorted_b[0]]
    for price in sorted_b[1:]:
        if abs(price - cluster[-1]) / cluster[-1] <= tolerance:
            cluster.append(price)
        else:
            if len(cluster) >= min_touches:
                clusters.append((float(np.mean(cluster)), len(cluster)))
            cluster = [price]
    if len(cluster) >= min_touches:
        clusters.append((float(np.mean(cluster)), len(cluster)))
    if not clusters:
        return out

    o, h, lo, c = opens[-1], highs[-1], lows[-1], closes[-1]
    rng = h - lo
    body = abs(c - o)
    if rng <= 0 or body <= 0:
        out["reason"] = "range/corpo nulo"
        return out
    upper = h - max(o, c)
    lower = min(o, c) - lo

    sup = [z for z in clusters if z[0] < c]
    res = [z for z in clusters if z[0] > c]

    # Toque em resistencia + rejeicao -> SELL
    if res:
        zone, touches = min(res, key=lambda z: abs(z[0] - c))
        touched = abs(c - zone) / zone <= TOUCH_TOL or h >= zone * (1 - TOUCH_TOL / 2)
        if touched and c < o and upper >= wick_ratio_min * body:
            out.update(detected=True, direction="SELL", zone=round(zone, 5),
                       touches=touches, wick_ratio=round(upper / rng, 3),
                       reason=f"toque em resistencia {zone:.5f} ({touches} toques) + pavio {upper / rng:.0%}")
            return out
    # Toque em suporte + rejeicao -> BUY
    if sup:
        zone, touches = max(sup, key=lambda z: z[0])
        touched = abs(c - zone) / zone <= TOUCH_TOL or lo <= zone * (1 + TOUCH_TOL / 2)
        if touched and c > o and lower >= wick_ratio_min * body:
            out.update(detected=True, direction="BUY", zone=round(zone, 5),
                       touches=touches, wick_ratio=round(lower / rng, 3),
                       reason=f"toque em suporte {zone:.5f} ({touches} toques) + pavio {lower / rng:.0%}")
            return out
    return out
