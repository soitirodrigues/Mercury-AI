#!/usr/bin/env python3
"""FROZEN EQUIVALENCE V2 — fixture pré-gerada compartilhada + InstitutionalMemory isolada"""
import sys, hashlib, json, tempfile, os
from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

# Pre-generate frozen fixture once
FROZEN={}
def build_fixture(symbols, intervals=["1m","5m","15m","1h","4h"]):
    for sym in symbols:
        for iv in intervals:
            key=f"{sym}|{iv}"
            seed=int(hashlib.sha256(key.encode()).hexdigest()[:8],16)
            rs=np.random.RandomState(seed)
            n_map={"1m":600,"5m":500,"15m":120,"1h":60,"4h":30}
            n=n_map.get(iv,100)
            base=100
            closes=base+np.cumsum(rs.randn(n)*base*0.002)
            highs=closes+np.abs(rs.randn(n)*base*0.001)
            lows=closes-np.abs(rs.randn(n)*base*0.001)
            opens=closes+rs.randn(n)*base*0.0003
            vols=np.abs(rs.randn(n)*1000)+500
            idx=pd.date_range("2025-06-01",periods=n,freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[iv],tz="UTC")
            FROZEN[key]=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols},index=idx)
    print(f"Fixture built {len(FROZEN)} keys")

SYMBOLS12=["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","AUDUSD=X","NZDUSD=X","EURGBP=X","EURJPY=X","EURCHF=X","EURAUD=X","EURNZD=X","USDCAD=X"]

class SharedFrozenProvider:
    def __init__(self): self.name="SharedFrozen"; self.priority=0
    def check_health(self): return True
    def is_available(self): return True
    def supports_symbol(self,s): return True
    def best_provider(self,s): return self
    def get_data(self, symbol, interval="5m", period="5d"):
        key=f"{symbol}|{interval}"
        df=FROZEN.get(key)
        if df is None: raise KeyError(key)
        return df.copy()

def extract(r):
    dec=r.decision
    confl=getattr(r,"confluence",None)
    c=getattr(confl,"weighted_score",None) if confl else None
    if c is None and confl: c=getattr(confl,"confluence_score",None)
    return (str(dec.decision), str(dec.grade), round(float(dec.confidence),6), round(float(c or 0),2), round(float(dec.buy_probability or 0),3), round(float(dec.sell_probability or 0),3), round(float(dec.wait_probability or 0),3))

build_fixture(SYMBOLS12)

# Test A: same pipeline sequential twice
print("\n=== TEST A: same pipeline same symbol twice ===")
tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp.write(b"[]"); tmp.close()
mock=SharedFrozenProvider(); ms=MarketDataService(provider=mock)
pipe=AnalysisPipeline(market_service=ms, providers=[mock], institutional_memory_path=tmp.name)
pipe.mtf_engine.market_service=ms; pipe.profiler.active=False
r1=pipe.analyze("EURUSD=X"); e1=extract(r1)
r2=pipe.analyze("EURUSD=X"); e2=extract(r2)
print(f"  e1={e1} e2={e2} equal={e1==e2}")
os.unlink(tmp.name)
print("  PASS" if e1==e2 else "  FAIL")

# Test B: two fresh pipelines same symbol
print("\n=== TEST B: two fresh pipelines same symbol ===")
for i in range(2):
    tmp2=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp2.write(b"[]"); tmp2.close()
    mock2=SharedFrozenProvider(); ms2=MarketDataService(provider=mock2)
    pipe2=AnalysisPipeline(market_service=ms2, providers=[mock2], institutional_memory_path=tmp2.name)
    pipe2.mtf_engine.market_service=ms2; pipe2.profiler.active=False
    r=pipe2.analyze("EURUSD=X")
    print(f"  run {i} {extract(r)} mem {len(pipe2._isolated_memory._memory_cache)}")
    os.unlink(tmp2.name)

# Test C: sequential single pipeline vs per-symbol isolated
print("\n=== TEST C: sequential single pipeline (ground truth) ===")
tmp3=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp3.write(b"[]"); tmp3.close()
mock3=SharedFrozenProvider(); ms3=MarketDataService(provider=mock3)
pipe3=AnalysisPipeline(market_service=ms3, providers=[mock3], institutional_memory_path=tmp3.name)
pipe3.mtf_engine.market_service=ms3; pipe3.profiler.active=False
seq={}
for s in SYMBOLS12[:6]:
    seq[s]=extract(pipe3.analyze(s))
