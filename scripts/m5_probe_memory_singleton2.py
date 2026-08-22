import sys, tempfile, os, hashlib
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

def extract(r): dec=r.decision; return (str(dec.decision), round(float(dec.confidence),8))

# Test: reset singleton, create pipeline A, analyze EURUSD, then WITHOUT resetting singleton, create pipeline B and analyze EURUSD
# Are they equal? The earlier test said NO — meaning singleton state leaks
print("Test: singleton reuse across pipelines")
# Start clean
InstitutionalMemoryEngine._instance=None
import threading
InstitutionalMemoryEngine._lock=threading.Lock()
tmp1=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
tmp1.write(b"[]"); tmp1.close()
mock1=FrozenMockProvider()
ms1=MarketDataService(provider=mock1)
pipe1=AnalysisPipeline(market_service=ms1, providers=[mock1])
# pipe1 singleton now exists, backed by data/institutional_memory.json or whatever path it loaded
# Let's check what file it's using and what's in cache
print(f"  pipe1 memory_path={pipe1.memory.memory_path} cache_len={len(pipe1.memory._memory_cache)} id={id(pipe1.memory)}")
r1=pipe1.analyze("EURUSD=X")
print(f"  after 1st analyze cache_len={len(pipe1.memory._memory_cache)} id={id(pipe1.memory)} extract={extract(r1)}")
# Now create pipe2 WITHOUT resetting singleton — should reuse same object
mock2=FrozenMockProvider()
ms2=MarketDataService(provider=mock2)
pipe2=AnalysisPipeline(market_service=ms2, providers=[mock2])
print(f"  pipe2 memory_path={pipe2.memory.memory_path} cache_len={len(pipe2.memory._memory_cache)} id={id(pipe2.memory)} same_obj={pipe1.memory is pipe2.memory}")
r2=pipe2.analyze("EURUSD=X")
print(f"  pipe2 analyze EURUSD extract={extract(r2)} cache_len={len(pipe2.memory._memory_cache)}")
print(f"  pipe1 vs pipe2 equal={extract(r1)==extract(r2)}")

print("\nTest same pipe twice (should be equal as earlier):")
# Same pipe twice with same memory
r3=pipe1.analyze("EURUSD=X")
print(f"  pipe1 second EURUSD {extract(r3)} vs first {extract(r1)} equal={extract(r3)==extract(r1)}")

print("\nTest: snapshot_logger also singleton?")
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
print(f"  snapshot_logger id pipe1={id(pipe1.snapshot_logger)} pipe2={id(pipe2.snapshot_logger)} same={pipe1.snapshot_logger is pipe2.snapshot_logger}")

os.unlink(tmp1.name)
# Reset
InstitutionalMemoryEngine._instance=None
print("\nDone")
