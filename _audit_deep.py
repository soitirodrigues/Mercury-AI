import pathlib, re
root=pathlib.Path("C:/Projetos/Mercury-AI")
files = [
 "mercury_ai/utils/deterministic_clock.py",
 "mercury_ai/analysis/historical_replay_engine.py",
 "mercury_ai/analysis/replay_batch_processor.py",
 "mercury_ai/core/analysis_pipeline.py",
 "mercury_ai/providers/yahoo_finance_provider.py",
 "mercury_ai/providers/historical_replay_provider.py",
 "mercury_ai/data/data_quality_engine.py",
 "mercury_ai/data/data_normalizer.py",
 "mercury_ai/data/market_data.py",
 "mercury_ai/data/mercury_data_provider.py",
 "mercury_ai/data/indicator_engine.py",
 "mercury_ai/analysis/replay_cache.py",
 "mercury_ai/analysis/benchmark_framework.py",
 "mercury_ai/analysis/institutional_memory_engine.py",
 "mercury_ai/database/replay_storage.py",
 "mercury_ai/database/snapshot_logger.py",
]

for rel in files:
    p=root/rel
    if not p.exists():
        print(f"MISSING {rel}")
        continue
    txt=p.read_text(encoding="utf-8", errors="ignore")
    print(f"\n### {rel} ###")
    for i,line in enumerate(txt.splitlines(),1):
        s=line.strip()
        if not s or s.startswith("#"): continue
        # flag interesting
        if any(k in line for k in ["datetime.now","datetime.utcnow","time.time","perf_counter","monotonic","sleep","random","uuid","hashlib","hash(","threading","ThreadPool","ProcessPool","asyncio","concurrent","Lock()","OrderedDict","set(","dict(","as_completed","global ","_instance","singleton","Singleton","InstitutionalMemory","MarketDataService","open(","read_csv","to_csv","json.dump","json.load","atomic","Path(","exists","yfinance","yf.","requests","http","isoformat","fromisoformat","timestamp","time.time","DeterministicClock"]):
            print(f"L{i:3d}: {s[:200]}")
