#!/usr/bin/env python3
"""Probe de price action: Engolfo, Morning/Evening Star, Pin Bar."""
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


def evaluate(frame: pd.DataFrame, max_gales: int = 2) -> dict:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    results = {"engulfing": [], "star": [], "pinbar": []}
    for i in range(20, n - (max_gales + 2)):
        if not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0:
            continue
        upper = highs[i] - max(opens[i], closes[i])
        lower = min(opens[i], closes[i]) - lows[i]
        prev_body = abs(closes[i - 1] - opens[i - 1])
        prev2_body = abs(closes[i - 2] - opens[i - 2])
        trend_down = closes[i - 1] < closes[i - 5]
        trend_up = closes[i - 1] > closes[i - 5]

        # ENGOLFO
        if (closes[i - 1] < opens[i - 1] and closes[i] > opens[i]
                and closes[i] >= opens[i - 1] and opens[i] <= closes[i - 1] and trend_down):
            results["engulfing"].append((i, "BUY"))
        elif (closes[i - 1] > opens[i - 1] and closes[i] < opens[i]
              and closes[i] <= opens[i - 1] and opens[i] >= closes[i - 1] and trend_up):
            results["engulfing"].append((i, "SELL"))

        # MORNING/EVENING STAR
        if (prev2_body > 0.5 * atr[i] and prev_body < 0.3 * atr[i]
                and closes[i] > opens[i] and closes[i] > (opens[i - 2] + closes[i - 2]) / 2 and trend_down):
            results["star"].append((i, "BUY"))
        elif (prev2_body > 0.5 * atr[i] and prev_body < 0.3 * atr[i]
              and closes[i] < opens[i] and closes[i] < (opens[i - 2] + closes[i - 2]) / 2 and trend_up):
            results["star"].append((i, "SELL"))

        # PIN BAR
        if lower >= 2 * body and lower / rng >= 0.6 and trend_down:
            results["pinbar"].append((i, "BUY"))
        elif upper >= 2 * body and upper / rng >= 0.6 and trend_up:
            results["pinbar"].append((i, "SELL"))

    out = {}
    for name, rows in results.items():
        obs = []
        for i, direction in rows:
            outcomes = []
            for leg in range(1, max_gales + 2):
                entry = opens[i + leg]
                exit_ = closes[i + leg]
                hit = exit_ > entry if direction == "BUY" else exit_ < entry
                outcomes.append(bool(hit))
                if hit:
                    break
            obs.append({"index": int(i), "direction": direction, "outcomes": outcomes, "hit": bool(outcomes[-1])})
        out[name] = obs
    return out


def _metrics(rows: list[dict]) -> dict:
    total = len(rows)
    wins = sum(row["hit"] for row in rows)
    direct = sum(row["outcomes"][0] for row in rows)
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "direct_hit_rate": direct / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe price action M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_price_action_probe.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    all_results = {"engulfing": [], "star": [], "pinbar": []}
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        res = evaluate(_load(path), args.max_gales)
        for name in all_results:
            all_results[name].extend(res[name])
    summary = {}
    for name, rows in all_results.items():
        split = int(len(rows) * 0.8)
        summary[name] = {"train": _metrics(rows[:split]), "test": _metrics(rows[split:])}
    # Combinado: uniao dos tres
    combined = all_results["engulfing"] + all_results["star"] + all_results["pinbar"]
    split = int(len(combined) * 0.8)
    summary["combined"] = {"train": _metrics(combined[:split]), "test": _metrics(combined[split:])}
    output = {"schema": "mercury.m5.price-action.v1", "summary": summary}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
