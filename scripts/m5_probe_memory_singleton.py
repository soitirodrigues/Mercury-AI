import sys, tempfile, os, hashlib, threading
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
        base=100
        closes=base+np.cumsum(np.random.randn(n)*base*0.002)
        highs=closes+np.abs(np.random.randn(n)*base*0.001)
        lows=closes-np.abs(np.random.randn(n)*base*0.001)
        opens=closes+np.random.randn(n)*base*0.0003
        vols=np.abs(np.random.randn(n)*1000)+500
        idx=pd.date_range("2025-06-01",periods=n,freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[interval],tz="UTC")
        df=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols},index=idx)
        self._fixture[key]=df
        return df.copy()

def extract(r): dec=r.decision; return (str(dec.decision), str(dec.grade), round(float(dec.confidence),8))

# With singleton reset INSIDE run_fresh before creating pipeline, does it become deterministic?
def run_fresh_isolated(sym, reset_before=True):
    if reset_before:
        InstitutionalMemoryEngine._instance=None
    mock=FrozenMockProvider()
    ms=MarketDataService(provider=mock)
    tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
    tmp.write(b"[]"); tmp.close()
    pipe=AnalysisPipeline(market_service=ms, providers=[mock])
    # After pipeline created, its memory is the singleton. Now override path
    pipe.memory.memory_path=tmp.name
    pipe.decision_engine.memory.memory_path=tmp.name
    pipe.memory._memory_cache=[]
    pipe.decision_engine.memory._memory_cache=[]
    pipe.mtf_engine.market_service=ms
    pipe.profiler.active=False
    r=pipe.analyze(sym)
    e=extract(r)
    os.unlink(tmp.name)
    # Check: are pipe.memory and pipe.decision_engine.memory same object? singleton => yes
    same = pipe.memory is pipe.decision_engine.memory
    return e, same, id(pipe.memory)

print("Testing singleton isolation")
for i in range(3):
    InstitutionalMemoryEngine._instance=None
    e1, same1, id1 = run_fresh_isolated("EURUSD=X", reset_before=False)  # internal reset
    # Now without resetting between runs, second call will reuse same singleton instance!
    # Because run_fresh_isolated does NOT reset before if reset_before=False, but we did reset outside
    # Let's test WITHOUT outer reset:
    e2, same2, id2 = run_fresh_isolated("EURUSD=X", reset_before=False)
    print(f"  iter {i} e1={e1} id1={id1} same={same1} | e2={e2} id2={id2} same={same2} equal={e1==e2} same_obj={id1==id2}")

print("\nWith outer reset each time (correct):")
for i in range(3):
    InstitutionalMemoryEngine._instance=None
    e1,_ ,id1 = run_fresh_isolated("EURUSD=X", reset_before=False)
    InstitutionalMemoryEngine._instance=None
    e2,_,id2 = run_fresh_isolated("EURUSD=X", reset_before=False)
    print(f"  {e1} vs {e2} equal={e1==e2} ids {id1} vs {id2}")

print("\nNow same pipeline instance twice (should be deterministic as Test2 showed):")
InstitutionalMemoryEngine._instance=None
tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json")
tmp.write(b"[]"); tmp.close()
mock=FrozenMockProvider()
ms=MarketDataService(provider=mock)
pipe=AnalysisPipeline(market_service=ms, providers=[mock])
pipe.memory.memory_path=tmp.name
pipe.decision_engine.memory.memory_path=tmp.name
pipe.memory._memory_cache=[]
pipe.decision_engine.memory._memory_cache=[]
pipe.mtf_engine.market_service=ms
pipe.profiler.active=False
e1=extract(pipe.analyze("EURUSD=X"))
e2=extract(pipe.analyze("EURUSD=X"))
e3=extract(pipe.analyze("GBPUSD=X"))
e4=extract(pipe.analyze("GBPUSD=X"))
print(f"  EURUSD twice: {e1} vs {e2} equal={e1==e2}")
print(f"  GBPUSD twice: {e3} vs {e4} equal={e3==e4}")
os.unlink(tmp.name)
print("\nConclusion: non-determinism comes from pipeline creation with singleton shared state, not from logic.")
