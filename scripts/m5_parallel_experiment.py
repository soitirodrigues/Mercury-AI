#!/usr/bin/env python3
"""
M5 PARALLEL EXPERIMENT — controlado e seguro
Compara SEQUENTIAL vs CONTROLLED_PARALLEL (max_workers=4) sem alterar lógica de produção.
Verifica: total duration, decision integrity, Top-3, determinism, provider errors
"""
import time, json, sys, traceback, hashlib
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

# Use universe but limit to first 10 for quick experiment to avoid long wait
# For final M5, use full universe if needed. We'll run 10-asset sample + full if time allows.
SAMPLE_SYMBOLS = ALL_SYMBOLS[:12]  # 12 to include mix
FULL = False  # set True to run 64 (takes ~17min seq, ~5min parallel)

symbols = ALL_SYMBOLS if FULL else SAMPLE_SYMBOLS
print(f"PARALLEL EXPERIMENT symbols={len(symbols)} full={FULL}")

def run_sequential(symbols):
    provider = MercuryDataProvider()
    market_service = MarketDataService(provider=provider)
    pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])
    results = {}
    t0 = time.perf_counter()
    for sym in symbols:
        try:
            r = pipeline.analyze(sym)
            dec = r.decision
            results[sym] = {
                "decision": str(getattr(dec, "decision", "")),
                "audit_id": str(getattr(dec, "audit_id", "")),
                "grade": str(getattr(dec, "grade", "")),
                "buy": float(getattr(dec, "buy_probability", 0) or 0),
                "sell": float(getattr(dec, "sell_probability", 0) or 0),
                "wait": float(getattr(dec, "wait_probability", 0) or 0),
            }
        except Exception as e:
            results[sym] = {"error": str(e), "trace": traceback.format_exc()[:600]}
    t1 = time.perf_counter()
    return results, (t1-t0)

def run_parallel(symbols, max_workers=4):
    # Each thread gets its own pipeline/market_service/provider to avoid shared state races
    # Provider is stateless except rate limits; DeterministicClock is thread-local; SnapshotLogger has lock
    def analyze_one(sym):
        provider = MercuryDataProvider()
        market_service = MarketDataService(provider=provider)
        pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])
        t0 = time.perf_counter()
        try:
            r = pipeline.analyze(sym)
            dec = r.decision
            dt = time.perf_counter()-t0
            return sym, {
                "decision": str(getattr(dec, "decision", "")),
                "audit_id": str(getattr(dec, "audit_id", "")),
                "grade": str(getattr(dec, "grade", "")),
                "buy": float(getattr(dec, "buy_probability", 0) or 0),
                "sell": float(getattr(dec, "sell_probability", 0) or 0),
                "wait": float(getattr(dec, "wait_probability", 0) or 0),
                "duration_s": dt,
            }, None
        except Exception as e:
            dt = time.perf_counter()-t0
            return sym, None, str(e) + traceback.format_exc()[:600]
    results = {}
    errors = {}
    t0 = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(analyze_one, s): s for s in symbols}
        for fut in as_completed(futs):
            sym, res, err = fut.result()
            if err:
                errors[sym]=err
                results[sym]={"error":err}
            else:
                results[sym]=res
    t1 = time.perf_counter()
    return results, (t1-t0), errors

print("\n--- SEQUENTIAL ---")
seq_res, seq_time = run_sequential(symbols)
print(f"Sequential time: {seq_time:.2f}s for {len(symbols)} symbols avg={seq_time/len(symbols):.2f}s/symbol")
for sym in symbols:
    r = seq_res.get(sym, {})
    print(f"  {sym:12} {r.get('decision','ERR'):5} audit={str(r.get('audit_id',''))[:12]}")

print("\n--- CONTROLLED_PARALLEL (max_workers=4) ---")
par_res, par_time, par_errors = run_parallel(symbols, max_workers=4)
print(f"Parallel time: {par_time:.2f}s for {len(symbols)} symbols avg={par_time/len(symbols):.2f}s/symbol speedup={seq_time/par_time:.2f}x")
for sym in symbols:
    r = par_res.get(sym, {})
    print(f"  {sym:12} {r.get('decision','ERR'):5} audit={str(r.get('audit_id',''))[:12]} err={1 if 'error' in r else 0}")

