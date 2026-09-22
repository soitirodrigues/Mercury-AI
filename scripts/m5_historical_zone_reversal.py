#!/usr/bin/env python3
"""Testa reversao em zonas historicas de topos/fundos com gale opcional."""
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


def _zones(frame: pd.DataFrame, index: int, lookback: int = 120) -> tuple[float | None, float | None]:
    if index < lookback:
        return None, None
    window = frame.iloc[index - lookback:index]
    highs = window["high"].astype(float).to_numpy()
    lows = window["low"].astype(float).to_numpy()
    closes = window["close"].astype(float).to_numpy()
    opens = window["open"].astype(float).to_numpy()
    tops = []
    bottoms = []
    for i in range(3, len(window) - 3):
        if highs[i] >= max(highs[i - 3:i + 4]):
            tops.append(highs[i])
        if lows[i] <= min(lows[i - 3:i + 4]):
            bottoms.append(lows[i])
    if not tops or not bottoms:
        return None, None
    return float(np.median(bottoms[-4:])), float(np.median(tops[-4:]))


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> list[dict]:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    highs = high.to_numpy()
    lows = low.to_numpy()
    top_mask = np.zeros(len(frame), dtype=bool)
    bottom_mask = np.zeros(len(frame), dtype=bool)
    for i in range(3, len(frame) - 3):
        top_mask[i] = highs[i] >= highs[i - 3:i + 4].max()
        bottom_mask[i] = lows[i] <= lows[i - 3:i + 4].min()
    top_values = pd.Series(np.where(top_mask, highs, np.nan), index=frame.index)
    bottom_values = pd.Series(np.where(bottom_mask, lows, np.nan), index=frame.index)
    zone_high_series = top_values.rolling(120, min_periods=4).apply(lambda x: np.nanmedian(x[-4:]), raw=True).shift(1)
    zone_low_series = bottom_values.rolling(120, min_periods=4).apply(lambda x: np.nanmedian(x[-4:]), raw=True).shift(1)
    results = []
    for i in range(120, len(frame) - (max_gales + 2)):
        zone_low = zone_low_series.iloc[i]
        zone_high = zone_high_series.iloc[i]
        if not np.isfinite(zone_low) or not np.isfinite(zone_high):
            continue
        body = abs(close.iloc[i] - open_.iloc[i])
        rng = high.iloc[i] - low.iloc[i]
        if rng <= 0:
            continue
        upper = high.iloc[i] - max(open_.iloc[i], close.iloc[i])
        lower = min(open_.iloc[i], close.iloc[i]) - low.iloc[i]
        touched_low = low.iloc[i] <= zone_low * 1.001 or abs(close.iloc[i] - zone_low) / zone_low <= 0.001
        touched_high = high.iloc[i] >= zone_high * 0.999 or abs(close.iloc[i] - zone_high) / zone_high <= 0.001
        rejection_buy = touched_low and close.iloc[i] > open_.iloc[i] and lower >= 1.5 * body
        rejection_sell = touched_high and close.iloc[i] < open_.iloc[i] and upper >= 1.5 * body
        if not (rejection_buy or rejection_sell):
            continue
        direction = "BUY" if rejection_buy else "SELL"
        outcomes = []
        for leg in range(max_gales + 1):
            entry = open_.iloc[i + leg]
            exit_ = close.iloc[i + leg]
            hit = exit_ > entry if direction == "BUY" else exit_ < entry
            outcomes.append(hit)
            if hit:
                break
        results.append({"index": int(i), "direction": direction, "outcomes": [bool(x) for x in outcomes], "hit": bool(outcomes[-1])})
    return results


def _metrics(rows: list[dict], max_gales: int) -> dict:
    total = len(rows)
    wins = sum(row["hit"] for row in rows)
    direct = sum(row["outcomes"][0] for row in rows)
    return {
        "signals": total,
        "wins": wins,
        "hit_rate": wins / total if total else None,
        "direct_hit_rate": direct / total if total else None,
        "net_payout_080": wins * 0.8 - (total - wins),
        "max_gales": max_gales,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe zonas historicas M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_historical_zone_reversal.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        rows = evaluate(_load(path), args.max_gales)
        split = int(len(rows) * 0.8)
        results.append({"symbol": path.stem, "train": _metrics(rows[:split], args.max_gales), "test": _metrics(rows[split:], args.max_gales), "observations": rows})
    all_rows = [row for item in results for row in item["observations"]]
    split = int(len(all_rows) * 0.8)
    output = {"schema": "mercury.m5.historical-zone-reversal.v1", "aggregate": {"train": _metrics(all_rows[:split], args.max_gales), "test": _metrics(all_rows[split:], args.max_gales)}, "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
