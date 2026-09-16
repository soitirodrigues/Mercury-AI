"""Selo N3 — reversao em topos/fundos multiplos (SIGNAL-ONLY, nunca bloqueia).

Replica a leitura do backtest (scripts/backtest_n3_reversal.py) como
observavel puro sobre df_closed (so fechadas):
  - zonas: pivots janela 3 em 60 fechadas, cluster por tolerancia 0.15%
    (largura operacional; o 0.1% estrito do protocolo virou filtro de
    qualidade: n3_tight=True quando amplitude <= 0.1%).
  - >=3 toques, sem close alem da zona apos o 1o toque, revisita <=5 velas.
  - gatilho: rejeicao (pinbar 2x) ou engolfo na trigger N + toque.
  - wr_hist: win rate do backtest (reports/n3_reversal_result.json) quando
    n>=5; senao None (nunca inventa).
Tudo None-safe. Nunca altera decisao/score/ranking.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PIVOT_W = 3
LOOKBACK = 60
CLUSTER_TOL = 0.0015
TIGHT_TOL = 0.001
REVISIT_MAX = 5

_RESULT = Path("reports/n3_reversal_result.json")


@lru_cache(maxsize=1)
def _wr_table() -> Dict[str, float]:
    try:
        bt = json.loads(_RESULT.read_text(encoding="utf-8"))
        out = {}
        for s, m in (bt.get("per_asset") or {}).items():
            if isinstance(m, dict) and m.get("n", 0) >= 5 and m.get("win_rate") is not None:
                out[s] = float(m["win_rate"]) / 100.0
        return out
    except Exception:
        return {}


def _f(v: Any, default: float = 0.0) -> float:
    try:
        return float(v if v is not None else default)
    except (TypeError, ValueError):
        return default


def _atr(h: List[float], lo: List[float], c: List[float], span: int = 14) -> Optional[float]:
    try:
        import pandas as _pd
        hh, ll, cc = _pd.Series(h), _pd.Series(lo), _pd.Series(c)
        tr = (hh - ll).abs().combine((hh - cc.shift()).abs(), max).combine(
            (ll - cc.shift()).abs(), max)
        v = float(tr.rolling(span).mean().iloc[-1])
        return v if v > 0 else None
    except Exception:
        return None


def _pivots(h: List[float], lo: List[float], w: int = PIVOT_W):
    tops, bots = [], []
    n = len(h)
    for i in range(w, n - w):
        sh, sl = h[i - w:i + w + 1], lo[i - w:i + w + 1]
        if h[i] >= max(sh) and (sh.count(h[i]) == 1 or sh.index(h[i]) == w):
            if not tops or i - tops[-1][0] >= w:
                tops.append((i, h[i]))
        if lo[i] <= min(sl) and (sl.count(lo[i]) == 1 or sl.index(lo[i]) == w):
            if not bots or i - bots[-1][0] >= w:
                bots.append((i, lo[i]))
    return tops, bots


def n3_zones(df_closed: Any) -> List[Dict[str, Any]]:
    """Zonas N>=3 ativas na trigger N (observavel, sem bloquear)."""
    out: List[Dict[str, Any]] = []
    try:
        if df_closed is None or len(df_closed) < 61:
            return out
        win = df_closed.iloc[-LOOKBACK:]
        h = [_f(v) for v in win["High"].tolist()]
        lo = [_f(v) for v in win["Low"].tolist()]
        o = [_f(v) for v in win["Open"].tolist()]
        c = [_f(v) for v in win["Close"].tolist()]
        atr = _atr(h, lo, c)
        if not atr:
            return out
        tops, bots = _pivots(h, lo)
        for pivots, kind in ((tops, "RES"), (bots, "SUP")):
            zones: List[Dict[str, Any]] = []
            for i, p in pivots:
                hit = None
                for z in zones:
                    if abs(p - z["level"]) / z["level"] <= CLUSTER_TOL:
                        hit = z
                        break
                if hit is None:
                    zones.append({"level": p, "touches": [(i, p)], "kind": kind})
                else:
                    hit["touches"].append((i, p))
                    hit["level"] = sum(t[1] for t in hit["touches"]) / len(hit["touches"])
            for z in zones:
                if len(z["touches"]) < 3:
                    continue
                if z["touches"][-1][0] < len(c) - 1 - REVISIT_MAX:
                    continue
                lvl = z["level"]
                first = z["touches"][0][0]
                if any((cc > lvl * (1 + TIGHT_TOL)) if kind == "RES"
                       else (cc < lvl * (1 - TIGHT_TOL)) for cc in c[first:]):
                    continue
                direction = "SELL" if kind == "RES" else "BUY"
                r0, r1 = len(c) - 2, len(c) - 1
                rng = h[r1] - lo[r1]
                body = abs(c[r1] - o[r1])
                rej = False
                if rng > 0 and body > 0:
                    if direction == "SELL":
                        rej = c[r1] < o[r1] and (h[r1] - max(o[r1], c[r1])) >= 2.0 * body
                    else:
                        rej = c[r1] > o[r1] and (min(o[r1], c[r1]) - lo[r1]) >= 2.0 * body
                eng = ((c[r0] > o[r0]) and (c[r1] < o[r1]) and (c[r1] <= o[r0]) and (o[r1] >= c[r0])
                       if direction == "SELL" else
                       (c[r0] < o[r0]) and (c[r1] > o[r1]) and (c[r1] >= o[r0]) and (o[r1] <= c[r0]))
                touched = abs((h[r1] if direction == "SELL" else lo[r1]) - lvl) / lvl <= TIGHT_TOL * 3
                amp = (max(t[1] for t in z["touches"]) - min(t[1] for t in z["touches"])) / lvl
                out.append({"kind": kind, "direction": direction, "level": round(lvl, 5),
                            "touches": len(z["touches"]), "tight": bool(amp <= TIGHT_TOL),
                            "rejection": bool(rej or eng), "touched": bool(touched),
                            "dist_atr": round(abs(c[r1] - lvl) / atr, 2)})
        return out
    except (KeyError, IndexError, TypeError, ValueError):
        return []


def n3_seal(df_closed: Any, decision: str, symbol: str = "") -> Dict[str, Any]:
    """Selo N3 alinhado a decisao. Nones honestos; nunca bloqueia."""
    out: Dict[str, Any] = {"n3_touches": None, "n3_level": None, "n3_tight": None,
                           "n3_rejection": None, "n3_wr_hist": None, "n3_score": None,
                           "n3_detail": ""}
    dec = str(decision or "").upper()
    if dec not in ("BUY", "SELL"):
        return out
    want = "BUY" if dec == "BUY" else "SELL"
    try:
        zones = [z for z in n3_zones(df_closed) if z["direction"] == want]
    except Exception:
        return out
    if not zones:
        out["n3_detail"] = "sem zona N>=3 a favor"
        return out
    z = max(zones, key=lambda x: (x["touches"], x["rejection"], -x["dist_atr"]))
    wr = _wr_table().get(str(symbol or ""))
    bonus = 1.2 if z["rejection"] else 1.0
    prox = 1.5 if z["dist_atr"] <= 0.3 else 1.0
    score = round(z["touches"] * (wr if wr is not None else 0.5) * bonus * prox, 2)
    out.update(n3_touches=z["touches"], n3_level=z["level"], n3_tight=z["tight"],
               n3_rejection=z["rejection"], n3_wr_hist=(round(wr * 100, 1) if wr is not None else None),
               n3_score=score,
               n3_detail=(f"{z['touches']} toques em {z['level']} "
                          f"({'tight 0.1%' if z['tight'] else 'cluster 0.15%'})"
                          f"{' + REJEICAO' if z['rejection'] else ''}"))
    return out
