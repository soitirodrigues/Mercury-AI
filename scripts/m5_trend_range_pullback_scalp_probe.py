#!/usr/bin/env python3
"""Probe: trend following, range trading, pullback, scalping."""
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
    ema21 = close.ewm(span=21, adjust=False).mean().to_numpy()
    ema80 = close.ewm(span=80, adjust=False).mean().to_numpy()
    results = {"trend": [], "range": [], "pullback": [], "scalp": []}
    for i in range(80, n - (max_gales + 2)):
        if not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0:
            continue
        trend_up = ema21[i] > ema80[i]
        trend_down = ema21[i] < ema80[i]
        # TREND: vela a favor da tendencia EMA21/80
        if trend_up and closes[i] > opens[i]:
            results["trend"].append((i, "BUY"))
        elif trend_down and closes[i] < opens[i]:
            results["trend"].append((i, "SELL"))
        # RANGE: preco entre suporte/resistencia de 48 velas, sem tendencia
        if not trend_up and not trend_down:
            sup = lows[i - 48:i].min()
            res = highs[i - 48:i].max()
            if closes[i] <= sup * 1.002 and closes[i] > opens[i]:
                results["range"].append((i, "BUY"))
            elif closes[i] >= res * 0.998 and closes[i] < opens[i]:
                results["range"].append((i, "SELL"))
        # PULLBACK: tendencia + retracao contra + retomada
        if trend_up and closes[i - 1] < opens[i - 1] and closes[i] > opens[i] and closes[i] > closes[i - 1]:
            results["pullback"].append((i, "BUY"))
        elif trend_down and closes[i - 1] > opens[i - 1] and closes[i] < opens[i] and closes[i] < closes[i - 1]:
            results["pullback"].append((i, "SELL"))
        # SCALP: range pequeno, corpo pequeno, direcao da vela
        if rng < 0.5 * atr[i] and body / rng >= 0.5:
            if closes[i] > opens[i]:
                results["scalp"].append((i, "BUY"))
            elif closes[i] < opens[i]:
                results["scalp"].append((i, "SELL"))
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
    parser = argparse.ArgumentParser(description="Probe trend/range/pullback/scalp M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_trend_range_pullback_scalp.json")
    parser.add_argument("--max-gales", type=int, default=2)
    args = parser.parse_args()
    all_results = {"trend": [], "range": [], "pullback": [], "scalp": []}
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        res = evaluate(_load(path), args.max_gales)
        for name in all_results:
            all_results[name].extend(res[name])
    summary = {}
    for name, rows in all_results.items():
        split = int(len(rows) * 0.8)
        summary[name] = {"train": _metrics(rows[:split]), "test": _metrics(rows[split:])}
    combined = all_results["trend"] + all_results["range"] + all_results["pullback"] + all_results["scalp"]
    split = int(len(combined) * 0.8)
    summary["combined"] = {"train": _metrics(combined[:split]), "test": _metrics(combined[split:])}
    output = {"schema": "mercury.m5.trend-range-pullback-scalp.v1", "summary": summary}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
