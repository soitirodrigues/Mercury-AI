#!/usr/bin/env python3
"""Valida confluencia macro H1 + exaustao M5 sem lookahead."""
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
    close = frame["close"].astype(float)
    high = frame["high"].astype(float)
    low = frame["low"].astype(float)
    open_ = frame["open"].astype(float)
    frame["ema21"] = close.ewm(span=21, adjust=False).mean()
    frame["ema80"] = close.ewm(span=80, adjust=False).mean()
    delta = close.diff()
    gain = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False).mean()
    loss = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False).mean()
    frame["rsi"] = (100 - 100 / (1 + gain / loss.replace(0, np.nan))).fillna(50.0)
    mid = close.rolling(20).mean()
    std = close.rolling(20).std()
    frame["bb_upper"] = mid + 2 * std
    frame["bb_lower"] = mid - 2 * std
    frame["prior_high"] = high.rolling(48).max().shift(1)
    frame["prior_low"] = low.rolling(48).min().shift(1)
    frame["next_open"] = open_.shift(-1)
    frame["next_close"] = close.shift(-1)
    return frame.iloc[100:-1]


def _metrics(frame: pd.DataFrame, mask: pd.Series) -> dict:
    selected = frame[mask]
    total = len(selected)
    wins = int(selected["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def evaluate(frame: pd.DataFrame) -> list[dict]:
    frame = frame.copy()
    trend_up = frame["ema21"] > frame["ema80"]
    trend_down = frame["ema21"] < frame["ema80"]
    buy_exhaustion = (frame["rsi"] < 30) & (frame["close"] <= frame["bb_lower"]) & (frame["low"] <= frame["prior_low"] * 1.001)
    sell_exhaustion = (frame["rsi"] > 70) & (frame["close"] >= frame["bb_upper"]) & (frame["high"] >= frame["prior_high"] * 0.999)
    frame["direction"] = np.select(
        [trend_up & buy_exhaustion, trend_down & sell_exhaustion],
        ["BUY", "SELL"],
        default="WAIT",
    )
    frame["hit"] = np.where(frame["direction"] == "BUY", frame["next_close"] > frame["next_open"],
                            np.where(frame["direction"] == "SELL", frame["next_close"] < frame["next_open"], False))
    candidates = {
        "macro_exhaustion": frame["direction"] != "WAIT",
        "macro_rsi_only": (trend_up & (frame["rsi"] < 30)) | (trend_down & (frame["rsi"] > 70)),
        "macro_bollinger_only": (trend_up & (frame["close"] <= frame["bb_lower"])) | (trend_down & (frame["close"] >= frame["bb_upper"])),
        "macro_sr_only": (trend_up & (frame["low"] <= frame["prior_low"] * 1.001)) | (trend_down & (frame["high"] >= frame["prior_high"] * 0.999)),
    }
    split = int(len(frame) * 0.8)
    train, test = frame.iloc[:split], frame.iloc[split:]
    return [{"candidate": name, "train": _metrics(train, mask.iloc[:split]), "test": _metrics(test, mask.iloc[split:])}
            for name, mask in candidates.items()]


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe macro H1 + exaustao M5")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_macro_confluence_probe.json")
    args = parser.parse_args()
    results = []
    for path in sorted(args.data_dir.glob("*_5m.csv")):
        frame = _load(path)
        results.append({"symbol": path.stem, "candles": len(frame), "candidates": evaluate(frame)})
    output = {"schema": "mercury.m5.macro-confluence.v1", "timing_filter": "NOT_TESTABLE_ON_CLOSED_M5", "results": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
