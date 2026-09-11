"""S33-E.4 — Benchmark instrumentado (SEM alterar produção).
Usa MercuryScanner.scan(workers=4) — caminho paralelo validado S33-E.3.
Canários 2/4/8/12 + 39. Yahoo REAL. Métricas T0-T4, cache, memória, orphans.
"""
import sys, time, json, hashlib, threading
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS, OPERATIONAL_UNIVERSE
from mercury_ai.brain.scanner import MercuryScanner

GLOBAL_MEM = Path("data/institutional_memory.json")

def mem_hash():
    if not GLOBAL_MEM.exists():
        return "NA(nonexistent)"
    h = hashlib.sha256(GLOBAL_MEM.read_bytes()).hexdigest()[:16]
    return f"{h}|size={GLOBAL_MEM.stat().st_size}|mtime={GLOBAL_MEM.stat().st_mtime}"

def run_canary(n, workers=4, cycle_timeout=290.0):
    symbols = list(ALL_SYMBOLS[:n])
    print(f"\n{'='*70}\nRUN canary n={n} workers={workers} start={datetime.now(timezone.utc).isoformat()}\n{'='*70}", flush=True)
    print(f"assets: {symbols}", flush=True)
    sc = MercuryScanner()
    # Força universo exato do canário sem tocar produção: resolve retorna subset
    orig_resolve = sc._resolve_scan_symbols
    def _patched():
        return (list(symbols), False, [])
    sc._resolve_scan_symbols = _patched
    # Instrumenta ordem de conclusão
    completion_order = []
    t0_global = [None]
    orig_iso = sc._analyze_symbol_isolated
    def _wrapped(symbol, scan_id=None):
        res = orig_iso(symbol, scan_id=scan_id)
        completion_order.append((symbol, time.perf_counter()))
        return res
    sc._analyze_symbol_isolated = _wrapped

    mem_before = mem_hash()
    threads_before = sorted([t.name for t in threading.enumerate()])
    cache_before = sc.get_download_stats()
    t0 = time.perf_counter()
    t0_global[0] = t0
    t_start_iso = datetime.now(timezone.utc).isoformat()
    ranked = sc.scan(workers=workers, cycle_timeout_s=cycle_timeout)
    t_end = time.perf_counter()
    t_end_iso = datetime.now(timezone.utc).isoformat()
    rep = sc.last_scan_report
    # aguarda 3s p/ detectar orphans tardios
    time.sleep(3)
    threads_after = sorted([t.name for t in threading.enumerate()])
    mem_after = mem_hash()
    cache_after = sc.get_download_stats()
    # métricas
    d = rep.to_dict() if rep is not None else {}
    per = d.get("per_asset", [])
    durs = [r.get("duration_ms", 0) for r in per]
    if completion_order:
        co_sorted = sorted(completion_order, key=lambda x: x[1])
        first_sym, first_t = co_sorted[0]
        t1 = first_t - t0
        order = [s for s, _ in co_sorted]
    else:
        first_sym, t1, order = None, None, []
    out = {
        "assets": n,
        "workers": workers,
        "start": t_start_iso,
        "first_result": {"symbol": first_sym, "latency_s": round(t1, 2) if t1 is not None else None},
        "first_top3": {"count": len(d.get("top3", [])), "top3": [t.get("symbol") for t in d.get("top3", [])]},
        "end": t_end_iso,
        "duration_s": round(t_end - t0, 2),
        "report_duration_s": d.get("duration_s"),
        "status": d.get("status"),
        "completed": d.get("symbols_completed"),
        "failed_errors": d.get("symbols_error"),
        "timeout": d.get("symbols_timeout"),
        "symbols_total": d.get("symbols_total"),
        "outcomes": {},
        "dur_max_ms": max(durs) if durs else None,
        "dur_mean_ms": round(sum(durs)/len(durs), 1) if durs else None,
        "assets_per_sec": round(n/(t_end-t0), 3) if (t_end-t0) > 0 else None,
        "downloads_before": cache_before,
        "downloads_after": cache_after,
        "cache_hits": cache_after.get("hits"),
        "cache_misses": cache_after.get("misses"),
        "downloads": cache_after.get("downloads"),
        "orphans_threads_before": len(threads_before),
        "orphans_threads_after": len(threads_after),
        "threads_delta": [t for t in threads_after if t not in threads_before],
        "global_memory_changed": (mem_before != mem_after),
        "mem_before": mem_before,
        "mem_after": mem_after,
        "ranking_count": len(d.get("ranked", [])),
        "top3_count": len(d.get("top3", [])),
        "completion_order": order,
        "ranking_symbols": [t.get("symbol") for t in d.get("ranked", [])],
    }
    for r in per:
        o = r.get("outcome", "?")
        out["outcomes"][o] = out["outcomes"].get(o, 0) + 1
    print(json.dumps(out, indent=2), flush=True)
    return out

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--sets", default="2,4,8,12,39")
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--timeout", type=float, default=290.0)
    a = p.parse_args()
    print(f"OPERATIONAL_UNIVERSE={len(OPERATIONAL_UNIVERSE)} ALL_SYMBOLS={len(ALL_SYMBOLS)}", flush=True)
    assert len(OPERATIONAL_UNIVERSE) == 39 and len(ALL_SYMBOLS) == 39, "UNIVERSO != 39 -> BLOCKED"
    results = []
    for n in [int(x) for x in a.sets.split(",")]:
        results.append(run_canary(n, workers=a.workers, cycle_timeout=a.timeout))
    Path("s33e4_benchmark_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print("\nSAVED s33e4_benchmark_results.json", flush=True)
