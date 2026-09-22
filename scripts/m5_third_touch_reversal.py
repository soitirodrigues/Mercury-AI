#!/usr/bin/env python3
"""Testa terceiro toque em zona horizontal com reversao e gale."""
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


def _touches(frame: pd.DataFrame, index: int, tolerance: float = 0.001) -> tuple[list[float], list[float]]:
    if index < 60:
        return [], []
    window = frame.iloc[:index]
    close = window["close"].astype(float).to_numpy()
    current = close[-1]
    history = close[-121:-1]
    if len(history) < 2:
        return [], []
    reference = float(np.mean(history))
    rounded = np.round(history / (reference * tolerance)).astype(int)
    counts = pd.Series(rounded).value_counts()
    levels = counts[counts >= 2].index.to_numpy() * reference * tolerance
    support = [float(level) for level in levels if level < current]
    resistance = [float(level) for level in levels if level > current]
    return support, resistance


def evaluate(frame: pd.DataFrame, max_gales: int) -> list[dict]:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    results = []
    for i in range(120, len(frame) - (max_gales + 2)):
        support, resistance = _touches(frame, i)
        if not support and not resistance:
            continue
        body = abs(close.iloc[i] - open_.iloc[i])
        rng = high.iloc[i] - low.iloc[i]
        if rng <= 0:
            continue
        upper = high.iloc[i] - max(open_.iloc[i], close.iloc[i])
        lower = min(open_.iloc[i], close.iloc[i]) - low.iloc[i]
        direction = None
        if resistance and (high.iloc[i] >= min(resistance) * 0.999 or abs(close.iloc[i] - min(resistance)) / min(resistance) <= 0.001):
            if close.iloc[i] < open_.iloc[i] and upper >= 1.5 * body:
                direction = "SELL"
        if direction is None and support and (low.iloc[i] <= max(support) * 1.001 or abs(close.iloc[i] - max(support)) / max(support) <= 0.001):
            if close.iloc[i] > open_.iloc[i] and lower >= 1.5 * body:
                direction = "BUY"
        if direction is None:
            continue
        outcomes = []
        for leg in range(max_gales + 1):
            entry = open_.iloc[i + leg]
            exit_ = close.iloc[i + leg]
            hit = exit_ > entry if direction == "BUY" else exit_ < entry
            outcomes.append(bool(hit))
            if hit:
                break
        results.append({"index": int(i), "direction": direction, "outcomes": outcomes, "hit": bool(outcomes[-1])})
    return results


def _metrics(rows: list[dict]) -> dict:
    total = len(rows)
    wins = sum(row["hit"] for row in rows)
    direct = sum(row["outcomes"][0] for row in rows)
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "direct_hit_rate": direct / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe terceiro toque M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_third_touch_reversal.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        rows = evaluate(_load(path), args.max_gales)
        split = int(len(rows) * 0.8)
        results.append({"symbol": path.stem, "train": _metrics(rows[:split]), "test": _metrics(rows[split:]), "observations": rows})
    all_rows = [row for item in results for row in item["observations"]]
    split = int(len(all_rows) * 0.8)
    output = {"schema": "mercury.m5.third-touch-reversal.v1", "aggregate": {"train": _metrics(all_rows[:split]), "test": _metrics(all_rows[split:])}, "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
