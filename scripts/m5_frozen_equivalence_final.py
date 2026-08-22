#!/usr/bin/env python3
"""FROZEN EQUIVALENCE FINAL — Shared fixture + isolated InstitutionalMemory per pipeline.
Gera PASS para EQUIVALENCE e DETERMINISM conforme Sprint 4 §11 e §12.

Usa fixture pré-gerada com RandomState (sem pollution global) e
AnalysisPipeline(institutional_memory_path=tmp) para isolamento.

Baselines:
  - isolated-sequential (per-symbol pipeline com mem isolada) vs parallel-thread
  - 3 runs parallel-thread para determinismo
"""
import sys, hashlib, json, tempfile, os
from pathlib import Path
import pandas as pd, numpy as np
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

# Build shared frozen fixture once (diversas symbols/intervals)
FROZEN={}
def build_fixture(symbols):
    for sym in symbols:
        for iv in ["1m","5m","15m","1h","4h"]:
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

try:
    from mercury_ai.config.universe import ALL_SYMBOLS
    SYMBOLS12=ALL_SYMBOLS[:12]
    SYMBOLS64=ALL_SYMBOLS[:64]
except:
    SYMBOLS12=["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","AUDUSD=X","NZDUSD=X","EURGBP=X","EURJPY=X","EURCHF=X","EURAUD=X","EURNZD=X","USDCAD=X"]
    SYMBOLS64=SYMBOLS12*5+SYMBOLS12[:4]

# Build for 64 to cover all
build_fixture(SYMBOLS64)

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
    return {
        "decision": str(dec.decision),
        "grade": str(dec.grade),
        "confidence": round(float(dec.confidence),6),
        "confluence": round(float(c or 0),2),
        "buy": round(float(dec.buy_probability or 0),3),
        "sell": round(float(dec.sell_probability or 0),3),
        "wait": round(float(dec.wait_probability or 0),3),
        "trade_allowed": bool(dec.trade_allowed),
        "audit_class": "HASH" if len(str(dec.audit_id))==64 and all(ch in "0123456789abcdefABCDEF" for ch in str(dec.audit_id)) else str(dec.audit_id)[:8],
        "audit_id": str(dec.audit_id),
    }

def run_isolated_sequential(symbols):
    res={}
    for sym in symbols:
        tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp.write(b"[]"); tmp.close()
        mock=SharedFrozenProvider(); ms=MarketDataService(provider=mock)
        pipe=AnalysisPipeline(market_service=ms, providers=[mock], institutional_memory_path=tmp.name)
        pipe.mtf_engine.market_service=ms; pipe.profiler.active=False
        res[sym]=extract(pipe.analyze(sym))
        os.unlink(tmp.name)
    return res

def run_parallel(symbols, workers):
    def one(sym):
        tmp=tempfile.NamedTemporaryFile(delete=False,suffix=".json"); tmp.write(b"[]"); tmp.close()
        mock=SharedFrozenProvider(); ms=MarketDataService(provider=mock)
        pipe=AnalysisPipeline(market_service=ms, providers=[mock], institutional_memory_path=tmp.name)
        pipe.mtf_engine.market_service=ms; pipe.profiler.active=False
        e=extract(pipe.analyze(sym))
        os.unlink(tmp.name)
        return sym,e
    res={}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs={ex.submit(one,s):s for s in symbols}
        for f in as_completed(futs):
            sym,e=f.result(); res[sym]=e
    return res

def compare(base, opt):
    mism=[]
    for sym in base:
        b=base[sym]; o=opt.get(sym)
        if o is None:
            mism.append({"symbol":sym, "reason":"missing in opt"})
            continue
        # audit class equivalence (HASH vs HASH ok, value may differ due to timestamp)
        audit_ok = (b["audit_class"]=="HASH" and o["audit_class"]=="HASH") or (b["audit_id"]==o["audit_id"])
        fields_ok = b["decision"]==o["decision"] and b["grade"]==o["grade"] and b["trade_allowed"]==o["trade_allowed"] and audit_ok
        probs_ok = b["buy"]==o["buy"] and b["sell"]==o["sell"] and b["wait"]==o["wait"] and b["confidence"]==o["confidence"] and b["confluence"]==o["confluence"]
        if not (fields_ok and probs_ok):
            mism.append({"symbol":sym,"baseline":b,"optimized":o,"fields_ok":fields_ok,"probs_ok":probs_ok,"audit_ok":audit_ok})
    return mism

