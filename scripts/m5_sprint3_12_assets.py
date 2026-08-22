#!/usr/bin/env python3
"""
SPRINT 3 — TESTE 12 ATIVOS (BASELINE vs OPTIMIZED)
Mede wall, MTF total, média, p50/p95, first_decision, partial_top3, complete_top3
Comparação com Sprint2: 285s complete, 21.9 first, 70.2 partial
"""
import sys, time, json, statistics
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

# 12 ativos: mix majors + crypto + stocks (primeiros 12 do universo)
SYMBOLS_12 = ALL_SYMBOLS[:12]
print(f"Testing 12 assets: {SYMBOLS_12}")

provider = MercuryDataProvider()
market_service = MarketDataService(provider=provider)
pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])

def percentile(data, p):
    if not data: return 0
    s=sorted(data); k=(len(s)-1)*p/100; f=int(k); c=min(f+1,len(s)-1)
    if f==c: return float(s[f])
    return float(s[f]*(c-k)+s[c]*(k-f))

# Run 12 assets real measurement (optimized path via pipeline which now does MTF parallel+reuse)
OUT_DIR = Path("reports/m5_mtf_optimization")
OUT_DIR.mkdir(parents=True, exist_ok=True)

wall_start = time.perf_counter()
wall_start_iso = datetime.now(timezone.utc).isoformat()

per_asset=[]
mtf_times=[]
total_times=[]
fetch_times=[]
completed_times=[]  # timestamp when asset finished
partial_top3_time=None
first_decision_time=None
complete_top3_time=None

# For ranking after
records=[]

for idx, sym in enumerate(SYMBOLS_12, 1):
    t0=time.perf_counter()
    try:
        result = pipeline.analyze(sym)
    except Exception as e:
        print(f"[{idx}] {sym} ERROR: {e}")
        continue
    t1=time.perf_counter()
    wall_ms = (t1-t0)*1000
    # extract MTF time from profiler
    mtf_ms=0
    fetch_ms=0
    try:
        prof=pipeline.profiler.summary()
        for st in prof.stage_profiles:
            if st.name=="MTFAnalysis": mtf_ms=st.duration*1000
            if st.name=="DataLoading": fetch_ms=st.duration*1000
    except: pass
    mtf_times.append(mtf_ms)
    total_times.append(wall_ms)
    fetch_times.append(fetch_ms)
    elapsed_from_start = (t1-wall_start)*1000
    completed_times.append(elapsed_from_start)
    if first_decision_time is None:
        first_decision_time = elapsed_from_start
    if idx==3 and partial_top3_time is None:
        partial_top3_time = elapsed_from_start
    decision = result.decision if result else None
    # ranking record minimal
    records.append({"symbol": sym, "decision": str(getattr(decision,"decision","") or ""), "grade": str(getattr(decision,"grade","") or ""), "confidence": getattr(decision,"confidence",0), "confluence": getattr(result.confluence,"weighted_score",0) if result and result.confluence else 0, "buy_p": getattr(decision,"buy_probability",0), "sell_p": getattr(decision,"sell_probability",0), "wait_p": getattr(decision,"wait_probability",0), "audit_id": str(getattr(decision,"audit_id","")or ""), "wall_ms": wall_ms, "mtf_ms": mtf_ms})
    print(f"[{idx}/12] {sym} wall={wall_ms:.0f} mtf={mtf_ms:.0f} fetch={fetch_ms:.0f} -> {getattr(decision,'decision','?')}")

complete_top3_time = (time.perf_counter()-wall_start)*1000
total_wall = complete_top3_time

# Compute stats
stats={
    "symbols": SYMBOLS_12,
    "measured_at": datetime.now(timezone.utc).isoformat(),
    "wall_start": wall_start_iso,
    "total_wall_ms": round(total_wall,2),
    "total_wall_s": round(total_wall/1000,2),
    "mtf_total_ms": round(sum(mtf_times),2),
    "mtf_total_s": round(sum(mtf_times)/1000,2),
    "mtf_avg_ms": round(statistics.mean(mtf_times),2) if mtf_times else 0,
    "mtf_p50_ms": round(statistics.median(mtf_times),2) if mtf_times else 0,
    "mtf_p95_ms": round(percentile(mtf_times,95),2) if mtf_times else 0,
    "wall_avg_ms": round(statistics.mean(total_times),2) if total_times else 0,
    "wall_p50_ms": round(statistics.median(total_times),2) if total_times else 0,
    "wall_p95_ms": round(percentile(total_times,95),2) if total_times else 0,
    "first_decision_ms": round(first_decision_time,2) if first_decision_time else 0,
    "partial_top3_ms": round(partial_top3_time,2) if partial_top3_time else 0,
    "complete_top3_ms": round(complete_top3_time,2),
    "sprint2_baseline": {"complete_s":285, "first_ms":21900, "partial_ms":70200},
    "improvement": {},
    "per_asset": records,
}

# improvement vs sprint2
baseline_complete = 285*1000
if stats["complete_top3_ms"]:
    stats["improvement"]["complete_pct"] = round((1 - stats["complete_top3_ms"]/baseline_complete)*100,1)
if stats["first_decision_ms"]:
    stats["improvement"]["first_pct"] = round((1 - stats["first_decision_ms"]/21900)*100,1)
if stats["partial_top3_ms"]:
    stats["improvement"]["partial_pct"] = round((1 - stats["partial_top3_ms"]/70200)*100,1)

out_json = OUT_DIR / "sprint3_12_assets.json"
out_json.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n" + "="*70)
print(json.dumps(stats, indent=2))
print(f"\nWrote {out_json}")
# TXT
txt = OUT_DIR / "sprint3_12_assets.txt"
txt_lines=[f"Sprint3 12 assets — {stats['measured_at']}", f"Symbols: {', '.join(SYMBOLS_12)}", f"Total wall: {stats['total_wall_s']:.1f}s (baseline 285s) -> {stats['improvement'].get('complete_pct','?')}% faster", f"First decision: {stats['first_decision_ms']:.0f}ms (baseline 21900) -> {stats['improvement'].get('first_pct','?')}%", f"Partial Top3: {stats['partial_top3_ms']:.0f}ms (baseline 70200) -> {stats['improvement'].get('partial_pct','?')}%", f"MTF avg: {stats['mtf_avg_ms']:.0f}ms p50={stats['mtf_p50_ms']:.0f} p95={stats['mtf_p95_ms']:.0f} total={stats['mtf_total_s']:.1f}s", f"Wall avg per asset: {stats['wall_avg_ms']:.0f}ms p95={stats['wall_p95_ms']:.0f}"]
txt.write_text("\n".join(txt_lines), encoding="utf-8")
print("\n".join(txt_lines))
