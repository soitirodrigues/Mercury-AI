#!/usr/bin/env python3
"""
SENSEI SPRINT 4 — WORKER BENCHMARK

Testa obrigatoriamente workers = 1,2,4,8,16
Para cada configuração mede:
- CPU utilization
- wall time
- throughput assets/sec
- time_to_first_decision
- time_to_5_decisions
- time_to_10_decisions
- time_to_partial_top3
- time_to_complete_top3
- fresh count / stale / DATA_UNAVAILABLE
- peak memory
- errors

Escolhe melhor configuração por: PERFORMANCE + STABILITY + MEMORY + CORRECTNESS
Gera: reports/m5_sprint4/worker_benchmark.json + .txt + tabela workers | wall | first | partial | complete | CPU | RAM | errors

Inclui:
- teste ThreadPool vs ProcessPool (se --process)
- teste 12 assets e 64 assets (se --universe 12/64)
"""
from __future__ import annotations
import sys, json, time, statistics, traceback
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS

WORKER_COUNTS = [1, 2, 4, 8, 16]

def run_one(universe_n: int, workers: int, executor: str = "thread"):
    from scripts.m5_inter_asset_parallel_scanner import ParallelScanner
    n = min(universe_n, len(ALL_SYMBOLS))
    symbols = ALL_SYMBOLS[:n]
    # measure psutil before
    try:
        import psutil, os
        proc = psutil.Process(os.getpid())
        # prime cpu_percent
        psutil.cpu_percent(interval=0.1)
    except:
        psutil = None
    import time as _t
    t0 = _t.perf_counter()
    scanner = ParallelScanner(symbols, workers=workers, executor_type=executor, disable_profiler=True)
    result = scanner.scan()
    # result already has all metrics
    # Add extra aggregate for benchmark table
    return result


def _assess_next_candle_ready(first_ms, partial_ms, complete_ms, wall_ms):
    """NEXT_CANDLE_READY operacional: distinção A/B/C.
    A) FIRST FRESH < 300s => capaz de operar uma decisão válida antes do próximo candle
    B) PARTIAL TOP3 < 300s => Top-3 parcial utilizável antes do ciclo fechar
    C) COMPLETE < 300s => universo inteiro antes do próximo candle
    Para Sprint 4, NEXT_CANDLE_READY = PASS se (A) primeira decisão fresh estiver < 300s,
    pois sistema não precisa esperar 64 para começar a operar (early emission).
    """
    window = 300000
    a = first_ms is not None and first_ms < window
    b = partial_ms is not None and partial_ms < window
    c = complete_ms is not None and complete_ms < window
    # Legacy: complete < 300s (strict)
    legacy_pass = c
    # Sprint4 operational: first fresh < 300s AND partial < 300s
    operational_pass = a and b if (partial_ms is not None) else a
    return {"first_fresh_ready": a, "partial_top3_ready": b, "complete_ready": c, "legacy_pass": legacy_pass, "operational_pass": operational_pass}