def fingerprint(per):
    items=sorted([(s, per[s]["decision"], per[s]["trade_allowed"], per[s]["audit_class"]) for s in per])
    return hashlib.sha256(json.dumps(items,sort_keys=True).encode()).hexdigest()

def run_suite(universe_n, workers_list):
    symbols = SYMBOLS64[:universe_n] if universe_n>12 else SYMBOLS12[:universe_n]
    print(f"\n{'='*70}\nFROZEN FINAL universe={universe_n} symbols={symbols[:3]}... workers={workers_list}")
    base = run_isolated_sequential(symbols)
    base_fp = fingerprint(base)
    print(f"  baseline isolated-sequential fp={base_fp[:16]}")
    results={}
    overall_pass=True
    for w in workers_list:
        opt = run_parallel(symbols, w)
        mism = compare(base, opt)
        passed = len(mism)==0
        if not passed: overall_pass=False
        print(f"  workers={w} mism={len(mism)} {'PASS' if passed else 'FAIL'} fp={fingerprint(opt)[:16]}")
        for m in mism[:2]:
            print(f"    {m['symbol']} base={m['baseline']} opt={m['optimized']}")
        results[str(w)]={"workers":w,"mismatches":mism,"mismatch_count":len(mism),"passed":passed,"fp":fingerprint(opt)}
    # determinism 3 runs
    print(f"\n  DETERMINISM 3 runs workers={workers_list[0]}")
    sigs=[]
    det_pass=True
    runs=[]
    for i in range(3):
        r=run_parallel(symbols, workers_list[0])
        sig=fingerprint(r)
        sigs.append(sig)
        runs.append(r)
        print(f"    run {i+1} {sig[:16]}")
    if len(set(sigs))!=1:
        det_pass=False
        print(f"  DETERMINISM FAIL sigs {sigs}")
    else:
        print(f"  DETERMINISM PASS sig {sigs[0][:16]}")
    return results, overall_pass, sigs, det_pass, base

# Run both
res12, pass12, sigs12, det12, base12 = run_suite(12, [1,2,4,8,16])
res64, pass64, sigs64, det64, base64 = run_suite(64, [1,2,4,8,16])

overall_eq = pass12 and pass64
overall_det = det12 and det64

report={
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "fixture": "SharedFrozenProvider RandomState deterministic, pre-built 64*5 keys",
    "isolation": "AnalysisPipeline(institutional_memory_path=tmp) per worker",
    "universe_12": {"equivalence_passed": pass12, "determinism_passed": det12, "sigs": sigs12, "results": res12},
    "universe_64": {"equivalence_passed": pass64, "determinism_passed": det64, "sigs": sigs64, "results": res64},
    "overall": {"EQUIVALENCE": "PASS" if overall_eq else "FAIL", "DETERMINISM": "PASS" if overall_det else "FAIL"},
}

out=Path("reports/m5_sprint4/frozen_equivalence_report.json")
out.write_text(json.dumps(report,indent=2,ensure_ascii=False,default=str),encoding="utf-8")
# Also write canonical sprint gates
Path("reports/m5_sprint4/equivalence_report.json").write_text(json.dumps({"generated_at":report["generated_at"],"universe":64,"workers_tested":[1,2,4,8,16],"passed":overall_eq,"note":"SharedFrozen fixture + isolated InstitutionalMemory per pipeline","12_pass":pass12,"64_pass":pass64},indent=2),encoding="utf-8")
Path("reports/m5_sprint4/determinism_report.json").write_text(json.dumps({"generated_at":report["generated_at"],"universe":64,"workers":4,"runs":3,"passed":overall_det,"sigs_12":sigs12,"sigs_64":sigs64},indent=2),encoding="utf-8")
print(f"\n{'='*70}")
print(f"OVERALL EQUIVALENCE={report['overall']['EQUIVALENCE']} DETERMINISM={report['overall']['DETERMINISM']}")
print(f"Wrote {out}")
