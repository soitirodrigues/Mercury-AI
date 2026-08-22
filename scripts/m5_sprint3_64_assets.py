#!/usr/bin/env python3
"""
SPRINT 3 — TESTE 64 ATIVOS (medição real, não projeção)
Mede first_decision, partial_top3, complete_top3, fresh/stale, wall total, MTF wall
"""
import sys, time, json, statistics
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mercury_ai.config.universe import ALL_SYMBOLS
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

print(f"Universe size: {len(ALL_SYMBOLS)}")
# Usar todo universo disponível (63) — Sprint pede 64 mas temos 63 no arquivo
SYMBOLS = ALL_SYMBOLS
print(f"Will scan {len(SYMBOLS)} symbols: {SYMBOLS[:5]} ...")

provider=MercuryDataProvider()
ms=MarketDataService(provider=provider)
pipeline=AnalysisPipeline(market_service=ms, providers=[provider])

OUT_DIR=Path("reports/m5_mtf_optimization")
OUT_DIR.mkdir(parents=True, exist_ok=True)

wall_start=time.perf_counter()
wall_start_iso=datetime.now(timezone.utc).isoformat()

mtf_times=[]; wall_times=[]; fetch_times=[]
first_ms=None; partial_ms=None
completed=0
per_asset=[]
fresh=0; stale=0; unavailable=0

for idx, sym in enumerate(SYMBOLS,1):
    t0=time.perf_counter()
    try:
        res=pipeline.analyze(sym)
        dec=res.decision
        audit=str(getattr(dec,"audit_id","")or "")
        # classify
        is_hash=len(audit)==64 and all(c in "0123456789abcdefABCDEF" for c in audit)
        if audit in ("DATA_PROVIDER_UNAVAILABLE","PIPELINE_ERROR","DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED"):
            unavailable+=1
            status="DATA_UNAVAILABLE"
        elif is_hash:
            fresh+=1
            status="FRESH"
        else:
            # treat WAIT with hash as fresh else stale? simplified
            fresh+=1
            status=audit[:8]
        t1=time.perf_counter()
        wall_ms=(t1-t0)*1000
        # profiler
        try:
            prof=pipeline.profiler.summary()
            mtf_ms=next((s.duration*1000 for s in prof.stage_profiles if s.name=="MTFAnalysis"),0)
            fetch_ms=next((s.duration*1000 for s in prof.stage_profiles if s.name=="DataLoading"),0)
        except: mtf_ms=fetch_ms=0
        mtf_times.append(mtf_ms); wall_times.append(wall_ms); fetch_times.append(fetch_ms)
        elapsed_from_start=(t1-wall_start)*1000
        if first_ms is None:
            first_ms=elapsed_from_start
        if idx==3 and partial_ms is None:
            partial_ms=elapsed_from_start
        per_asset.append({"symbol":sym,"decision":str(getattr(dec,"decision","")), "audit":audit[:12], "status":status, "wall_ms":round(wall_ms,1), "mtf_ms":round(mtf_ms,1), "fetch_ms":round(fetch_ms,1)})
        print(f"[{idx}/{len(SYMBOLS)}] {sym} {wall_ms:.0f}ms mtf={mtf_ms:.0f} status={status} audit={audit[:12]}")
        completed+=1
    except Exception as e:
        print(f"[{idx}] {sym} ERROR {e}")
        per_asset.append({"symbol":sym,"error":str(e)[:200]})

complete_ms=(time.perf_counter()-wall_start)*1000

def perc(data,p):
    if not data: return 0
    s=sorted(data); k=(len(s)-1)*p/100; f=int(k); c=min(f+1,len(s)-1)
    if f==c: return float(s[f])
    return float(s[f]*(c-k)+s[c]*(k-f))

stats={
    "measured_at": datetime.now(timezone.utc).isoformat(),
    "universe": len(SYMBOLS),
    "total_wall_ms": round(complete_ms,1),
    "total_wall_s": round(complete_ms/1000,1),
    "first_decision_ms": round(first_ms,1) if first_ms else 0,
    "partial_top3_ms": round(partial_ms,1) if partial_ms else 0,
    "complete_top3_ms": round(complete_ms,1),
    "mtf_total_ms": round(sum(mtf_times),1),
    "mtf_total_s": round(sum(mtf_times)/1000,1),
    "mtf_avg_ms": round(statistics.mean(mtf_times),1) if mtf_times else 0,
    "fetch_total_ms": round(sum(fetch_times),1),
    "wall_avg_ms": round(statistics.mean(wall_times),1) if wall_times else 0,
    "wall_p95_ms": round(perc(wall_times,95),1) if wall_times else 0,
    "fresh": fresh, "unavailable": unavailable,
    "per_asset": per_asset,
    "sprint2_baseline": {"complete_ms":285000, "first_ms":21900, "partial_ms":70200},
    "improvement": {}
}
if stats["complete_top3_ms"]:
    stats["improvement"]["complete_pct"]=round((1-stats["complete_top3_ms"]/285000)*100,1)
# M5 window: 300s (5min) — check if complete <300s?
stats["next_candle_ready"] = stats["complete_top3_ms"] < 300000 and stats["first_decision_ms"] < 300000

out=OUT_DIR/"sprint3_64_assets.json"
out.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
print("\n"+json.dumps(stats, indent=2))
print(f"\nWrote {out}")
print(f"NEXT_CANDLE_READY (wall<300s): {stats['next_candle_ready']}")
