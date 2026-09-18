#!/usr/bin/env python3
"""Gera relatorio walk-forward M5 a partir de um CSV OHLCV local."""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.signals.m5_walk_forward import evaluate_walk_forward


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="M5 walk-forward sem lookahead")
    parser.add_argument("csv", type=Path, help="CSV com Open/High/Low/Close e timestamp opcional")
    parser.add_argument("--out", type=Path, default=None, help="Arquivo JSON de saida")
    parser.add_argument("--timestamp-column", default=None, help="Coluna temporal do CSV")
    parser.add_argument("--min-history", type=int, default=60)
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--payout", type=float, default=0.80)
    parser.add_argument("--cost", type=float, default=0.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.csv.exists():
        raise SystemExit(f"CSV nao encontrado: {args.csv}")
    frame = pd.read_csv(args.csv)
    timestamp_column = args.timestamp_column
    if timestamp_column is None:
        for candidate in ("timestamp", "datetime", "date", "time"):
            if candidate in frame.columns:
                timestamp_column = candidate
                break
    if timestamp_column:
        if timestamp_column not in frame.columns:
            raise SystemExit(f"coluna temporal nao encontrada: {timestamp_column}")
        frame[timestamp_column] = pd.to_datetime(frame[timestamp_column], utc=True)
        frame = frame.set_index(timestamp_column)

    report = evaluate_walk_forward(
        frame,
        min_history=args.min_history,
        horizon=args.horizon,
        payout=args.payout,
        cost=args.cost,
    )
    report["source"] = {
        "csv": str(args.csv),
        "timestamp_column": timestamp_column,
    }
    report["observations"] = [asdict(row) for row in report["observations"]]
    output = args.out or args.csv.with_suffix(".walk_forward.json")
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(output), "overall": report["overall"], "test": report["splits"]["test"]}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
