#!/usr/bin/env python3
"""Replay fiel da prioridade Q5 -> ALT -> LAST2, sem ordens reais."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def color(row):
    if row.close > row.open:
        return True
    if row.close < row.open:
        return False
    return None


def replay(path: Path) -> list[dict]:
    frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    frame.columns = [str(c).lower() for c in frame.columns]
    frame.index = pd.to_datetime(frame.index, utc=True)
    frame = frame.sort_index()
    frame["bucket"] = frame.index.floor("5min")
    groups = [(bucket, list(group.sort_index().itertuples())) for bucket, group in frame.groupby("bucket", sort=True)]
    candles = [(bucket, rows[:5]) for bucket, rows in groups if len(rows) >= 5]
    results = []
    used_quadrants = set()
    for i, (bucket, rows) in enumerate(candles):
        if len(rows) < 5:
            continue
        current = [color(row) for row in rows]
        if i >= 1:
            previous = candles[i - 1][1]
            prev = [color(row) for row in previous]
        else:
            prev = []
        candidate = None
        if current[0] is not None and current[0] == current[1] == current[2]:
            candidate = ("Q5", not current[0], current[3])
        if candidate is None and len(prev) >= 5 and prev[3] is not None and prev[3] == prev[4] and current[0] is not None:
            candidate = ("LAST2", not prev[4], current[0])
        if candidate is None and i >= 1:
            seq = [prev[4]] + current[:3]
            if None not in seq and seq[0] != seq[1] and seq[1] != seq[2] and seq[2] != seq[3]:
                candidate = ("ALT", not seq[3], current[3])
        if candidate is None:
            continue
        strategy, predicted_call, result_color = candidate
        if bucket in used_quadrants:
            continue
        used_quadrants.add(bucket)
        results.append({"timestamp": bucket.isoformat(), "strategy": strategy,
                        "direction": "CALL" if predicted_call else "PUT",
                        "hit": result_color is not None and result_color == predicted_call})
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Replay Alpha Code sem corretora")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m1_probe")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "alpha_code_exact_replay.json")
    args = parser.parse_args()
    rows = []
    for path in sorted(args.data_dir.glob("*_1m.csv")):
        rows.extend({"symbol": path.stem, **row} for row in replay(path))
    n = len(rows)
    split = int(n * 0.8)
    summary = []
    for name, sample in (("all", rows), ("train_validation", rows[:split]), ("test", rows[split:])):
        wins = sum(row["hit"] for row in sample)
        total = len(sample)
        summary.append({"split": name, "signals": total, "wins": wins,
                        "hit_rate": wins / total if total else None,
                        "net_payout_080": wins * 0.8 - (total - wins)})
    output = {"schema": "mercury.alpha-code-exact-replay.v1", "priority": ["Q5", "LAST2", "ALT"], "summary": summary, "observations": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "summary": summary}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
