#!/usr/bin/env python3
"""Filtros sobre zone touch: volume spike, time-of-day, ATR expansion."""
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


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> pd.DataFrame:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    volume = frame["volume"].astype(float).to_numpy() if "volume" in frame.columns else np.ones(n)
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    vol_avg = pd.Series(volume).rolling(20).mean().to_numpy()
    # Zonas de toque de corpo (mesma logica do zone_touch_reversal)
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
    for i in range(lookback, n - (max_gales + 2)):
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
        rows.append({
            "index": i,
            "direction": direction,
            "hit": bool(hit),
            "volume_spike": bool(volume[i] > 1.5 * vol_avg[i]) if np.isfinite(vol_avg[i]) else False,
            "london_ny": frame.index[i].hour in range(7, 17),
            "atr_expansion": bool(rng > 2.0 * atr[i]),
        })
    return pd.DataFrame(rows)


def _metrics(df: pd.DataFrame, mask: pd.Series) -> dict:
    sel = df[mask]
    total = len(sel)
    wins = int(sel["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Filtros sobre zone touch")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_zone_filters.json")
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
        "volume_spike": lambda d: d["volume_spike"],
        "london_ny": lambda d: d["london_ny"],
        "no_atr_expansion": lambda d: ~d["atr_expansion"],
        "vol_spike_london": lambda d: d["volume_spike"] & d["london_ny"],
        "vol_spike_no_atr": lambda d: d["volume_spike"] & ~d["atr_expansion"],
        "london_no_atr": lambda d: d["london_ny"] & ~d["atr_expansion"],
        "all_three": lambda d: d["volume_spike"] & d["london_ny"] & ~d["atr_expansion"],
    }
    rows = []
    for name, fn in filters.items():
        rows.append({"filter": name, "train": _metrics(train, fn(train)), "test": _metrics(test, fn(test))})
    output = {"schema": "mercury.m5.zone-filters.v1", "base_signals": len(data), "filters": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "filters": rows}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
