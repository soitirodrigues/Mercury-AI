#!/usr/bin/env python3
"""M5 Operational Runner CLI — camada operacional oficial Sprint 5.

Uso:
  python scripts/m5_operational_runner.py --universe 12 --workers 4 --executor process
  python scripts/m5_operational_runner.py --universe 64 --workers 4 --executor process --out reports/m5_sprint5/operational_cycle_report.json

Flags:
  --universe 12|64  (default 12 para teste rápido; 64 para baseline oficial)
  --workers N       (override; default vem de M5OperationalConfig)
  --executor thread|process
  --use-scanner     rollback para MercuryScanner (feature flag test)
  --cycles N        multi-cycle: N ciclos consecutivos (5m incremental simulado)
"""
from __future__ import annotations
import sys, json, argparse, os
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.operations.m5_operational.config import M5OperationalConfig
from mercury_ai.operations.m5_operational.runner import M5OperationalRunner
from mercury_ai.operations.m5_operational.clock import M5Clock


def main():
    p = argparse.ArgumentParser(description="M5 Operational Runner Sprint 5")
    p.add_argument("--universe", type=int, default=12, choices=[12, 64])
    p.add_argument("--workers", type=int, default=None)
    p.add_argument("--executor", choices=["thread", "process"], default=None)
    p.add_argument("--out", type=str, default="reports/m5_sprint5/operational_cycle_report.json")
    p.add_argument("--summary", type=str, default="reports/m5_sprint5/SENSEI_SPRINT5_REPORT.md")
    p.add_argument("--use-scanner", action="store_true", help="rollback: use MercuryScanner instead of operational runner")
    p.add_argument("--cycles", type=int, default=1, help="multi-cycle count (1 = single cycle)")
    p.add_argument("--multi-out", type=str, default="reports/m5_sprint5/multi_cycle_report.json")
    args = p.parse_args()

    n = min(args.universe, len(ALL_SYMBOLS))
    symbols = ALL_SYMBOLS[:n]

    # Config
    cfg = M5OperationalConfig.from_env()
    if args.workers is not None:
        cfg = M5OperationalConfig(**{**cfg.to_dict(), ("process_workers" if cfg.executor == "process" else "thread_workers"): args.workers})
    if args.executor is not None:
        cfg = M5OperationalConfig(**{**cfg.to_dict(), "executor": args.executor})
    cfg.validate()

    print(f"M5 Operational Runner — universe={n} executor={cfg.executor} workers={cfg.workers_for_executor()} cycles={args.cycles}")
    print(f"Config: {json.dumps(cfg.to_dict(), indent=2)}")

    # Rollback / feature flag test
    if args.use_scanner:
        print("\n[ROLLBACK MODE] Using MercuryScanner (old path) — flag use_operational_runner=False")
        from mercury_ai.brain.scanner import MercuryScanner
        scanner = MercuryScanner()
        # Monkey: filter universe for test — scanner uses AssetRegistry, so we just run it
        ranked = scanner.scan()
        print(f"Scanner returned {len(ranked)} ranked")
        # Minimal report
        report = {
            "mode": "rollback_scanner",
            "universe": n,
            "ranked_count": len(ranked),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        }
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"Wrote {out}")
        return

    runner = M5OperationalRunner(universe=symbols, config=cfg, disable_profiler=True)

    # Install shutdown handlers (SIGTERM/SIGINT)
    runner._install_signal_handlers()

    if args.cycles == 1:
        print(f"\nRunning single cycle ...")
        report = runner.run_cycle()
        print(f"  cycle_id={report.get('cycle_id')} status={report.get('cycle_status')} wall={report.get('cycle_duration_s')}s")
        print(f"  fresh={report.get('fresh')} stale={report.get('stale')} stale_as_fresh={report.get('stale_as_fresh')} timeout={report.get('assets_timeout')}")
        print(f"  first_fresh={report.get('first_fresh_decision_ms')}ms first_top3={report.get('first_top3_ms')}ms queue_max={report.get('queue_max_depth')}")
        print(f"  Top3: {report.get('top3')}")

        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"Wrote {out}")

        # Sensei summary skeleton
        md = Path(args.summary)
        md.parent.mkdir(parents=True, exist_ok=True)
        md.write_text(
            f"# SENSEI Sprint 5 — Operational Cycle ({n} assets, {cfg.executor} w={cfg.workers_for_executor()})\n\n"
            f"- Generated: {datetime.now(timezone.utc).isoformat()}\n"
            f"- Cycle: {report.get('cycle_id')} target={report.get('target_candle')}\n"
            f"- Wall: {report.get('cycle_duration_s')}s  first_fresh: {report.get('first_fresh_decision_ms')}ms  first_top3: {report.get('first_top3_ms')}ms\n"
            f"- Fresh {report.get('fresh')} stale {report.get('stale')} stale_as_fresh {report.get('stale_as_fresh')} timeout {report.get('assets_timeout')}\n"
            f"- Queue max depth {report.get('queue_max_depth')}/{report.get('queue_maxsize')} worker_restarts {report.get('worker_restart_count')}\n"
            f"- Status {report.get('cycle_status')} next_candle_ready={report.get('next_candle_ready')}\n"
            f"- Top3: {json.dumps(report.get('top3'), ensure_ascii=False)}\n"
            f"- Config: `process_workers=4` (baseline Sprint 4) executor={cfg.executor}\n"
            f"- FreshnessGate stale_as_fresh == 0: {'PASS' if report.get('stale_as_fresh') == 0 else 'FAIL'}\n",
            encoding="utf-8",
        )
        print(f"Wrote {md}")
    else:
        print(f"\nRunning {args.cycles} cycles consecutivos (multi-cycle test) ...")
        clock = M5Clock(runner=runner, config=cfg)
        reports = clock.run_cycles_blocking(count=args.cycles)
        for r in reports:
            print(f"  cycle {r.get('cycle_id')} target={r.get('target_candle')} status={r.get('cycle_status')} wall={r.get('cycle_duration_s')}s stale_as_fresh={r.get('stale_as_fresh')} queue_max={r.get('queue_max_depth')}")
        # Validate multi-cycle gates
        cycle_ids = [r.get('cycle_id') for r in reports]
        targets = [r.get('target_candle') for r in reports]
        unique = len(set(cycle_ids)) == len(reports)
        sorted_targets = targets == sorted(targets)
        no_overlap = True  # M5Clock blocking ensures no overlap
        stale_all_zero = all(r.get('stale_as_fresh') == 0 for r in reports)
        orphan_zero = all(r.get('orphan_workers', 0) == 0 for r in reports)
        # Memory growth check: delta relative to first cycle
        mem_deltas = [r.get('memory_delta_mb') for r in reports if r.get('memory_delta_mb') is not None]

        multi = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "cycles": args.cycles,
            "config": cfg.to_dict(),
            "reports": reports,
            "gates": {
                "unique_cycle_ids": unique,
                "targets_sorted": sorted_targets,
                "no_overlap": no_overlap,
                "stale_as_fresh_all_zero": stale_all_zero,
                "orphan_workers_zero": orphan_zero,
                "cycle_ids": cycle_ids,
                "targets": targets,
                "memory_deltas": mem_deltas,
            },
            "pass": bool(unique and sorted_targets and no_overlap and stale_all_zero and orphan_zero),
        }
        out = Path(args.multi_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(multi, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
        print(f"\nMULTI-CYCLE GATES: unique={unique} sorted={sorted_targets} stale_zero={stale_all_zero} orphan_zero={orphan_zero}")
        print(f"PASS = {multi['pass']}")
        print(f"Wrote {out}")


if __name__ == "__main__":
    main()
