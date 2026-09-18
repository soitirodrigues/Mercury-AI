#!/usr/bin/env python3
"""Executa o walk-forward M5 em todos os CSVs de um manifesto."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.signals.m5_walk_forward import evaluate_walk_forward


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida o filtro SMC em lote")
    parser.add_argument("--data-dir", type=Path, default=ROOT / "data" / "validation_m5")
    parser.add_argument("--out", type=Path, default=ROOT / "reports" / "m5_validation_batch.json")
    parser.add_argument("--min-history", type=int, default=60)
    parser.add_argument("--horizon", type=int, default=1)
    parser.add_argument("--payout", type=float, default=0.80)
    parser.add_argument("--cost", type=float, default=0.0)
    parser.add_argument("--max-candles", type=int, default=2000,
                        help="Usa somente os candles mais recentes por ativo")
    args = parser.parse_args()
    args.data_dir = args.data_dir.resolve()
    args.out = args.out.resolve()
    if args.max_candles < args.min_history + args.horizon + 1:
        raise SystemExit("max-candles deve comportar min-history + horizon")
    manifest_path = args.data_dir / "manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"manifesto nao encontrado: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    results = []
    for entry in manifest.get("records", []):
        if entry.get("status") != "OK" or not entry.get("file"):
            results.append({"symbol": entry.get("symbol"), "status": "SKIPPED", "reason": entry.get("error")})
            continue
        path = ROOT / entry["file"]
        try:
            frame = pd.read_csv(path, index_col="timestamp", parse_dates=["timestamp"])
            if len(frame) > args.max_candles:
                frame = frame.iloc[-args.max_candles:].copy()
            report = evaluate_walk_forward(
                frame,
                min_history=args.min_history,
                horizon=args.horizon,
                payout=args.payout,
                cost=args.cost,
            )
            results.append({
                "symbol": entry["symbol"],
                "status": "OK",
                "rows": len(frame),
                "overall": report["overall"],
                "splits": report["splits"],
            })
            print(
                f"{entry['symbol']}: signals={report['overall']['signals']} "
                f"hit={report['overall']['hit_rate']} "
                f"test_hit={report['splits']['test']['hit_rate']}",
                flush=True,
            )
        except Exception as exc:
            results.append({"symbol": entry.get("symbol"), "status": "ERROR", "error": f"{type(exc).__name__}: {exc}"})
            print(f"{entry.get('symbol')}: ERROR {exc}", flush=True)

    valid = [row for row in results if row.get("status") == "OK"]
    aggregate = {
        "assets": len(results),
        "assets_ok": len(valid),
        "assets_with_signals": sum(row["overall"]["signals"] > 0 for row in valid),
        "signals": sum(row["overall"]["signals"] for row in valid),
        "wins": sum(row["overall"]["wins"] for row in valid),
        "net_result": sum(row["overall"]["net_result"] for row in valid),
    }
    aggregate["hit_rate"] = aggregate["wins"] / aggregate["signals"] if aggregate["signals"] else None
    output = {
        "schema": "mercury.m5.validation.batch.v1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_manifest": str(manifest_path.relative_to(ROOT)).replace("\\", "/"),
        "parameters": {
            "min_history": args.min_history,
            "horizon": args.horizon,
            "payout": args.payout,
            "cost": args.cost,
            "max_candles": args.max_candles,
        },
        "aggregate": aggregate,
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"output": str(args.out), "aggregate": aggregate}, indent=2, ensure_ascii=False))
    return 0 if aggregate["signals"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
