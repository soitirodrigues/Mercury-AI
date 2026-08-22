#!/usr/bin/env python3
"""
M5 DEEP DIVE — mede MTF vs outros estágios isoladamente
Usa runtime_reports já gerados + profiling fino de 3 amostras representativas
"""
import json, sys, time, statistics
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Aggregate runtime_reports
import glob, json as js

# Pick latest 3 reports: one FOREX, one CRYPTO, one STOCK
reports = sorted(Path(".").glob("runtime_report_*.json"), key=lambda p: p.stat().st_mtime, reverse=True)

# Filter: reports from our scan (today)
from datetime import datetime, timedelta
today_reports = [p for p in reports if "20260902" in p.name]
print(f"Total runtime reports today: {len(today_reports)}")

# Group by symbol
from collections import defaultdict
by_symbol = defaultdict(list)
for p in today_reports:
    # symbol is before _20
    name = p.name
    # runtime_report_SYMBOL_TIMESTAMP.json
    try:
        inner = name[len("runtime_report_"):]
        # Find _20 (year)
        idx = inner.rfind("_20")
        sym = inner[:idx]
        by_symbol[sym].append(p)
    except: pass

print(f"Distinct symbols with reports: {len(by_symbol)}")
for sym, lst in sorted(by_symbol.items())[:10]:
    print(f"  {sym}: {len(lst)} reports")

# Analyze one FOREX, one CRYPTO, one STOCK with latest report each
samples = {}
for pick in ["EURUSD=X", "BTC-USD", "AAPL"]:
    if pick in by_symbol:
        latest = max(by_symbol[pick], key=lambda p: p.stat().st_mtime)
        samples[pick] = latest

print("\n=== SAMPLE STAGE BREAKDOWN ===")
for sym, path in samples.items():
    data = js.loads(path.read_text(encoding="utf-8"))
    stages = data["stages"]
    total = sum(s["execution_time"] for s in stages)
    mtf = next((s for s in stages if s["engine_name"]=="MTFAnalysis"), None)
    struct = next((s for s in stages if s["engine_name"]=="StructureAnalysis"), None)
    data_load = next((s for s in stages if s["engine_name"]=="DataLoading"), None)
    print(f"\n{sym} ({path.name}): total stages={total:.2f}s")
    for s in stages:
        pct = s["execution_time"]/total*100 if total else 0
        print(f"  {s['engine_name']:20} {s['execution_time']:6.2f}s {pct:5.1f}%")
    if mtf:
        print(f"  >>> MTF share = {mtf['execution_time']/total*100:.1f}% ({mtf['execution_time']:.2f}s)")
    if struct:
        print(f"  >>> Structure share = {struct['execution_time']/total*100:.1f}%")

# Aggregate across all today's reports: average stage times
print("\n=== AGGREGATE STAGE AVERAGES (all today's reports) ===")
stage_times = defaultdict(list)
for p in today_reports:
    try:
        data = js.loads(p.read_text(encoding="utf-8"))
        for s in data["stages"]:
            stage_times[s["engine_name"]].append(s["execution_time"])
    except: continue

for name, times in sorted(stage_times.items(), key=lambda x: statistics.mean(x[1]), reverse=True):
    avg = statistics.mean(times)
    med = statistics.median(times)
    mx = max(times)
    mn = min(times)
    total_avg = sum(statistics.mean(v) for v in stage_times.values())
    share = avg/total_avg*100 if total_avg else 0
    print(f"  {name:20} avg={avg:6.3f}s med={med:6.3f} max={mx:6.2f} share={share:4.1f}% n={len(times)}")

total_avg_all = sum(statistics.mean(v) for v in stage_times.values())
print(f"\nTotal avg per asset (sum of stage means): {total_avg_all:.2f}s")
print(f"Of which MTF avg: {statistics.mean(stage_times.get('MTFAnalysis', [0])):.2f}s ({statistics.mean(stage_times.get('MTFAnalysis', [0]))/total_avg_all*100:.1f}%)")

# Also do live micro-benchmark: measure MTF internal fetch vs compute
print("\n=== LIVE MTF FETCH vs COMPUTE SPLIT ===")
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.analysis.mtf_engine import MTFEngine

provider = MercuryDataProvider()
mtf_engine = MTFEngine(providers=[provider])

for sym in ["EURUSD=X", "BTC-USD", "AAPL"]:
    print(f"\n--- {sym} ---")
    # Time MTF analyze
    t0 = time.perf_counter()
    evs, consensus = mtf_engine.analyze(sym)
    t1 = time.perf_counter()
    print(f"MTF.analyze wall: {(t1-t0):.2f}s evs={len(evs)} bias={consensus.global_bias} alignment={consensus.alignment_score:.1f}")
    print(f"  timeframe_status: {consensus.timeframe_status}")
    # Fetch-only timing
    from mercury_ai.config.timeframes import YFINANCE_INTERVALS
    fetch_total = 0
    for tf in ["M1","M5","M15","H1","H4"]:
        interval = YFINANCE_INTERVALS[tf]
        t0 = time.perf_counter()
        try:
            df = mtf_engine.market_service.get_data(sym, interval=interval, period="1mo")
            dt = time.perf_counter()-t0
            fetch_total += dt
            print(f"    {tf} ({interval}): {dt:.3f}s rows={0 if df is None else len(df)}")
        except Exception as e:
            print(f"    {tf}: ERROR {e}")

# Check cache opportunity: are MTF fetches overlapping with main fetch?
print("\n=== CACHE OPPORTUNITY ANALYSIS ===")
print("Main pipeline does: MarketDataService.get_data(M5, 5d) -> then MTF re-fetches M5/1mo + M1/M15/H1/H4")
print("Overlap: M5 is fetched TWICE (main + MTF). MTF period is 1mo vs main 5d — different windows.")
print("Potential cache: MTF's 5 fetches dominate wall time; each is yfinance download (network).")
print("Risk: reusing stale 5m candle would mean decision based on previous close, not latest close.")
print("Safe cache window: < 60s if we trust yfinance TTL; but must guarantee last candle is fresh.")
