#!/usr/bin/env python3
"""Probe CCL: Continuacao -> Consolidacao -> Liquidez -> entrada a favor."""
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


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> list[dict]:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    results = []
    for i in range(30, n - (max_gales + 2)):
        if not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        # 1) CONTINUACAO: 2-3 velas fortes na mesma direcao antes da caixa
        c1, c2 = closes[i - 5:i - 3], closes[i - 4:i - 2]
        o1 = opens[i - 5:i - 3]
        bull_cont = all(closes[j] > opens[j] for j in range(i - 5, i - 3)) and closes[i - 3] > closes[i - 5]
        bear_cont = all(closes[j] < opens[j] for j in range(i - 5, i - 3)) and closes[i - 3] < closes[i - 5]
        if not (bull_cont or bear_cont):
            continue
        # 2) CONSOLIDACAO: caixa de 2-4 velas com range estreito (< 0.8 ATR total)
        box = slice(i - 3, i)
        box_high = highs[box].max()
        box_low = lows[box].min()
        box_range = box_high - box_low
        if box_range <= 0 or box_range > 0.8 * atr[i]:
            continue
        # 3) LIQUIDEZ: vela atual varre a caixa contra a tendencia e fecha de volta
        sweep_low = lows[i] < box_low and closes[i] > box_low
        sweep_high = highs[i] > box_high and closes[i] < box_high
        direction = None
        if bull_cont and sweep_low:
            direction = "BUY"
        elif bear_cont and sweep_high:
            direction = "SELL"
        if direction is None:
            continue
        # 4) ENTRADA: proxima vela na direcao da tendencia
        outcomes = []
        for leg in range(1, max_gales + 2):
            entry = opens[i + leg]
            exit_ = closes[i + leg]
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
    parser = argparse.ArgumentParser(description="Probe CCL M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_ccl_continuation_probe.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        rows = evaluate(_load(path), args.max_gales)
        split = int(len(rows) * 0.8)
        results.append({"symbol": path.stem, "train": _metrics(rows[:split]), "test": _metrics(rows[split:]), "observations": rows})
    all_rows = [row for item in results for row in item["observations"]]
    split = int(len(all_rows) * 0.8)
    output = {"schema": "mercury.m5.ccl-continuation.v1", "aggregate": {"train": _metrics(all_rows[:split]), "test": _metrics(all_rows[split:])}, "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