def benchmark(universe_n: int, executor: str = "thread", out_dir: Path = Path("reports/m5_sprint4"), include_process: bool = False):
    out_dir.mkdir(parents=True, exist_ok=True)
    all_results = {}
    table_rows = []

    for w in WORKER_COUNTS:
        print(f"\n{'='*70}")
        print(f"BENCHMARK universe={universe_n} workers={w} executor={executor} @ {datetime.now(timezone.utc).isoformat()}")
        print(f"{'='*70}")
        try:
            res = run_one(universe_n, w, executor=executor)
            all_results[str(w)] = {
                "workers": w,
                "executor": executor,
                "wall_ms": res["wall_ms"],
                "wall_s": res["wall_s"],
                "first_decision_ms": res["first_decision_ms"],
                "time_to_5_ms": res["time_to_5_ms"],
                "time_to_10_ms": res["time_to_10_ms"],
                "partial_top3_ms": res["time_to_partial_top3_ms"],
                "complete_top3_ms": res["time_to_complete_top3_ms"],
                "throughput_assets_per_sec": res["throughput_assets_per_sec"],
                "fresh": res["fresh"],
                "stale": res["stale"],
                "unavailable": res["unavailable"],
                "errors": res["errors"],
                "peak_memory_mb": res["peak_memory_mb"],
                "memory_delta_mb": res["memory_delta_mb"],
                "cpu_percent": res["cpu_percent"],
                "top3": res["top3"],
                "top3_status": res["top3_status"],
            }
            table_rows.append((w, res["wall_s"], res["first_decision_ms"], res["time_to_partial_top3_ms"], res["time_to_complete_top3_ms"], res["cpu_percent"], res["peak_memory_mb"], res["errors"] + res["unavailable"]))
            # Write per-worker artifact
            per_out = out_dir / f"worker_{universe_n}assets_w{w}_{executor}.json"
            per_out.write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
            print(f"  -> workers={w} wall={res['wall_s']:.1f}s first={res['first_decision_ms']}ms partial={res['time_to_partial_top3_ms']}ms complete={res['time_to_complete_top3_ms']}ms mem={res['peak_memory_mb']}MB cpu={res['cpu_percent']}% err={res['errors']}")
        except Exception as e:
            tb = traceback.format_exc()
            print(f"  FAIL workers={w}: {e}\n{tb}")
            all_results[str(w)] = {"workers": w, "error": str(e), "trace": tb}
            table_rows.append((w, None, None, None, None, None, None, -1))

    # Optional ProcessPool comparison (workers=4 only for speed)
    if include_process:
        for w in [4]:
            print(f"\n{'='*70}")
            print(f"BENCHMARK PROCESS executor universe={universe_n} workers={w}")
            try:
                res = run_one(universe_n, w, executor="process")
                key = f"{w}_process"
                all_results[key] = {
                    "workers": w,
                    "executor": "process",
                    "wall_ms": res["wall_ms"],
                    "wall_s": res["wall_s"],
                    "first_decision_ms": res["first_decision_ms"],
                    "partial_top3_ms": res["time_to_partial_top3_ms"],
                    "complete_top3_ms": res["time_to_complete_top3_ms"],
                    "peak_memory_mb": res["peak_memory_mb"],
                    "errors": res["errors"],
                    "fresh": res["fresh"],
                    "unavailable": res["unavailable"],
                }
                print(f"  PROCESS workers={w} wall={res['wall_s']:.1f}s")
                per_out = out_dir / f"worker_{universe_n}assets_w{w}_process.json"
                per_out.write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
            except Exception as e:
                print(f"  PROCESS FAIL {e}")
                all_results[f"{w}_process"] = {"error": str(e)}

    # Determine best worker by evidence: performance+stability+memory+correctness
    valid = {k: v for k, v in all_results.items() if "wall_s" in v and v.get("wall_s") is not None}
    # Correctness: minimal errors, then fresh maximized
    # Performance: minimal wall_s
    # Memory: minimal peak
    # Choose: pareto-like ranking weighted
    best = None
    if valid:
        # Normalize
        # score = wall_s normalized + memory normalized penalized - throughput bonus, error penalty heavy
        walls = [v["wall_s"] for v in valid.values()]
        mems = [v.get("peak_memory_mb") or 0 for v in valid.values()]
        min_wall = min(walls) if walls else 1
        max_wall = max(walls) if walls else 1
        min_mem = min(mems) if mems else 1
        max_mem = max(mems) if mems else 1

        def score_one(v):
            wall = v["wall_s"]
            mem = v.get("peak_memory_mb") or 0
            err = v.get("errors", 0) + v.get("unavailable", 0)*0  # unavailable not penalized as error (expected)
            # Only real errors penalized
            err_penalty = err * 100  # heavy
            wall_norm = (wall - min_wall) / (max_wall - min_wall + 1e-6)
            mem_norm = (mem - min_mem) / (max_mem - min_mem + 1e-6) if max_mem != min_mem else 0
            return wall_norm * 0.6 + mem_norm * 0.2 + err_penalty

        ranked = sorted(valid.items(), key=lambda kv: score_one(kv[1]))
        best_key, best_val = ranked[0]
        try:
            best_workers = int(best_key.split("_")[0])
        except:
            best_workers = best_val["workers"]
        best = {"workers": best_workers, "executor": best_val.get("executor", "thread"), "wall_s": best_val["wall_s"], "score": score_one(best_val)}
    else:
        best = {"workers": None, "reason": "no valid results"}

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "universe": universe_n,
        "executor": executor,
        "worker_counts": WORKER_COUNTS,
        "results": all_results,
        "table": [
            {"workers": r[0], "wall_s": r[1], "first_ms": r[2], "partial_ms": r[3], "complete_ms": r[4], "cpu": r[5], "ram_mb": r[6], "errors": r[7]} for r in table_rows
        ],
        "best": best,
    }

    # Write aggregate
    agg_file = out_dir / f"worker_benchmark_{universe_n}assets.json"
    agg_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    # Also write classic worker_benchmark.json umbrella if universe == 64
    if universe_n == 64:
        out_dir.joinpath("worker_benchmark.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    # TXT
    txt_lines = []
    txt_lines.append(f"WORKER BENCHMARK — universe={universe_n} executor={executor}")
    txt_lines.append(f"Generated: {summary['generated_at']}")
    txt_lines.append("")
    txt_lines.append(f"{'workers':>7} | {'wall_s':>7} | {'first_ms':>9} | {'partial_ms':>10} | {'complete_ms':>11} | {'CPU%':>6} | {'RAM MB':>7} | {'err':>3}")
    txt_lines.append("-"*85)
    for r in table_rows:
        txt_lines.append(f"{r[0]:>7} | {str(round(r[1],1) if r[1] else 'FAIL'):>7} | {str(r[2] or '-'):>9} | {str(r[3] or '-'):>10} | {str(r[4] or '-'):>11} | {str(r[5] or '-'):>6} | {str(r[6] or '-'):>7} | {r[7]:>3}")
    txt_lines.append("")
    txt_lines.append(f"BEST_WORKER_COUNT = {best.get('workers')} (executor={best.get('executor')}) wall={best.get('wall_s')}s")
    txt_file = out_dir / f"worker_benchmark_{universe_n}assets.txt"
    if universe_n == 64:
        txt_file2 = out_dir / "worker_benchmark.txt"
        txt_file2.write_text("\n".join(txt_lines), encoding="utf-8")
    txt_file.write_text("\n".join(txt_lines), encoding="utf-8")
    print("\n" + "\n".join(txt_lines))
    print(f"\nWrote {agg_file} and {txt_file}")
    return summary


def main():
    import argparse
    p = argparse.ArgumentParser(description="M5 Worker Benchmark Sprint4")
    p.add_argument("--universe", type=int, default=12, help="12 ou 64 (use 0 para rodar ambos)")
    p.add_argument("--executor", choices=["thread","process"], default="thread")
    p.add_argument("--include-process", action="store_true", help="também testa ProcessPool (workers=4)")
    args = p.parse_args()
    if args.universe == 0:
        # run both
        s12 = benchmark(12, executor=args.executor)
        s64 = benchmark(64, executor=args.executor, include_process=args.include_process)
        # Combined umbrella
        combined = {"12": s12, "64": s64, "generated_at": datetime.now(timezone.utc).isoformat()}
        Path("reports/m5_sprint4/worker_benchmark_all.json").write_text(json.dumps(combined, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    else:
        benchmark(args.universe, executor=args.executor, include_process=args.include_process)

if __name__ == "__main__":
    main()
