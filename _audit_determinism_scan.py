import os, re, pathlib

root = pathlib.Path("C:/Projetos/Mercury-AI")
targets = [
    "mercury_ai/analysis/historical_replay_engine.py",
    "mercury_ai/analysis/replay_batch_processor.py",
    "mercury_ai/utils/deterministic_clock.py",
    "mercury_ai/core/analysis_pipeline.py",
    "mercury_ai/providers/yahoo_finance_provider.py",
    "mercury_ai/providers/historical_replay_provider.py",
]
# add data/*.py
data_dir = root/"mercury_ai/data"
for p in data_dir.glob("*.py"):
    targets.append(str(p.relative_to(root)).replace("\\","/"))
# providers
prov_dir = root/"mercury_ai/providers"
for p in prov_dir.glob("*.py"):
    if str(p.relative_to(root)).replace("\\","/") not in targets:
        targets.append(str(p.relative_to(root)).replace("\\","/"))
# analysis/*.py
ana_dir = root/"mercury_ai/analysis"
for p in ana_dir.glob("*.py"):
    rel = str(p.relative_to(root)).replace("\\","/")
    if rel not in targets:
        targets.append(rel)
for p in (ana_dir/"smart_money").glob("*.py"):
    rel = str(p.relative_to(root)).replace("\\","/")
    targets.append(rel)

patterns = {
    "SYSTEM_CLOCK_datetime.now": re.compile(r"datetime\.now\s*\("),
    "SYSTEM_CLOCK_datetime.utcnow": re.compile(r"datetime\.utcnow\s*\("),
    "SYSTEM_CLOCK_time.time": re.compile(r"\btime\.time\s*\("),
    "MONOTONIC_perf_counter": re.compile(r"perf_counter\s*\("),
    "MONOTONIC_monotonic": re.compile(r"time\.monotonic\s*\("),
    "DETERMINISTIC_CLOCK": re.compile(r"DeterministicClock"),
    "RANDOM_random": re.compile(r"\brandom\b"),
    "RANDOM_RandomState": re.compile(r"RandomState"),
    "RANDOM_np.random": re.compile(r"np\.random|numpy\.random"),
    "UUID": re.compile(r"\buuid\b"),
    "HASH": re.compile(r"hashlib|hash\(\)"),
    "THREADING": re.compile(r"threading|ThreadPoolExecutor|concurrent\.futures|Lock\(\)|as_completed"),
    "ASYNC": re.compile(r"\basyncio\b|async def|await "),
    "CACHE": re.compile(r"cache|_CacheEntry|ReplayCache"),
    "SINGLETON_GLOBAL": re.compile(r"class.*Singleton|_instance|global |InstitutionalMemoryEngine\(\)|MarketDataService"),
    "FILESYSTEM": re.compile(r"os\.path|open\(|read_csv|to_csv|atomic_json|json\.dump|json\.load|Path\(|exists"),
    "NETWORK_yfinance": re.compile(r"yfinance|yf\.Ticker|ticker\.history|requests\.|http"),
    "COLLECTIONS_ORDER": re.compile(r"\bset\(|dict\(|as_completed\(|for .* in .*\.keys\(\)|for .* in .*\.items\(\)"),
    "TIMESTAMP_isoformat": re.compile(r"isoformat\(\)|fromisoformat|timestamp"),
}

for rel in sorted(targets):
    fp = root/rel
    if not fp.exists():
        continue
    text = fp.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    print(f"\n=== {rel} ({len(lines)} linhas) ===")
    for name, pat in patterns.items():
        for i, line in enumerate(lines, 1):
            if pat.search(line):
                stripped = line.strip()
                if len(stripped) > 180:
                    stripped = stripped[:180]+"..."
                print(f"  L{i:3d} [{name}] {stripped}")
