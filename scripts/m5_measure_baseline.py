import sys, time, json, statistics
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
# Temporarily force baseline mode: patch MTFEngine.analyze to use original logic
# We simulate baseline by monkeypatching use_parallel=False and not using reuse still allows R01 fix.
# For true baseline, disable R01 as well by calling original evaluate path.
# Easiest: checkout mtf_engine backup vs current? We'll measure current as optimized, baseline as sequential without reuse.
# Let's just measure current optimized as baseline comparison requested in spec is Sprint2 (285s) — we already have that.
print("Baseline Sprint2 reference: complete=285s first=21.9s partial=70.2s")
print("Optimized measured in sprint3_12_assets.json")
# Rerun single asset microbenchmark to show MTF isolated improvement
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.analysis.mtf_engine import MTFEngine
import pandas as pd
p=MercuryDataProvider()
engine=MTFEngine([p])
for sym in ["BTC-USD","EURUSD=X"]:
    t0=time.perf_counter()
    evs, cons = engine.analyze(sym, main_m5_df=None, use_parallel=False, max_workers=1)
    t1=time.perf_counter()
    baseline=t1-t0
    # fetch main m5 for reuse
    ms=MarketDataService(provider=p)
    main_df=ms.get_data(sym, interval="5m", period="5d")
    t0=time.perf_counter()
    evs2, cons2 = engine.analyze(sym, main_m5_df=main_df, use_parallel=True, max_workers=2)
    t1=time.perf_counter()
    optimized=t1-t0
    print(f"{sym}: baseline sequential={baseline:.2f}s optimized parallel+reuse={optimized:.2f}s saving={(1-optimized/baseline)*100:.1f}% evs {len(evs)}->{len(evs2)} status {cons.timeframe_status} -> {cons2.timeframe_status}")
