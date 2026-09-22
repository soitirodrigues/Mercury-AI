#!/usr/bin/env python3
"""Filtros de qualidade sobre o sinal de zona de toque de corpo (sem gale)."""
from __future__ import annotations

import argparse
import itertools
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


def evaluate(frame: pd.DataFrame, lookback: int = 60, tolerance: float = 0.0005) -> pd.DataFrame:
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    n = len(frame)
    opens, closes, highs, lows = open_.to_numpy(), close.to_numpy(), high.to_numpy(), low.to_numpy()
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean().to_numpy()
    zone_sup = np.full(n, np.nan)
    zone_res = np.full(n, np.nan)
    zone_touches = np.zeros(n)
    for i in range(lookback, n):
        bodies = np.concatenate([opens[i - lookback:i], closes[i - lookback:i]])
        sorted_b = np.sort(bodies)
        clusters = []
        cluster = [sorted_b[0]]
        for price in sorted_b[1:]:
            if abs(price - cluster[-1]) / cluster[-1] <= tolerance:
                cluster.append(price)
            else:
                if len(cluster) >= 2:
                    clusters.append((float(np.mean(cluster)), len(cluster)))
                cluster = [price]
        if len(cluster) >= 2:
            clusters.append((float(np.mean(cluster)), len(cluster)))
        current = closes[i]
        sup = [c for c in clusters if c[0] < current]
        res = [c for c in clusters if c[0] > current]
        if sup:
            best = max(sup, key=lambda c: c[0])
            zone_sup[i] = best[0]
            zone_touches[i] = best[1]
        if res:
            best = min(res, key=lambda c: c[0])
            zone_res[i] = best[0]
            zone_touches[i] = max(zone_touches[i], best[1])
    rows = []
    for i in range(lookback, n - 2):
        body = abs(closes[i] - opens[i])
        rng = highs[i] - lows[i]
        if rng <= 0 or not np.isfinite(atr[i]) or atr[i] <= 0:
            continue
        upper = highs[i] - max(opens[i], closes[i])
        lower = min(opens[i], closes[i]) - lows[i]
        direction = None
        if np.isfinite(zone_res[i]) and (abs(closes[i] - zone_res[i]) / zone_res[i] <= 0.001 or highs[i] >= zone_res[i] * 0.9995):
            if closes[i] < opens[i] and upper >= 1.2 * body:
                direction = "SELL"
        if direction is None and np.isfinite(zone_sup[i]) and (abs(closes[i] - zone_sup[i]) / zone_sup[i] <= 0.001 or lows[i] <= zone_sup[i] * 1.0005):
            if closes[i] > opens[i] and lower >= 1.2 * body:
                direction = "BUY"
        if direction is None:
            continue
        entry = opens[i + 1]
        exit_ = closes[i + 1]
        hit = exit_ > entry if direction == "BUY" else exit_ < entry
        prev_bull = closes[i - 1] > opens[i - 1]
        rows.append({
            "index": i,
            "direction": direction,
            "hit": bool(hit),
            "touches": int(zone_touches[i]),
            "wick_ratio": float((upper if direction == "SELL" else lower) / rng),
            "body_ratio": float(body / rng),
            "range_atr": float(rng / atr[i]),
            "hour": frame.index[i].hour,
            "prev_aligned": bool((direction == "SELL" and prev_bull) or (direction == "BUY" and not prev_bull)),
        })
    return pd.DataFrame(rows)


def _metrics(df: pd.DataFrame, mask: pd.Series) -> dict:
    sel = df[mask]
    total = len(sel)
    wins = int(sel["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Filtros de qualidade sobre zonas de toque")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_zone_quality_filters.json")
    args = parser.parse_args()
    frames = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        part = evaluate(_load(path))
        part["symbol"] = path.stem
        frames.append(part)
    data = pd.concat(frames, ignore_index=True)
    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    filters = {
        "base": lambda d: pd.Series(True, index=d.index),
        "touches3": lambda d: d["touches"] >= 3,
        "touches4": lambda d: d["touches"] >= 4,
        "wick40": lambda d: d["wick_ratio"] >= 0.40,
        "wick50": lambda d: d["wick_ratio"] >= 0.50,
        "body30": lambda d: d["body_ratio"] >= 0.30,
        "range_atr15": lambda d: d["range_atr"] <= 1.5,
        "range_atr10": lambda d: d["range_atr"] <= 1.0,
        "prev_aligned": lambda d: d["prev_aligned"],
        "london_ny": lambda d: d["hour"].between(7, 16),
    }
    rows = []
    for name, fn in filters.items():
        rows.append({"filter": name, "train": _metrics(train, fn(train)), "test": _metrics(test, fn(test))})
    combos = []
    for combo in itertools.combinations(["touches3", "wick40", "body30", "range_atr15", "prev_aligned", "london_ny"], 2):
        mask_train = pd.Series(True, index=train.index)
        mask_test = pd.Series(True, index=test.index)
        for name in combo:
            mask_train &= filters[name](train)
            mask_test &= filters[name](test)
        combos.append({"combo": list(combo), "train": _metrics(train, mask_train), "test": _metrics(test, mask_test)})
    combos.sort(key=lambda r: (r["test"]["hit_rate"] or 0, r["test"]["signals"]), reverse=True)
    output = {"schema": "mercury.m5.zone-quality-filters.v1", "base_signals": len(data),
              "single_filters": rows, "combos": combos[:20]}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "single_filters": rows, "top_combos": combos[:10]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
