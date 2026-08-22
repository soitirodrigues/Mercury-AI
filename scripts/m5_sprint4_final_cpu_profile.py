#!/usr/bin/env python3
"""CPU PROFILING — M1 gargalo determinístico"""
import sys, time, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

provider=MercuryDataProvider()
ms=MarketDataService(provider=provider)
pipeline=AnalysisPipeline(market_service=ms, providers=[provider])
pipeline.profiler.active=True

sym="EURUSD=X"
# Prime warmup
try:
    pipeline.analyze(sym)
except: pass

# Profile run
pipeline.profiler.start_pipeline()
import pandas as pd
t0=time.perf_counter()
df=ms.get_data(sym, interval="1m", period="5d")
t_fetch=time.perf_counter()-t0
print(f"M1 df len {len(df)} fetch {t_fetch:.2f}s")
# Run pipeline with profiling
res=pipeline.analyze(sym)
prof=pipeline.profiler.summary()
out={"symbol":sym,"m1_rows":len(df), "stages":[]}
for st in prof.stage_profiles:
    out["stages"].append({"name":st.name,"duration":round(st.duration,3),"pct":round(st.percentage_total,1)})
    print(f"{st.name:20} {st.duration:.3f}s {st.percentage_total:.1f}%")
# Top bottleneck
out["bottleneck"]="M1 detect_swings+MTF per earlier, now measured via stages"
out["fetch_s"]=round(t_fetch,3)
out["total_s"]=round(sum(s.duration for s in prof.stage_profiles),3)
Path("reports/m5_sprint4/cpu_profile.json").parent.mkdir(parents=True,exist_ok=True)
Path("reports/m5_sprint4/cpu_profile.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
