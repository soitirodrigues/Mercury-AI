#!/usr/bin/env python3
"""Reproduz Q5, ALT e LAST2 do Alpha Code sobre M1 local, sem executar ordens."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def direction(row):
    if row.close > row.open:
        return True
    if row.close < row.open:
        return False
    return None


def run(path: Path) -> list[dict]:
    data = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    data.columns = [str(c).lower() for c in data.columns]
    data.index = pd.to_datetime(data.index, utc=True)
    data = data.sort_index()
    data["bucket"] = data.index.floor("5min")
    groups = [(bucket, group.sort_index()) for bucket, group in data.groupby("bucket", sort=True)]
    candles = []
    for bucket, group in groups:
        rows = list(group.itertuples())
        if len(rows) < 5:
            continue
        candles.append({"bucket": bucket, "rows": rows[:5]})
    outcomes = []
    for i, item in enumerate(candles):
        rows = item["rows"]
        dirs = [direction(row) for row in rows]
        if None not in dirs[:4] and dirs[0] == dirs[1] == dirs[2]:
            predicted = not dirs[0]
            outcomes.append({"strategy": "Q5", "hit": direction(rows[3]) == predicted})
        if i >= 1:
            prev = candles[i - 1]["rows"]
            prev_dirs = [direction(row) for row in prev]
            if None not in (prev_dirs[3], prev_dirs[4], dirs[0]) and prev_dirs[3] == prev_dirs[4]:
                outcomes.append({"strategy": "LAST2", "hit": direction(rows[0]) == (not prev_dirs[4])})
        if i >= 1:
            previous = candles[i - 1]["rows"][-1]
            # ALT is evaluated over four consecutive M1 candles, including
            # the final candle of the previous block and the first 3 current.
            seq = [direction(candles[i - 1]["rows"][-1])] + [direction(row) for row in rows[:3]]
            if None not in seq and seq[0] != seq[1] and seq[1] != seq[2] and seq[2] != seq[3]:
                outcomes.append({"strategy": "ALT", "hit": direction(rows[3]) == (not seq[3])})
    return outcomes


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe das estratégias Alpha Code")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m1_probe")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "alpha_code_strategy_probe.json")
    args = parser.parse_args()
    rows = []
    for path in sorted(args.data_dir.glob("*_1m.csv")):
        for result in run(path):
            rows.append({"symbol": path.stem, **result})
    summary = []
    for strategy in ("Q5", "ALT", "LAST2"):
        selected = [row for row in rows if row["strategy"] == strategy]
        wins = sum(row["hit"] for row in selected)
        total = len(selected)
        summary.append({"strategy": strategy, "signals": total, "wins": wins,
                        "hit_rate": wins / total if total else None,
                        "net_payout_080": wins * 0.8 - (total - wins)})
    output = {"schema": "mercury.alpha-code-probe.v1", "contract": "M1 color outcome, one candle", "summary": summary, "observations": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "summary": summary}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
