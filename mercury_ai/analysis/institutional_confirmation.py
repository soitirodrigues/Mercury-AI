"""M5 Institutional Confirmation — matematica SMC pura (SIGNAL-ONLY, sem pesos).

Regras absolutas:
- Opera SEMPRE sobre df_closed (velas fechadas, sem a vela em formacao).
- Nao altera engines, pesos, thresholds ou ranking existentes.
- Nao executa ordens, nao importa broker, nao faz rede.
- Retorna dicts simples (deteccao + score 0-100) para o seletor Top-3 consumir.

Criterios:
  Sweep:  low[i] < min(low[j]) - 0.1*ATR  AND close[i] > min(low[j])  (bull-trap invertido p/ short)
  Displacement: range >= 1.8*ATR AND corpo >= 0.6*range AND close no terco
                direcional AND volume >= 1.5*SMA20 AND rompe swing anterior
  FVG: gap >= 0.2*ATR e nao preenchido nas velas seguintes
  Score: Sweep 25 + Displacement 20 + FVG/OB 20 + CHoCH/BOS 15 + MTF 10 + Volume 10
  Gate Top-3: score >= 70 AND RR >= 2.0 AND timing VALID (ver top3_selector)
"""
from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd

SWEEP_LOOKBACK = 20
SWEEP_WICK_ATR = 0.1
DISP_ATR_MULT = 1.8
DISP_BODY_RATIO = 0.6
DISP_VOL_MULT = 1.5
DISP_VOL_WINDOW = 20
FVG_MIN_ATR = 0.2


