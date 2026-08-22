#!/usr/bin/env python3
"""Diagnostica por que frozen equivalence falha — isola InstitutionalMemory, snapshot, clock."""
import sys, hashlib, tempfile, os, json
from pathlib import Path
import pandas as pd, numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

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
        base={"EURUSD=X":1.08,"GBPUSD=X":1.27,"USDJPY=X":150.0}.get(symbol,100.0)
        closes=base+np.cumsum(np.random.randn(n)*base*0.002)
        highs=closes+np.abs(np.random.randn(n)*base*0.001)
        lows=closes-np.abs(np.random.randn(n)*base*0.001)
        opens=closes+np.random.randn(n)*base*0.0003
        vols=np.abs(np.random.randn(n)*1000)+500
        idx=pd.date_range("2025-06-01",periods=n,freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[interval],tz="UTC")
        df=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols},index=idx)
        self._fixture[key]=df
        return df.copy()

# Test 1: same MockProvider instance shared vs per-call new
print("Test 1: same fixture vs new provider with same seed")
m1=FrozenMockProvider()
m2=FrozenMockProvider()
df1=m1.get_data("EURUSD=X","5m")
df2=m2.get_data("EURUSD=X","5m")
print(f"  df1 len={len(df1)} close[-1]={df1['close'].iloc[-1]:.4f}")
print(f"  df2 len={len(df2)} close[-1]={df2['close'].iloc[-1]:.4f}")
print(f"  equal={(df1['close'].values==df2['close'].values).all()}")

# Test 2: pipeline analyze twice with SAME pipeline instance vs NEW pipeline
print("\nTest 2: same pipeline instance twice (memory pollution check)")
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
# Reset singleton
InstitutionalMemoryEngine._instance=None
InstitutionalMemoryEngine._lock=__import__("threading").Lock()
tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
tmp.write(b"[]"); tmp.close()
mock=FrozenMockProvider()
ms=MarketDataService(provider=mock)
pipe=AnalysisPipeline(market_service=ms, providers=[mock])
pipe.memory.memory_path=tmp.name
pipe.decision_engine.memory.memory_path=tmp.name
pipe.memory._memory_cache=[]; pipe.decision_engine.memory._memory_cache=[]
pipe.mtf_engine.market_service=ms
pipe.profiler.active=False
# monkey: isolate decision result
def extract(r):
    dec=r.decision
    return (str(dec.decision), str(dec.grade), round(float(dec.confidence),6), round(float(dec.buy_probability),4), round(float(dec.sell_probability),4))
r1=pipe.analyze("EURUSD=X")
e1=extract(r1)
r2=pipe.analyze("EURUSD=X")
e2=extract(r2)
print(f"  run1 {e1}")
print(f"  run2 {e2}")
print(f"  equal={e1==e2}")
os.unlink(tmp.name)

# Test 3: two NEW pipelines each with fresh mock + fresh memory file — should be equal if deterministic
print("\nTest 3: two NEW pipelines fresh memory")
def run_fresh(sym):
    InstitutionalMemoryEngine._instance=None
    mock=FrozenMockProvider()
    ms=MarketDataService(provider=mock)
    tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
    tmp.write(b"[]"); tmp.close()
    pipe=AnalysisPipeline(market_service=ms, providers=[mock])
    pipe.memory.memory_path=tmp.name
    pipe.decision_engine.memory.memory_path=tmp.name
    pipe.memory._memory_cache=[]; pipe.decision_engine.memory._memory_cache=[]
    pipe.mtf_engine.market_service=ms
    pipe.profiler.active=False
    r=pipe.analyze(sym)
    e=extract(r)
    os.unlink(tmp.name)
    return e
# Need to handle singleton: each call will share same instance unless reset before __init__
# Actually AnalysisPipeline.__init__ does self.memory=InstitutionalMemoryEngine() which returns singleton if not reset
# So we reset singleton BETWEEN creations
import threading
for sym in ["EURUSD=X","GBPUSD=X"]:
    InstitutionalMemoryEngine._instance=None
    e_a=run_fresh(sym)
    InstitutionalMemoryEngine._instance=None
    e_b=run_fresh(sym)
    print(f"  {sym} a={e_a} b={e_b} equal={e_a==e_b}  {'' if e_a==e_b else 'MISMATCH!'}")

# Test 4: check if DataNormalizer mutates df that is shared via fixture copy
print("\nTest 4: DataNormalizer idempotence")
mock=FrozenMockProvider()
df_a=mock.get_data("EURUSD=X","5m")
df_b=mock.get_data("EURUSD=X","5m")
print(f"  fixture copy isolation: df_a is df_b? {df_a is df_b}  values equal={(df_a['close'].values==df_b['close'].values).all()}")
from mercury_ai.data.data_normalizer import DataNormalizer
try:
    norm_a=DataNormalizer.normalize(df_a)
    norm_b=DataNormalizer.normalize(df_b)
    print(f"  normalized equal={(norm_a['Close'].values==norm_b['Close'].values).all() if 'Close' in norm_a else 'no Close'}")
except Exception as e:
    print(f"  normalizer error {e}")

print("\nDone. If Test2 shows equal=False, InstitutionalMemory or DecisionSnapshotLogger file pollution is cause.")
print("If Test3 shows equal=False despite fresh memory_path, then singleton not isolated or DataNormalizer side effect.")
