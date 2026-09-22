#!/usr/bin/env python3
"""Coleta candles M1 e trades agregados publicos da Binance."""
from __future__ import annotations

import argparse
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://api.binance.com/api/v3"


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _get(path: str, params: dict) -> list:
    last_error = None
    for attempt in range(4):
        try:
            response = requests.get(f"{BASE}{path}", params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            time.sleep(min(2 ** attempt, 8))
    raise last_error


def collect_klines(symbol: str, minutes: int) -> pd.DataFrame:
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = end - minutes * 60_000
    rows = []
    cursor = start
    while cursor < end:
        batch = _get("/klines", {"symbol": symbol, "interval": "1m", "startTime": cursor, "endTime": end, "limit": 1000})
        if not batch:
            break
        rows.extend(batch)
        cursor = int(batch[-1][6]) + 1
        if len(batch) < 1000:
            break
        time.sleep(0.05)
    frame = pd.DataFrame(rows, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "trades", "taker_buy_volume", "taker_buy_quote_volume", "ignore"])
    if frame.empty:
        return frame
    frame["timestamp"] = pd.to_datetime(frame["open_time"].astype("int64"), unit="ms", utc=True)
    numeric = ["open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume", "taker_buy_quote_volume"]
    frame[numeric] = frame[numeric].astype(float)
    frame["trades"] = frame["trades"].astype(int)
    return frame.set_index("timestamp")[["open", "high", "low", "close", "volume", "quote_volume", "trades", "taker_buy_volume", "taker_buy_quote_volume"]]


def collect_trades(symbol: str, minutes: int) -> pd.DataFrame:
    end = int(datetime.now(timezone.utc).timestamp() * 1000)
    start = end - minutes * 60_000
    rows = []
    cursor = start
    while cursor < end:
        batch = _get("/aggTrades", {"symbol": symbol, "startTime": cursor, "endTime": end, "limit": 1000})
        if not batch:
            break
        rows.extend(batch)
        cursor = int(batch[-1]["T"]) + 1
        if len(batch) < 1000:
            break
        time.sleep(0.05)
    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame
    frame["timestamp"] = pd.to_datetime(frame["T"].astype("int64"), unit="ms", utc=True)
    frame["price"] = frame["p"].astype(float)
    frame["quantity"] = frame["q"].astype(float)
    frame["is_buyer_maker"] = frame["m"].astype(bool)
    return frame.set_index("timestamp")[["a", "price", "quantity", "is_buyer_maker"]]


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta order flow publico Binance")
    parser.add_argument("--symbols", nargs="+", default=["BTCUSDT", "ETHUSDT"])
    parser.add_argument("--minutes", type=int, default=720)
    parser.add_argument("--out-dir", type=Path, default=ROOT / "data" / "orderflow_binance")
    args = parser.parse_args()
    args.out_dir = args.out_dir.resolve()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for symbol in args.symbols:
        print(f"{symbol}: candles", flush=True)
        candles = collect_klines(symbol, args.minutes)
        print(f"{symbol}: trades", flush=True)
        trades = collect_trades(symbol, args.minutes)
        candle_path = args.out_dir / f"{symbol}_1m.csv"
        trade_path = args.out_dir / f"{symbol}_aggtrades.csv"
        candles.to_csv(candle_path)
        trades.to_csv(trade_path)
        records.append({
            "symbol": symbol,
            "candles": len(candles),
            "trades": len(trades),
            "candles_file": str(candle_path.relative_to(ROOT)).replace("\\", "/"),
            "trades_file": str(trade_path.relative_to(ROOT)).replace("\\", "/"),
            "candles_sha256": _sha256(candle_path),
            "trades_sha256": _sha256(trade_path),
        })
    manifest = {"schema": "mercury.orderflow.binance.v1", "source": "Binance public REST", "minutes": args.minutes, "records": records}
    (args.out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
