#!/usr/bin/env python3
"""Coleta probe M1 curto para testar entradas intrabar em velas M5."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mercury_ai.config.universe import ALL_SYMBOLS


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe M1 intrabar")
    parser.add_argument("--out-dir", type=Path, default=ROOT / "data" / "validation_m1_probe")
    parser.add_argument("--limit", type=int, default=38)
    parser.add_argument("--period", default="7d")
    args = parser.parse_args()
    args.out_dir = args.out_dir.resolve()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    records = []
    for symbol in ALL_SYMBOLS[:args.limit]:
        try:
            frame = yf.Ticker(symbol).history(period=args.period, interval="1m", auto_adjust=False, actions=False)
            if frame is None or frame.empty:
                raise ValueError("empty")
            if isinstance(frame.columns, pd.MultiIndex):
                frame.columns = [str(column[0]) for column in frame.columns]
            frame.columns = [str(column).lower() for column in frame.columns]
            frame = frame[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric, errors="coerce").dropna()
            frame.index = pd.to_datetime(frame.index, utc=True)
            target = args.out_dir / f"{symbol.replace('=', '_').replace('-', '_')}_1m.csv"
            frame.to_csv(target, index_label="timestamp")
            records.append({"symbol": symbol, "status": "OK", "rows": len(frame), "file": str(target.relative_to(ROOT)).replace("\\", "/")})
            print(f"{symbol}: {len(frame)}", flush=True)
        except Exception as exc:
            records.append({"symbol": symbol, "status": "ERROR", "error": str(exc)})
            print(f"{symbol}: ERROR {exc}", flush=True)
    (args.out_dir / "manifest.json").write_text(json.dumps({"interval": "1m", "period": args.period, "records": records}, indent=2), encoding="utf-8")
    return 0 if any(row["status"] == "OK" for row in records) else 2


if __name__ == "__main__":
    raise SystemExit(main())
