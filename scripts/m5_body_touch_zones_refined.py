#!/usr/bin/env python3
"""Refinamento de zonas de toque de corpo com parametros ajustaveis."""
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


def evaluate(frame: pd.DataFrame, lookback: int, tolerance: float, min_touches: int, wick_ratio: float, max_gales: int) -> list[dict]:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens = open_.to_numpy()
    closes = close.to_numpy()
    highs = high.to_numpy()
    lows = low.to_numpy()
    zone_support = np.full(n, np.nan)
    zone_resistance = np.full(n, np.nan)
    for i in range(lookback, n):
        bodies = np.concatenate([opens[i - lookback:i], closes[i - lookback:i]])
        if len(bodies) < 4:
            continue
        sorted_b = np.sort(bodies)
        clusters = []
        cluster = [sorted_b[0]]
        for price in sorted_b[1:]:
            if abs(price - cluster[-1]) / cluster[-1] <= tolerance:
                cluster.append(price)
            else:
                if len(cluster) >= min_touches:
                    clusters.append(float(np.mean(cluster)))
                cluster = [price]
        if len(cluster) >= min_touches:
            clusters.append(float(np.mean(cluster)))
        current = closes[i]
        sup = [z for z in clusters if z < current]
        res = [z for z in clusters if z > current]
        if sup:
            zone_support[i] = max(sup)
        if res:
            zone_resistance[i] = min(res)
    results = []
    for i in range(lookback, n - (max_gales + 2)):
        support = zone_support[i]
        resistance = zone_resistance[i]
        if not np.isfinite(support) and not np.isfinite(resistance):
            continue
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0:
            continue
        upper = highs[i] - max(opens[i], closes[i])
        lower = min(opens[i], closes[i]) - lows[i]
        direction = None
        if np.isfinite(resistance):
            if abs(closes[i] - resistance) / resistance <= 0.001 or highs[i] >= resistance * 0.9995:
                if closes[i] < opens[i] and upper >= wick_ratio * body:
                    direction = "SELL"
        if direction is None and np.isfinite(support):
            if abs(closes[i] - support) / support <= 0.001 or lows[i] <= support * 1.0005:
                if closes[i] > opens[i] and lower >= wick_ratio * body:
                    direction = "BUY"
        if direction is None:
            continue
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
    parser = argparse.ArgumentParser(description="Refinamento de zonas de toque de corpo")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_body_touch_zones_refined.json")
    parser.add_argument("--lookback", type=int, default=60)
    parser.add_argument("--tolerance", type=float, default=0.0005)
    parser.add_argument("--min-touches", type=int, default=2)
    parser.add_argument("--wick-ratio", type=float, default=1.2)
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        rows = evaluate(_load(path), args.lookback, args.tolerance, args.min_touches, args.wick_ratio, args.max_gales)
        split = int(len(rows) * 0.8)
        results.append({"symbol": path.stem, "train": _metrics(rows[:split]), "test": _metrics(rows[split:]), "observations": rows})
    all_rows = [row for item in results for row in item["observations"]]
    split = int(len(all_rows) * 0.8)
    output = {"schema": "mercury.m5.body-touch-zones-refined.v1", "params": {"lookback": args.lookback, "tolerance": args.tolerance, "min_touches": args.min_touches, "wick_ratio": args.wick_ratio, "max_gales": args.max_gales}, "aggregate": {"train": _metrics(all_rows[:split]), "test": _metrics(all_rows[split:])}, "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": output["aggregate"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
