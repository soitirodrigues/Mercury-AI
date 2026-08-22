#!/usr/bin/env python3
"""
Frozen determinism ISOLATED — usa pipeline único compartilhado para todos os símbolos,
ou cria pipelines por símbolo MAS com singleton reset correto.
Avalia equivalência REAL do SPRINT 3/4 sem pollution de InstitutionalMemory.
"""
import sys, tempfile, os, hashlib, json
from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine

class FrozenMockProvider:
    def __init__(self):
        self.name="FrozenMock"; self.priority=0; self._fixture={}
    def check_health(self): return True
    def is_available(self): return True
    def supports_symbol(self, s): return True
    def best_provider(self, s): return self
    def get_data(self, symbol, interval="5m", period="5d"):
        key=f"{symbol}|{interval}"
        if key in self._fixture: return self._fixture[key].copy()
        seed=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)
        np.random.seed(seed)
        n_map={"1m":600,"5m":500,"15m":120,"1h":60,"4h":30}
        n=n_map.get(interval,100)
        closes=100+np.cumsum(np.random.randn(n)*2)
        highs=closes+np.abs(np.random.randn(n))
        lows=closes-np.abs(np.random.randn(n))
        opens=closes+np.random.randn(n)*0.3
        vols=np.abs(np.random.randn(n)*1000)+500
        idx=pd.date_range("2025-06-01",periods=n,freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[interval],tz="UTC")
        df=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols},index=idx)
        self._fixture[key]=df
        return df.copy()

def extract(r): 
    dec=r.decision
    confl=getattr(r, "confluence", None)
    confluence=None
    if confl is not None:
        confluence=getattr(confl,"weighted_score",None)
        if confluence is None: confluence=getattr(confl,"confluence_score",None)
    return (str(dec.decision), str(dec.grade), round(float(dec.confidence),6), round(float(confluence or 0),2), round(float(dec.buy_probability or 0),2), round(float(dec.sell_probability or 0),2))

# METHOD A: single pipeline sequential (baseline) vs same pipeline via wrapper (not per-symbol pipeline)
# This avoids singleton pollution entirely — single memory cache progressive is REAL behavior
print("METHOD A: single pipeline sequential (real behavior)")
InstitutionalMemoryEngine._instance=None
tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
tmp.write(b"[]"); tmp.close()
mock=FrozenMockProvider()
ms=MarketDataService(provider=mock)
pipe=AnalysisPipeline(market_service=ms, providers=[mock])
# override memory to tmp for isolation
pipe.memory.memory_path=tmp.name
pipe.decision_engine.memory.memory_path=tmp.name
pipe.memory._memory_cache=[]
pipe.decision_engine.memory._memory_cache=[]
pipe.mtf_engine.market_service=ms
pipe.profiler.active=False
symbols=["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","AUDUSD=X","NZDUSD=X"]
baseline={}
for s in symbols:
    r=pipe.analyze(s)
    baseline[s]=extract(r)
print(f"  baseline {baseline}")

# Now same pipe again with FRESH memory file but SAME sequence -> should be deterministic?
# Reset singleton and tmp
InstitutionalMemoryEngine._instance=None
tmp2=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
tmp2.write(b"[]"); tmp2.close()
mock2=FrozenMockProvider()
ms2=MarketDataService(provider=mock2)
pipe2=AnalysisPipeline(market_service=ms2, providers=[mock2])
pipe2.memory.memory_path=tmp2.name
pipe2.decision_engine.memory.memory_path=tmp2.name
pipe2.memory._memory_cache=[]
pipe2.decision_engine.memory._memory_cache=[]
pipe2.mtf_engine.market_service=ms2
pipe2.profiler.active=False
rerun={}
for s in symbols:
    r=pipe2.analyze(s)
    rerun[s]=extract(r)
print(f"  rerun   {rerun}")
print(f"  baseline == rerun? {baseline==rerun}")
for s in symbols:
    if baseline[s]!=rerun[s]:
        print(f"    MISMATCH {s} {baseline[s]} vs {rerun[s]}")

os.unlink(tmp.name); os.unlink(tmp2.name)

# METHOD B: per-symbol pipeline with FULL isolation (new mock + new singleton + new tmp each time)
# This is what frozen_equivalence did — and it fails because each symbol's memory starts empty vs progressive
# The CORRECT frozen determinism should compare: workers=1 sequential with per-symbol isolated vs workers=N isolated
# But baseline for Sprint 4 equivalence should be: same isolation level for baseline and optimized
print("\nMETHOD B: per-symbol isolated (baseline vs optimized with same isolation)")
def run_isolated_per_symbol(symbols, workers):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def one(sym):
        InstitutionalMemoryEngine._instance=None
        mock=FrozenMockProvider()
        ms=MarketDataService(provider=mock)
        tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
        tmp.write(b"[]"); tmp.close()
        pipe=AnalysisPipeline(market_service=ms, providers=[mock])
        pipe.memory.memory_path=tmp.name
        pipe.decision_engine.memory.memory_path=tmp.name
        pipe.memory._memory_cache=[]
        pipe.decision_engine.memory._memory_cache=[]
        pipe.mtf_engine.market_service=ms
        pipe.profiler.active=False
        r=pipe.analyze(sym)
        e=extract(r)
        os.unlink(tmp.name)
        InstitutionalMemoryEngine._instance=None
        return sym,e
    if workers==1:
        res={}
        for s in symbols:
            _,e=one(s)
            res[s]=e
        return res
    else:
        res={}
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs={ex.submit(one,s):s for s in symbols}
            for fut in as_completed(futs):
                sym,e=fut.result()
                res[sym]=e
        return res

# However singleton across threads races! So we need thread-safe singleton bypass
# For ThreadPool, InstitutionalMemoryEngine._instance is shared across threads — cannot isolate per-thread via singleton
# The frozen test above that fails for determinism is because threads share singleton!
# Let's test with workers=4 but sequential submission with lock on singleton creation?
print("\nMethod B workers=1")
InstitutionalMemoryEngine._instance=None
b_iso=run_isolated_per_symbol(symbols, workers=1)
print(f"  {b_iso}")
InstitutionalMemoryEngine._instance=None
print("Method B workers=4 (threaded, but singleton shared — RACE)")
o_iso=run_isolated_per_symbol(symbols, workers=4)
print(f"  {o_iso}")
print(f"  equal? {b_iso==o_iso}")
for s in symbols:
    if b_iso[s]!=o_iso[s]:
        print(f"    MISMATCH {s} iso1={b_iso[s]} iso4={o_iso[s]}")

print("\nConclusion: For frozen determinism, must use SINGLE pipeline sequential as GROUND TRUTH,")
print("or disable InstitutionalMemory (make it stateless) for frozen test.")
print("Live yfinance tests earlier already showed pipeline is deterministic when using single pipeline instance (Test2 PASS).")
