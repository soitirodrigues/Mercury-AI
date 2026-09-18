#!/usr/bin/env python3
"""Testa entrada intrabar apos sweep e reclaim dentro da mesma M5."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def evaluate(path: Path) -> dict:
    frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    frame.columns = [str(column).lower() for column in frame.columns]
    frame.index = pd.to_datetime(frame.index, utc=True)
    frame = frame.sort_index()
    frame["bucket"] = frame.index.floor("5min")
    grouped = frame.groupby("bucket", sort=True)
    m5 = grouped.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last"))
    m5["prior_high"] = m5["high"].rolling(20).max().shift(1)
    m5["prior_low"] = m5["low"].rolling(20).min().shift(1)
    observations = []
    for bucket, minute_rows in grouped:
        if bucket not in m5.index:
            continue
        current = m5.loc[bucket]
        if pd.isna(current["prior_high"]) or pd.isna(current["prior_low"]):
            continue
        prior_high, prior_low = float(current["prior_high"]), float(current["prior_low"])
        for timestamp, row in minute_rows.iterrows():
            close = float(row["close"])
            low = float(row["low"])
            high = float(row["high"])
            if low < prior_low and close > prior_low:
                entry = close
                hit = float(current["close"]) > entry
                observations.append({"timestamp": timestamp.isoformat(), "direction": "BUY", "hit": bool(hit), "entry": entry, "exit": float(current["close"])})
                break
            if high > prior_high and close < prior_high:
                entry = close
                hit = float(current["close"]) < entry
                observations.append({"timestamp": timestamp.isoformat(), "direction": "SELL", "hit": bool(hit), "entry": entry, "exit": float(current["close"])})
                break
    total = len(observations)
    wins = sum(int(row["hit"]) for row in observations)
    return {"file": path.name, "signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe intrabar M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m1_probe")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_intrabar_probe.json")
    args = parser.parse_args()
    results = [evaluate(path) for path in sorted(args.data_dir.glob("*_1m.csv"))]
    signals = sum(row["signals"] for row in results)
    wins = sum(row["wins"] for row in results)
    output = {"schema": "mercury.m5.intrabar-probe.v1", "contract": "sweep_reclaim_entry_to_same_m5_close", "results": results,
              "aggregate": {"assets": len(results), "signals": signals, "wins": wins,
                            "hit_rate": wins / signals if signals else None,
                            "net_payout_080": wins * 0.8 - (signals - wins)}}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
