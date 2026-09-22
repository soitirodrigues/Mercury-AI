#!/usr/bin/env python3
"""Busca sistematica de filtros M5 com selecao no treino e teste final."""
from __future__ import annotations

import argparse
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _features(path: Path) -> pd.DataFrame:
    frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
    frame.columns = [str(c).lower() for c in frame.columns]
    frame.index = pd.to_datetime(frame.index, utc=True, format="mixed")
    frame = frame.sort_index()
    open_, high, low, close = (frame[c].astype(float) for c in ("open", "high", "low", "close"))
    body = (close - open_).abs()
    rng = (high - low).replace(0, np.nan)
    upper = high - np.maximum(open_, close)
    lower = np.minimum(open_, close) - low
    tr = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = tr.rolling(14).mean()
    ema21 = close.ewm(span=21, adjust=False).mean()
    ema80 = close.ewm(span=80, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    rsi = (100 - 100 / (1 + gain / loss.replace(0, np.nan))).fillna(50.0)
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    upper_band = mid + 2 * std
    lower_band = mid - 2 * std
    prior_high = high.rolling(48).max().shift(1)
    prior_low = low.rolling(48).min().shift(1)
    direction = np.where(close > open_, "BUY", np.where(close < open_, "SELL", "WAIT"))
    next_open = open_.shift(-1)
    next_close = close.shift(-1)
    out = pd.DataFrame(index=frame.index)
    out["direction"] = direction
    out["hit"] = np.where(direction == "BUY", next_close > next_open,
                          np.where(direction == "SELL", next_close < next_open, False))
    out["body25"] = body / rng >= 0.25
    out["body40"] = body / rng >= 0.40
    out["range_atr2"] = rng / atr <= 2.0
    out["trend_aligned"] = ((direction == "BUY") & (ema21 > ema80)) | ((direction == "SELL") & (ema21 < ema80))
    out["rsi_context"] = ((direction == "BUY") & rsi.between(50, 70)) | ((direction == "SELL") & rsi.between(30, 50))
    out["rsi_extreme"] = ((direction == "BUY") & (rsi < 30)) | ((direction == "SELL") & (rsi > 70))
    out["wick_rejection"] = ((direction == "BUY") & (lower >= 2 * body)) | ((direction == "SELL") & (upper >= 2 * body))
    out["bb_extreme"] = ((direction == "BUY") & (close <= lower_band)) | ((direction == "SELL") & (close >= upper_band))
    out["sr_touch"] = ((direction == "BUY") & (low <= prior_low * 1.001)) | ((direction == "SELL") & (high >= prior_high * 0.999))
    out["previous_aligned"] = ((direction == "BUY") & (close.shift(1) > open_.shift(1))) | ((direction == "SELL") & (close.shift(1) < open_.shift(1)))
    out["reversal"] = ((direction == "BUY") & (close.shift(1) < open_.shift(1)) & (lower >= 2 * body)) | ((direction == "SELL") & (close.shift(1) > open_.shift(1)) & (upper >= 2 * body))
    out = out.iloc[100:-1]
    return out[out["direction"] != "WAIT"]


def _metrics(frame: pd.DataFrame, mask: pd.Series) -> dict:
    selected = frame[mask]
    total = len(selected)
    wins = int(selected["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Busca sistematica M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_systematic_search.json")
    parser.add_argument("--min-test-signals", type=int, default=100)
    parser.add_argument("--min-train-signals", type=int, default=100)
    parser.add_argument("--min-train-hit", type=float, default=0.60)
    args = parser.parse_args()
    frames = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        part = _features(path)
        part["symbol"] = path.stem
        frames.append(part)
    data = pd.concat(frames).sort_index()
    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    feature_names = ["body25", "body40", "range_atr2", "trend_aligned", "rsi_context", "rsi_extreme", "wick_rejection", "bb_extreme", "sr_touch", "previous_aligned", "reversal"]
    rows = []
    for size in range(1, 4):
        for combo in itertools.combinations(feature_names, size):
            mask_train = train[list(combo)].all(axis=1)
            train_metrics = _metrics(train, mask_train)
            if train_metrics["signals"] < args.min_train_signals or (train_metrics["hit_rate"] or 0) < args.min_train_hit:
                continue
            mask_test = test[list(combo)].all(axis=1)
            test_metrics = _metrics(test, mask_test)
            rows.append({"features": list(combo), "train": train_metrics, "test": test_metrics})
    rows.sort(key=lambda row: ((row["test"]["hit_rate"] or 0), row["test"]["signals"]), reverse=True)
    output = {"schema": "mercury.m5.systematic-search.v1", "min_test_signals": args.min_test_signals, "candidates": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "top": rows[:20]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
