#!/usr/bin/env python3
"""Estudo temporal de filtros M5 sem lookahead e sem otimizar no teste."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def _features(frame: pd.DataFrame) -> pd.DataFrame:
    columns = {str(column).lower(): column for column in frame.columns}
    data = frame.rename(columns={value: key for key, value in columns.items()}).copy()
    data = data.rename(columns={"open": "Open", "high": "High", "low": "Low", "close": "Close"})
    data = data.sort_index()
    open_ = data["Open"].astype(float)
    high = data["High"].astype(float)
    low = data["Low"].astype(float)
    close = data["Close"].astype(float)
    direction = np.where(close > open_, "BUY", np.where(close < open_, "SELL", "WAIT"))
    body = (close - open_).abs()
    candle_range = (high - low).where(lambda value: value > 0)
    upper_wick = high - np.maximum(open_, close)
    lower_wick = np.minimum(open_, close) - low
    true_range = pd.concat([high - low, (high - close.shift()).abs(), (low - close.shift()).abs()], axis=1).max(axis=1)
    atr = true_range.rolling(14).mean()
    ema = close.ewm(span=200, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    rsi = (100 - 100 / (1 + gain / loss.replace(0, np.nan))).fillna(50.0)
    next_open = open_.shift(-1)
    next_close = close.shift(-1)
    outcome = np.where(direction == "BUY", next_close > next_open,
                       np.where(direction == "SELL", next_close < next_open, False))
    result = pd.DataFrame(index=data.index)
    result["direction"] = direction
    result["outcome"] = outcome
    result["valid"] = (direction != "WAIT") & next_open.notna() & next_close.notna()
    result["body25"] = body.div(candle_range) >= 0.25
    result["body40"] = body.div(candle_range) >= 0.40
    result["range_atr2"] = candle_range.div(atr) <= 2.0
    result["ema_aligned"] = ((direction == "BUY") & (close > ema)) | ((direction == "SELL") & (close < ema))
    result["rsi_context"] = ((direction == "BUY") & rsi.between(50, 70)) | ((direction == "SELL") & rsi.between(30, 50))
    result["wick_rejection"] = ((direction == "BUY") & (lower_wick >= 2 * body)) | ((direction == "SELL") & (upper_wick >= 2 * body))
    previous = pd.Series(direction, index=data.index).shift(1)
    result["previous_aligned"] = ((direction == "BUY") & (previous == "BUY")) | ((direction == "SELL") & (previous == "SELL"))
    result["reversal_context"] = ((direction == "BUY") & (previous == "SELL") & (lower_wick >= 2 * body)) | ((direction == "SELL") & (previous == "BUY") & (upper_wick >= 2 * body))
    result = result.iloc[200:-1]
    return result


def _metrics(frame: pd.DataFrame, mask: pd.Series) -> dict:
    selected = frame[frame["valid"] & mask]
    wins = int(selected["outcome"].sum())
    total = len(selected)
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Estudo de candidatos M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_candidate_study.json")
    args = parser.parse_args()
    rows = []
    candidates = {
        "baseline": lambda d: d["valid"],
        "body25": lambda d: d["body25"],
        "body40": lambda d: d["body40"],
        "range_atr2": lambda d: d["range_atr2"],
        "ema_aligned": lambda d: d["ema_aligned"],
        "rsi_context": lambda d: d["rsi_context"],
        "wick_rejection": lambda d: d["wick_rejection"],
        "previous_aligned": lambda d: d["previous_aligned"],
        "reversal_context": lambda d: d["reversal_context"],
        "body25_ema": lambda d: d["body25"] & d["ema_aligned"],
        "body25_wick": lambda d: d["body25"] & d["wick_rejection"],
        "body25_reversal": lambda d: d["body25"] & d["reversal_context"],
        "body25_ema_rsi": lambda d: d["body25"] & d["ema_aligned"] & d["rsi_context"],
        "body25_wick_ema": lambda d: d["body25"] & d["wick_rejection"] & d["ema_aligned"],
    }
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        features = _features(pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"]))
        n = len(features)
        train_end, validation_end = int(n * 0.60), int(n * 0.80)
        for name, builder in candidates.items():
            mask = builder(features)
            rows.append({"symbol": path.stem, "candidate": name,
                         "train": _metrics(features.iloc[:train_end], mask.iloc[:train_end]),
                         "validation": _metrics(features.iloc[train_end:validation_end], mask.iloc[train_end:validation_end]),
                         "test": _metrics(features.iloc[validation_end:], mask.iloc[validation_end:])})
    output = {"schema": "mercury.m5.candidate-study.v1", "candidates": rows}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = []
    for name in candidates:
        part = [row["test"] for row in rows if row["candidate"] == name]
        signals = sum(item["signals"] for item in part)
        wins = sum(item["wins"] for item in part)
        summary.append({"candidate": name, "signals": signals, "wins": wins,
                        "hit_rate": wins / signals if signals else None,
                        "net_payout_080": sum(item["net_payout_080"] for item in part)})
    summary.sort(key=lambda item: (item["hit_rate"] or -1, item["signals"]), reverse=True)
    print(json.dumps({"output": str(args.out), "test_summary": summary}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
