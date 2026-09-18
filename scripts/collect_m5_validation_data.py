#!/usr/bin/env python3
"""Coleta candles M5 do universo oficial e grava manifesto auditavel."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _normalise_history(history: pd.DataFrame) -> pd.DataFrame:
    if history is None or history.empty:
        return pd.DataFrame()
    frame = history.copy()
    if isinstance(frame.columns, pd.MultiIndex):
        frame.columns = [str(column[0]) for column in frame.columns]
    frame.columns = [str(column).lower() for column in frame.columns]
    required = {"open", "high", "low", "close", "volume"}
    if not required.issubset(frame.columns):
        return pd.DataFrame()
    frame = frame[["open", "high", "low", "close", "volume"]]
    frame = frame.apply(pd.to_numeric, errors="coerce").dropna()
    if not isinstance(frame.index, pd.DatetimeIndex):
        frame.index = pd.to_datetime(frame.index, utc=True)
    elif frame.index.tz is None:
        frame.index = frame.index.tz_localize("UTC")
    else:
        frame.index = frame.index.tz_convert("UTC")
    frame = frame[~frame.index.duplicated(keep="last")].sort_index()
    return frame


def _collect(symbol: str, period: str, retries: int) -> tuple[pd.DataFrame, str | None]:
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            history = yf.Ticker(symbol).history(
                period=period,
                interval="5m",
                auto_adjust=False,
                actions=False,
            )
            frame = _normalise_history(history)
            if frame.empty:
                last_error = "empty_or_invalid_ohlcv"
            else:
                return frame, None
        except Exception as exc:
            last_error = f"{type(exc).__name__}: {exc}"
        if attempt < retries:
            time.sleep(min(2 ** (attempt - 1), 8))
    return pd.DataFrame(), last_error or "unknown_collection_error"


def main() -> int:
    parser = argparse.ArgumentParser(description="Coleta dados M5 oficiais para walk-forward")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--period", default="60d", help="Periodo aceito pelo Yahoo para M5")
    parser.add_argument("--limit", type=int, default=None, help="Limita ativos para smoke test")
    parser.add_argument("--retries", type=int, default=3)
    parser.add_argument("--pause", type=float, default=0.25)
    args = parser.parse_args()
    if args.retries < 1 or args.pause < 0:
        raise SystemExit("retries deve ser >=1 e pause deve ser >=0")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    symbols = list(ALL_SYMBOLS[:args.limit] if args.limit else ALL_SYMBOLS)
    started = datetime.now(timezone.utc)
    records = []
    for position, symbol in enumerate(symbols, start=1):
        print(f"[{position}/{len(symbols)}] {symbol}", flush=True)
        frame, error = _collect(symbol, args.period, args.retries)
        record = {
            "symbol": symbol,
            "status": "OK" if not frame.empty else "ERROR",
            "rows": int(len(frame)),
            "first_timestamp": frame.index[0].isoformat() if not frame.empty else None,
            "last_timestamp": frame.index[-1].isoformat() if not frame.empty else None,
            "error": error,
            "file": None,
            "sha256": None,
        }
        if not frame.empty:
            target = args.out_dir / f"{symbol.replace('=', '_').replace('-', '_')}_5m.csv"
            temp = target.with_suffix(".tmp")
            frame.to_csv(temp, index_label="timestamp")
            temp.replace(target)
            record["file"] = str(target.relative_to(ROOT)).replace("\\", "/")
            record["sha256"] = _sha256(target)
        records.append(record)
        if args.pause:
            time.sleep(args.pause)

    manifest = {
        "schema": "mercury.m5.validation.v1",
        "source": "Yahoo Finance via yfinance",
        "interval": "5m",
        "requested_period": args.period,
        "started_at": started.isoformat(),
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "universe_requested": len(symbols),
        "assets_ok": sum(record["status"] == "OK" for record in records),
        "assets_error": sum(record["status"] != "OK" for record in records),
        "records": records,
    }
    manifest_path = args.out_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({
        "manifest": str(manifest_path),
        "assets_ok": manifest["assets_ok"],
        "assets_error": manifest["assets_error"],
    }, indent=2, ensure_ascii=False))
    return 0 if manifest["assets_ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