def atr14(df: pd.DataFrame) -> float:
    """ATR-14 classico sobre High/Low/Close."""
    h = pd.to_numeric(df["High"], errors="coerce")
    l = pd.to_numeric(df["Low"], errors="coerce")
    c = pd.to_numeric(df["Close"], errors="coerce")
    tr = pd.concat([(h - l), (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    val = tr.rolling(14).mean().iloc[-1]
    return float(val) if pd.notna(val) and val > 0 else 0.0


def closed_df(df: pd.DataFrame) -> pd.DataFrame:
    """Remove a vela em formacao (ultima linha). Anti-repaint."""
    if df is None or len(df) < 2:
        return df
    return df.iloc[:-1].copy()


def detect_liquidity_sweep(df_closed: pd.DataFrame, atr: float, lookback: int = SWEEP_LOOKBACK) -> Dict[str, Any]:
    """Sweep com reclaim (wick). Retorna {detected, direction, level, index}.

    lookback parametrizável (default 20 = legado): IDM usa janela curta (5)
    sem mutação global — a divergência de Pecados auditada em 2026-09-14
    (6 vs 0 combos) veio de mutação de SWEEP_LOOKBACK entre probes.
    """
    try:
        lb = int(lookback)
    except (TypeError, ValueError):
        lb = SWEEP_LOOKBACK
    lb = max(2, lb)
    out: Dict[str, Any] = {"detected": False, "direction": "NONE", "level": None, "index": None}
    if df_closed is None or len(df_closed) < lb + 2 or atr <= 0:
        return out
    df = df_closed.reset_index(drop=True)
    for i in range(lb, len(df)):
        win_lo = float(df["Low"].iloc[i - lb:i].min())
        win_hi = float(df["High"].iloc[i - lb:i].max())
        lo, hi, cl = float(df["Low"].iloc[i]), float(df["High"].iloc[i]), float(df["Close"].iloc[i])
        # Bear-trap -> LONG
        if lo < win_lo - SWEEP_WICK_ATR * atr and cl > win_lo and (win_lo - lo) >= SWEEP_WICK_ATR * atr:
            out.update(detected=True, direction="BULLISH", level=win_lo, index=i)
            return out
        # Bull-trap -> SHORT
        if hi > win_hi + SWEEP_WICK_ATR * atr and cl < win_hi and (hi - win_hi) >= SWEEP_WICK_ATR * atr:
            out.update(detected=True, direction="BEARISH", level=win_hi, index=i)
            return out
    return out


def detect_displacement(df_closed: pd.DataFrame, atr: float) -> Dict[str, Any]:
    """Vela de forca que rompe estrutura com volume. Retorna {detected, direction, index}."""
    out: Dict[str, Any] = {"detected": False, "direction": "NONE", "index": None}
    if df_closed is None or len(df_closed) < SWEEP_LOOKBACK + 2 or atr <= 0:
        return out
    df = df_closed.reset_index(drop=True)
    vol = pd.to_numeric(df["Volume"], errors="coerce") if "Volume" in df.columns else None
    vol_avg = vol.rolling(DISP_VOL_WINDOW).mean() if vol is not None else None
    for i in range(SWEEP_LOOKBACK, len(df)):
        o, h, l, c = (float(df[x].iloc[i]) for x in ("Open", "High", "Low", "Close"))
        rng = h - l
        if rng < DISP_ATR_MULT * atr or rng <= 0:
            continue
        body = abs(c - o)
        if body < DISP_BODY_RATIO * rng:
            continue
        v = float(vol.iloc[i]) if vol is not None else 0.0
        va = float(vol_avg.iloc[i]) if vol_avg is not None else 0.0
        if vol is not None and (pd.isna(va) or va <= 0 or v < DISP_VOL_MULT * va):
            continue
        prev_hi = float(df["High"].iloc[i - SWEEP_LOOKBACK:i].max())
        prev_lo = float(df["Low"].iloc[i - SWEEP_LOOKBACK:i].min())
        bull = c > o and c >= h - 0.25 * rng and c > prev_hi
        bear = c < o and c <= l + 0.25 * rng and c < prev_lo
        if bull:
            out.update(detected=True, direction="BULLISH", index=i)
            return out
        if bear:
            out.update(detected=True, direction="BEARISH", index=i)
            return out
    return out


def detect_fvg(df_closed: pd.DataFrame, atr: float) -> Dict[str, Any]:
    """FVG bullish/bearish aberto com gap >= 0.2*ATR. Retorna {detected, direction, top, bottom}."""
    out: Dict[str, Any] = {"detected": False, "direction": "NONE", "top": None, "bottom": None, "index": None}
    if df_closed is None or len(df_closed) < 5 or atr <= 0:
        return out
    df = df_closed.reset_index(drop=True)
    # Varre trios (i-2, i-1, i); o mais recente aberto prevalece
    for i in range(len(df) - 1, 2, -1):
        h1, l3 = float(df["High"].iloc[i - 2]), float(df["Low"].iloc[i])
        l1, h3 = float(df["Low"].iloc[i - 2]), float(df["High"].iloc[i])
        if l3 > h1 and (l3 - h1) >= FVG_MIN_ATR * atr:
            # fill check: nenhum low posterior <= h1
            if (df["Low"].iloc[i + 1:] <= h1).any():
                continue
            out.update(detected=True, direction="BULLISH", top=l3, bottom=h1, index=i)
            return out
        if h3 < l1 and (l1 - h3) >= FVG_MIN_ATR * atr:
            if (df["High"].iloc[i + 1:] >= l1).any():
                continue
            out.update(detected=True, direction="BEARISH", top=l1, bottom=h3, index=i)
            return out
    return out


def score_setup(sweep: Dict[str, Any], disp: Dict[str, Any], fvg_or_ob: bool,
                choch_bos_ok: bool, mtf_aligned: bool, volume_ok: bool) -> Dict[str, Any]:
    """Score 0-100 com pesos fixos documentados. Nao altera nenhum motor."""
    parts = {
        "sweep": 25.0 if sweep.get("detected") else 0.0,
        "displacement": 20.0 if disp.get("detected") else 0.0,
        "fvg_ob": 20.0 if fvg_or_ob else 0.0,
        "choch_bos": 15.0 if choch_bos_ok else 0.0,
        "mtf": 10.0 if mtf_aligned else 0.0,
        "volume": 10.0 if volume_ok else 0.0,
    }
    total = round(sum(parts.values()), 1)
    dirs = [sweep.get("direction"), disp.get("direction")]
    dirs = [d for d in dirs if d in ("BULLISH", "BEARISH")]
    direction = dirs[0] if dirs and all(d == dirs[0] for d in dirs) else "NONE"
    if total < 70:
        direction = "NONE"
    return {"score": total, "parts": parts, "direction": direction,
            "pass_gate": total >= 70.0 and direction != "NONE"}
