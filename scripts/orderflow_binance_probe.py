#!/usr/bin/env python3
"""Avalia order flow Binance M1 sem lookahead e sem executar ordens."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def _load(symbol: str, data_dir: Path) -> pd.DataFrame:
    candles = pd.read_csv(data_dir / f"{symbol}_1m.csv", index_col="timestamp", parse_dates=["timestamp"])
    trades = pd.read_csv(data_dir / f"{symbol}_aggtrades.csv", index_col="timestamp", parse_dates=["timestamp"])
    candles.index = pd.to_datetime(candles.index, utc=True, format="mixed")
    trades.index = pd.to_datetime(trades.index, utc=True, format="mixed")
    trades["minute"] = trades.index.floor("min")
    trades["buy_volume"] = np.where(trades["is_buyer_maker"], 0.0, trades["quantity"])
    trades["sell_volume"] = np.where(trades["is_buyer_maker"], trades["quantity"], 0.0)
    flow = trades.groupby("minute").agg(
        buy_volume=("buy_volume", "sum"),
        sell_volume=("sell_volume", "sum"),
        trade_count=("quantity", "size"),
        flow_volume=("quantity", "sum"),
        vwap=("price", "mean"),
    )
    flow["delta"] = flow["buy_volume"] - flow["sell_volume"]
    flow["delta_ratio"] = flow["delta"] / flow["flow_volume"].replace(0, np.nan)
    frame = candles.join(flow, how="left").fillna({"buy_volume": 0.0, "sell_volume": 0.0, "trade_count": 0, "flow_volume": 0.0, "delta": 0.0})
    frame["next_open"] = frame["open"].shift(-1)
    frame["next_close"] = frame["close"].shift(-1)
    frame["next_hit_buy"] = frame["next_close"] > frame["next_open"]
    frame["next_hit_sell"] = frame["next_close"] < frame["next_open"]
    return frame.iloc[:-1]


def _metrics(frame: pd.DataFrame, mask: pd.Series) -> dict:
    selected = frame[mask]
    total = len(selected)
    wins = int(selected["hit"].sum()) if total else 0
    return {"signals": total, "wins": wins, "hit_rate": wins / total if total else None,
            "net_payout_080": wins * 0.8 - (total - wins)}


def evaluate(frame: pd.DataFrame) -> dict:
    frame = frame.copy()
    frame["direction"] = np.where(frame["delta"] > 0, "BUY", np.where(frame["delta"] < 0, "SELL", "WAIT"))
    frame["hit"] = np.where(frame["direction"] == "BUY", frame["next_hit_buy"],
                            np.where(frame["direction"] == "SELL", frame["next_hit_sell"], False))
    volume_median = frame["flow_volume"].median()
    candidates = {
        "delta_any": frame["direction"] != "WAIT",
        "delta_10pct": frame["delta_ratio"].abs() >= 0.10,
        "delta_20pct": frame["delta_ratio"].abs() >= 0.20,
        "delta_30pct": frame["delta_ratio"].abs() >= 0.30,
        "delta_20_volume_median": (frame["delta_ratio"].abs() >= 0.20) & (frame["flow_volume"] >= volume_median),
        "delta_30_volume_median": (frame["delta_ratio"].abs() >= 0.30) & (frame["flow_volume"] >= volume_median),
    }
    split = int(len(frame) * 0.8)
    train, test = frame.iloc[:split], frame.iloc[split:]
    rows = []
    for name, mask in candidates.items():
        rows.append({
            "candidate": name,
            "train": _metrics(train, mask.iloc[:split]),
            "test": _metrics(test, mask.iloc[split:]),
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe order flow Binance")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "orderflow_binance")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "orderflow_binance_probe.json")
    args = parser.parse_args()
    manifest = json.loads((args.data_dir / "manifest.json").read_text(encoding="utf-8"))
    results = []
    for record in manifest["records"]:
        symbol = record["symbol"]
        frame = _load(symbol, args.data_dir)
        results.append({"symbol": symbol, "candles": len(frame), "candidates": evaluate(frame)})
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"schema": "mercury.orderflow.probe.v1", "results": results}, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "results": results}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