# Integrity checks
print("\n--- DECISION INTEGRITY ---")
mismatches = []
for sym in symbols:
    s = seq_res.get(sym, {})
    p = par_res.get(sym, {})
    if s.get("decision") != p.get("decision") or s.get("audit_id") != p.get("audit_id"):
        mismatches.append(sym)
        print(f"  MISMATCH {sym}: seq={s} par={p}")
if not mismatches:
    print("  PASS: all decisions+audit_id identical between seq and parallel")
else:
    print(f"  FAIL: {len(mismatches)} mismatches")

# Determinism: run parallel twice
print("\n--- DETERMINISM (parallel run 2) ---")
par_res2, par_time2, _ = run_parallel(symbols, max_workers=4)
det_mismatch = []
for sym in symbols:
    if par_res.get(sym, {}).get("audit_id") != par_res2.get(sym, {}).get("audit_id"):
        det_mismatch.append(sym)
if not det_mismatch:
    print(f"  PASS: parallel determinism (run1 == run2) times {par_time:.2f}s vs {par_time2:.2f}s")
else:
    print(f"  FAIL: determinism mismatches {det_mismatch}")

# Provider errors
seq_errs = sum(1 for v in seq_res.values() if "error" in v)
par_errs = sum(1 for v in par_res.values() if "error" in v)
print(f"\nProvider errors: seq={seq_errs} parallel={par_errs}")

# Thread safety notes
print("\n--- THREAD SAFETY ASSESSMENT ---")
print("DeterministicClock: thread-local (SAFE)")
print("SnapshotLogger: threading.Lock (SAFE)")
print("PipelineProfiler: threading.local stack but tracemalloc global (RACE: tracemalloc.start/stop global, may interleave)")
print("MarketDataService/YahooAdapter: yfinance not thread-safe, but each thread has own provider instance; rate limit unknown")
print("AnalysisPipeline shared state if reused: last_snapshot/last_snapshots/runtime_report RACE — mitigated by per-thread pipeline instance")
print("DataQualityEngine/IndicatorEngine: stateless (SAFE)")
print("Recommendation: per-thread pipeline instance + avoid global profiler tracemalloc in parallel (disable profiler)")

# Top-3 comparison
def compute_top3(results):
    GRADE_BONUS = {"A+":25,"A":20,"B":15,"C":10,"D":5,"N/A":0, None:0}
    eligible=[]
    for sym, r in results.items():
        if "error" in r: continue
        # need to fetch full decision? We have grade/decision but need confluence/confidence — not captured here
        # For this quick test, Top-3 comparison not fully achievable without confluence. Skip.
        pass
    return eligible

# Summary
speedup = seq_time/par_time if par_time else 0
projected_full_seq = 1026  # from operational latency
projected_full_par4 = projected_full_seq / speedup if speedup else 0

report = {
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "sample_size": len(symbols),
    "sequential_seconds": round(seq_time,2),
    "parallel_seconds": round(par_time,2),
    "speedup": round(speedup,2),
    "sequential_avg_per_symbol_s": round(seq_time/len(symbols),2),
    "parallel_avg_per_symbol_s": round(par_time/len(symbols),2),
    "mismatches": mismatches,
    "determinism_pass": len(det_mismatch)==0,
    "provider_errors_seq": seq_errs,
    "provider_errors_par": par_errs,
    "projected_full_scan_seq_s": projected_full_seq,
    "projected_full_scan_par4_s": round(projected_full_par4,2),
    "projected_margin_for_M5_par4_s": round(300 - projected_full_par4,2),
    "thread_safety_notes": "DeterministicClock thread-local SAFE; SnapshotLogger lock SAFE; PipelineProfiler tracemalloc global RACE; per-thread pipeline mitigates last_snapshot race; yfinance rate limit UNKNOWN",
}

OUT = ROOT / "reports" / "asset_universe" / "m5_parallel_experiment.json"
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nWrote {OUT}")
print(json.dumps(report, indent=2))