print(f"  seq {seq}")
os.unlink(tmp3.name)

print("\n=== TEST C2: per-symbol isolated pipelines ===")
iso={}
for s in SYMBOLS12[:6]:
    tmp4=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp4.write(b"[]"); tmp4.close()
    mock4=SharedFrozenProvider(); ms4=MarketDataService(provider=mock4)
    pipe4=AnalysisPipeline(market_service=ms4, providers=[mock4], institutional_memory_path=tmp4.name)
    pipe4.mtf_engine.market_service=ms4; pipe4.profiler.active=False
    iso[s]=extract(pipe4.analyze(s))
    os.unlink(tmp4.name)
print(f"  iso {iso}")
for s in SYMBOLS12[:6]:
    print(f"  {s} seq={seq[s]} iso={iso[s]} eq={seq[s]==iso[s]}")

# Note: seq vs iso may differ because sequential accumulates memory across symbols (though memory len 0 suggests not affecting?)
# Let's check memory contents after seq
print("\n=== TEST D: parallel ThreadPool with shared fixture ===")
from concurrent.futures import ThreadPoolExecutor, as_completed
def one_thread(sym):
    tmp5=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp5.write(b"[]"); tmp5.close()
    mock5=SharedFrozenProvider(); ms5=MarketDataService(provider=mock5)
    pipe5=AnalysisPipeline(market_service=ms5, providers=[mock5], institutional_memory_path=tmp5.name)
    pipe5.mtf_engine.market_service=ms5; pipe5.profiler.active=False
    r=pipe5.analyze(sym)
    e=extract(r)
    os.unlink(tmp5.name)
    return sym, e

par={}
with ThreadPoolExecutor(max_workers=4) as ex:
    futs={ex.submit(one_thread,s):s for s in SYMBOLS12[:6]}
    for f in as_completed(futs):
        sym,e=f.result(); par[sym]=e
print(f"  par {par}")
for s in SYMBOLS12[:6]:
    print(f"  {s} seq={seq[s]} par={par[s]} eq={seq[s]==par[s]}")

# Equivalence between sequential-isolated-per-symbol and parallel-thread should be deterministic if memory isolated
# But seq here is progressive memory; iso/par is per-symbol isolated. To make fair, baseline should ALSO be per-symbol isolated sequential
print("\n=== TEST E: baseline per-symbol isolated sequential vs parallel thread ===")
base_iso={}
for s in SYMBOLS12[:6]:
    tmp6=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp6.write(b"[]"); tmp6.close()
    mock6=SharedFrozenProvider(); ms6=MarketDataService(provider=mock6)
    pipe6=AnalysisPipeline(market_service=ms6, providers=[mock6], institutional_memory_path=tmp6.name)
    pipe6.mtf_engine.market_service=ms6; pipe6.profiler.active=False
    base_iso[s]=extract(pipe6.analyze(s))
    os.unlink(tmp6.name)
print(f"  base_iso {base_iso}")
print(f"  par      {par}")
equal=all(base_iso[s]==par[s] for s in SYMBOLS12[:6])
print(f"  EQUIVALENCE isolated-sequential vs parallel-thread: {'PASS' if equal else 'FAIL'}")
for s in SYMBOLS12[:6]:
    if base_iso[s]!=par[s]:
        print(f"    MISMATCH {s} base={base_iso[s]} par={par[s]}")

# Determinism: 3 runs parallel-thread should be identical
print("\n=== TEST F: determinism 3 runs parallel-thread ===")
sigs=[]
for run in range(3):
    run_par={}
    with ThreadPoolExecutor(max_workers=4) as ex:
        futs={ex.submit(one_thread,s):s for s in SYMBOLS12[:6]}
        for f in as_completed(futs):
            sym,e=f.result(); run_par[sym]=e
    sig=hashlib.sha256(json.dumps(sorted(run_par.items()),sort_keys=True).encode()).hexdigest()[:12]
    sigs.append(sig)
    print(f"  run {run+1} sig {sig} {run_par}")
print(f"  determinism {'PASS' if len(set(sigs))==1 else 'FAIL'} sigs {sigs}")
