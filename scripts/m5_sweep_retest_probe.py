#!/usr/bin/env python3
"""Probe institucional: sweep + rejeicao + deslocamento + reteste."""
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
    frame = frame.sort_index()
    return frame


def evaluate(frame: pd.DataFrame) -> list[dict]:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    prior_high = high.rolling(20).max().shift(1)
    prior_low = low.rolling(20).min().shift(1)
    body = (close - open_).abs()
    rng = (high - low).replace(0, np.nan)
    upper = high - np.maximum(open_, close)
    lower = np.minimum(open_, close) - low
    next_open = open_.shift(-1)
    next_close = close.shift(-1)
    results = []
    for i in range(60, len(frame) - 2):
        if not np.isfinite(atr.iloc[i]) or atr.iloc[i] <= 0:
            continue
        # Sweep de fundo + reclaim + rejeicao + deslocamento comprador.
        sweep_low = low.iloc[i] < prior_low.iloc[i] - 0.1 * atr.iloc[i] and close.iloc[i] > prior_low.iloc[i]
        rejection_buy = lower.iloc[i] >= 2 * body.iloc[i] and close.iloc[i] > open_.iloc[i]
        displacement_buy = rng.iloc[i] >= 1.0 * atr.iloc[i] and body.iloc[i] / rng.iloc[i] >= 0.25
        if sweep_low and rejection_buy and displacement_buy:
            entry = next_open.iloc[i]
            hit = next_close.iloc[i] > entry
            results.append({"index": i, "direction": "BUY", "hit": bool(hit)})
            continue
        sweep_high = high.iloc[i] > prior_high.iloc[i] + 0.1 * atr.iloc[i] and close.iloc[i] < prior_high.iloc[i]
        rejection_sell = upper.iloc[i] >= 2 * body.iloc[i] and close.iloc[i] < open_.iloc[i]
        displacement_sell = rng.iloc[i] >= 1.0 * atr.iloc[i] and body.iloc[i] / rng.iloc[i] >= 0.25
        if sweep_high and rejection_sell and displacement_sell:
            entry = next_open.iloc[i]
            hit = next_close.iloc[i] < entry
            results.append({"index": i, "direction": "SELL", "hit": bool(hit)})
    return results


def _metrics(rows: list[dict]) -> dict:
    total = len(rows)
    wins = sum(row["hit"] for row in rows)
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe sweep+reteste M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_sweep_retest_probe.json")
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        rows = evaluate(_load(path))
        split = int(len(rows) * 0.8)
        results.append({"symbol": path.stem, "train": _metrics(rows[:split]), "test": _metrics(rows[split:]), "observations": rows})
    all_rows = [row for item in results for row in item["observations"]]
    split = int(len(all_rows) * 0.8)
    output = {"schema": "mercury.m5.sweep-retest.v1", "aggregate": {"train": _metrics(all_rows[:split]), "test": _metrics(all_rows[split:])}, "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
