#!/usr/bin/env python3
"""Testa se Entry Timing, Regime e Displacement melhoram o G0 (sem gale)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _load(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    frame.columns = [str(c).lower() for c in frame.columns]
    frame.index = pd.to_datetime(frame.index, utc=True, format="mixed")
    return frame.sort_index()


def evaluate(frame: pd.DataFrame) -> pd.DataFrame:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    ema21 = close.ewm(span=21, adjust=False).mean().to_numpy()
    ema80 = close.ewm(span=80, adjust=False).mean().to_numpy()
    # Zonas de toque de corpo
    lookback, tolerance = 60, 0.0005
    zone_sup = np.full(n, np.nan)
    zone_res = np.full(n, np.nan)
    for i in range(lookback, n):
        bodies = np.concatenate([opens[i - lookback:i], closes[i - lookback:i]])
        sorted_b = np.sort(bodies)
        clusters = []
        cluster = [sorted_b[0]]
        for price in sorted_b[1:]:
            if abs(price - cluster[-1]) / cluster[-1] <= tolerance:
                cluster.append(price)
            else:
                if len(cluster) >= 2:
                    clusters.append(float(np.mean(cluster)))
                cluster = [price]
        if len(cluster) >= 2:
            clusters.append(float(np.mean(cluster)))
        current = closes[i]
        sup = [z for z in clusters if z < current]
        res = [z for z in clusters if z > current]
        if sup:
            zone_sup[i] = max(sup)
        if res:
            zone_res[i] = min(res)
    rows = []
    for i in range(lookback, n - 2):
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0 or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        upper = highs[i] - max(opens[i], closes[i])
        lower = min(opens[i], closes[i]) - lows[i]
        direction = None
        if np.isfinite(zone_res[i]) and (abs(closes[i] - zone_res[i]) / zone_res[i] <= 0.001 or highs[i] >= zone_res[i] * 0.9995):
            if closes[i] < opens[i] and upper >= 1.2 * body:
                direction = "SELL"
        if direction is None and np.isfinite(zone_sup[i]) and (abs(closes[i] - zone_sup[i]) / zone_sup[i] <= 0.001 or lows[i] <= zone_sup[i] * 1.0005):
            if closes[i] > opens[i] and lower >= 1.2 * body:
                direction = "BUY"
        if direction is None:
            continue
        entry = opens[i + 1]
        exit_ = closes[i + 1]
        hit = exit_ > entry if direction == "BUY" else exit_ < entry
        # Features para filtros
        trend_up = ema21[i] > ema80[i]
        trend_down = ema21[i] < ema80[i]
        regime = "TREND_UP" if trend_up else "TREND_DOWN" if trend_down else "RANGE"
        displacement = rng > 1.5 * atr[i]
        extension = abs(closes[i] - ema21[i]) / atr[i] if atr[i] > 0 else 0
        rows.append({
            "index": i,
            "direction": direction,
            "hit": bool(hit),
            "regime": regime,
            "displacement": bool(displacement),
            "extension": float(extension),
            "trend_aligned": bool((direction == "BUY" and trend_up) or (direction == "SELL" and trend_down)),
        })
    return pd.DataFrame(rows)


def _metrics(df: pd.DataFrame, mask: pd.Series) -> dict:
    sel = df[mask]
    total = len(sel)
    wins = int(sel["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe G0 improvement")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_g0_improvement.json")
    args = parser.parse_args()
    frames = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        part = evaluate(_load(path))
        part["symbol"] = path.stem
        frames.append(part)
    data = pd.concat(frames, ignore_index=True)
    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    filters = {
        "base": lambda d: pd.Series(True, index=d.index),
        "trend_aligned": lambda d: d["trend_aligned"],
        "no_displacement": lambda d: ~d["displacement"],
        "low_extension": lambda d: d["extension"] < 1.0,
        "regime_trend": lambda d: d["regime"].isin(["TREND_UP", "TREND_DOWN"]),
        "trend_no_disp": lambda d: d["trend_aligned"] & ~d["displacement"],
        "trend_low_ext": lambda d: d["trend_aligned"] & (d["extension"] < 1.0),
        "all_three": lambda d: d["trend_aligned"] & ~d["displacement"] & (d["extension"] < 1.0),
    }
    rows = []
    for name, fn in filters.items():
        rows.append({"filter": name, "train": _metrics(train, fn(train)), "test": _metrics(test, fn(test))})
    output = {"schema": "mercury.m5.g0-improvement.v1", "base_signals": len(data), "filters": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "filters": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
