#!/usr/bin/env python3
"""
FASE 7 — VALIDAÇÃO DE EQUIVALÊNCIA BASELINE vs OPTIMIZED
Snapshot congelado de dados (fixture sintética determinística) + comparação semântica
"""
import sys, json, copy, hashlib
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.config.timeframes import YFINANCE_INTERVALS
from mercury_ai.analysis.mtf_engine import MTFEngine
from mercury_ai.providers.market_provider import MercuryDataProvider

# Provider mockado: retorna DataFrame sintético determinístico por símbolo+intervalo
class MockProvider:
    def __init__(self, fixture: dict):
        self.name="Mock"
        self.fixture=fixture
        self.is_implemented=True
        self.priority=0
        self.supported_assets=list(fixture.keys())
    def check_health(self): return True
    def is_available(self): return True
    def supports_symbol(self, s): return True
    def best_provider(self, s): return self
    def get_data(self, symbol, interval="5m", period="5d"):
        key=f"{symbol}|{interval}"
        df=self.fixture.get(key)
        if df is None:
            # fallback: generate deterministic df
            np.random.seed(abs(hash(key))%2**32)
            n={"1m": 500, "5m": 120, "15m": 80, "1h": 60, "4h": 30}[interval]
            base={"BTC-USD": 60000, "ETH-USD": 3000, "EURUSD=X": 1.08, "USDJPY=X": 150.0, "AUDNZD=X": 1.07}.get(symbol, 100)
            closes = base + np.cumsum(np.random.randn(n)*base*0.002)
            highs = closes + np.abs(np.random.randn(n)*base*0.001)
            lows = closes - np.abs(np.random.randn(n)*base*0.001)
            opens = closes + np.random.randn(n)*base*0.0005
            vols = np.abs(np.random.randn(n)*1000)+500
            idx=pd.date_range("2025-01-01", periods=n, freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[interval])
            df=pd.DataFrame({"open":opens,"high":highs,"low":lows,"close":closes,"volume":vols}, index=idx)
            # DataNormalizer expects lowercase only (it creates Capitalized itself) — keep only lowercase to avoid duplicate col bug
            self.fixture[key]=df
        return df.copy()

# Build fixture
fixture={}
mock=MockProvider(fixture)
from mercury_ai.data.market_data import MarketDataService
ms=MarketDataService(providers=[mock])
# Use MTFEngine with mock provider via MarketDataService
engine = MTFEngine(providers=[mock])
# Monkey patch market_service to use our ms (providers list, no provider_manager)
engine.market_service = ms

OUT_JSON = Path("reports/m5_mtf_optimization/equivalence_report.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

symbols=["BTC-USD","ETH-USD","EURUSD=X","USDJPY=X","AUDNZD=X"]

def canonical(obj):
    # normalize for comparison: sort evidences by engine_name+direction
    if isinstance(obj, dict):
        return {k: canonical(v) for k,v in sorted(obj.items())}
    if isinstance(obj, list):
        try:
            return sorted([canonical(x) for x in obj], key=lambda y: json.dumps(y, sort_keys=True))
        except:
            return [canonical(x) for x in obj]
    return obj

def extract_semantic(evidences, consensus):
    # Build comparable dict
    ev_list=[]
    for e in evidences:
        ev_list.append({
            "engine": e.engine_name,
            "timeframe": e.timeframe,
            "direction": e.direction,
            "evidence_name": e.evidence_name,
            "strength": round(float(e.strength),4),
            "confidence": round(float(e.confidence),4),
            "weight": round(float(e.weight),4),
        })
    ev_list_sorted = sorted(ev_list, key=lambda x: (x["timeframe"], x["engine"], x["evidence_name"]))
    cons={
        "global_bias": consensus.global_bias,
        "local_bias": consensus.local_bias,
        "alignment_score": round(consensus.alignment_score,4),
        "conflict_score": round(consensus.conflict_score,4),
        "trend_alignment": round(consensus.trend_alignment,4),
        "liquidity_alignment": round(consensus.liquidity_alignment,4),
        "structure_alignment": round(consensus.structure_alignment,4),
        "volatility_alignment": round(consensus.volatility_alignment,4),
        "conflict_detected": consensus.conflict_detected,
        "timeframe_status": dict(consensus.timeframe_status),
    }
    return {"evidences": ev_list_sorted, "consensus": cons}

# Baseline: engine with use_parallel=False e sem reuse (main_m5_df=None) + original logic via evaluate
# To simulate baseline exactly, we call with use_parallel=False, main_m5_df=None
# Optimized: use_parallel=True, main_m5_df fetched (for M5 reuse)

results=[]

for sym in symbols:
    print(f"Checking {sym} ...")
    # Prepare main_m5_df via MarketDataService (normalized, as real pipeline does)
    main_m5 = ms.get_data(sym, interval="5m", period="5d")
    # BASELINE
    ev_base, cons_base = engine.analyze(sym, main_m5_df=None, use_parallel=False, max_workers=1)
    sem_base = extract_semantic(ev_base, cons_base)
    # OPTIMIZED (reuse via ms-normalized df)
    ev_opt, cons_opt = engine.analyze(sym, main_m5_df=main_m5, use_parallel=True, max_workers=2)
    sem_opt = extract_semantic(ev_opt, cons_opt)
    # Compare
    # Note: timeframe_errors reuse marker differs; we compare status only, not reuse marker
    # Remove reuse marker from comparison
    status_base = sem_base["consensus"]["timeframe_status"]
    status_opt = sem_opt["consensus"]["timeframe_status"]
    # Also need to compare evidences ignoring audit meta? We already extracted semantic.
    evid_match = sem_base["evidences"] == sem_opt["evidences"]
    consensus_match = sem_base["consensus"] == sem_opt["consensus"]
    # Deep compare with detailed diff
    diffs=[]
    if not evid_match:
        # find first mismatch
        set_base = {json.dumps(x, sort_keys=True) for x in sem_base["evidences"]}
        set_opt = {json.dumps(x, sort_keys=True) for x in sem_opt["evidences"]}
        diffs.append(f"evidences symmetric_diff base_only={len(set_base-set_opt)} opt_only={len(set_opt-set_base)}")
        # sample
        only_base=list(set_base-set_opt)[:2]
        only_opt=list(set_opt-set_base)[:2]
        diffs.append(f"  sample base_only: {only_base[:1]}")
        diffs.append(f"  sample opt_only: {only_opt[:1]}")
    if not consensus_match:
        for k in sem_base["consensus"]:
            if sem_base["consensus"][k] != sem_opt["consensus"][k]:
                diffs.append(f"consensus {k}: base={sem_base['consensus'][k]} opt={sem_opt['consensus'][k]}")
    passed = evid_match and consensus_match
    print(f"  -> {'PASS' if passed else 'FAIL'} evid_match={evid_match} consensus_match={consensus_match}")
    if diffs:
        for d in diffs: print("     ", d)
    results.append({
        "symbol": sym,
        "evid_count_base": len(ev_base),
        "evid_count_opt": len(ev_opt),
        "consensus_base": sem_base["consensus"],
        "consensus_opt": sem_opt["consensus"],
        "evid_match": evid_match,
        "consensus_match": consensus_match,
        "passed": passed,
        "diffs": diffs,
    })

# Also check with real structure evaluate equivalence (evaluate vs evaluate_with_swings on fixture)
print("\nChecking evaluate vs evaluate_with_swings direct ...")
from mercury_ai.analysis.market_structure_intelligence_engine import MarketStructureIntelligenceEngine
struct_eng = MarketStructureIntelligenceEngine()
direct_pass=True
for sym in symbols[:2]:
    for interval in ["1m","5m"]:
        df=mock.get_data(sym, interval=interval)
        swings, evs = struct_eng.swing_engine.detect_swings(df)
        prof1, evs1 = struct_eng.evaluate(df)
        prof2, evs2 = struct_eng.evaluate_with_swings(df, swings, evs)
        # Compare profiles and evidences counts/fields
        if prof1.classification != prof2.classification or abs(prof1.confidence_score - prof2.confidence_score)>1e-9:
            print(f"FAIL profile mismatch {sym} {interval}")
            direct_pass=False
        if len(evs1)!=len(evs2):
            print(f"FAIL ev count {sym} {interval}: {len(evs1)} vs {len(evs2)}")
            direct_pass=False
        # compare evidences sorted by name
        s1=sorted([(e.engine_name, e.evidence_name, e.direction) for e in evs1])
        s2=sorted([(e.engine_name, e.evidence_name, e.direction) for e in evs2])
        if s1!=s2:
            print(f"FAIL ev content {sym} {interval}")
            direct_pass=False
print(f"Direct evaluate equivalence: {'PASS' if direct_pass else 'FAIL'}")

overall_pass = all(r["passed"] for r in results) and direct_pass

report={
    "generated_at": pd.Timestamp.now(tz="UTC").isoformat(),
    "method": "fixture sintética determinística, baseline=sequential no-reuse vs optimized=parallel reuse",
    "symbols": symbols,
    "results": results,
    "direct_evaluate_with_swings": "PASS" if direct_pass else "FAIL",
    "overall": "PASS" if overall_pass else "FAIL",
    "note": "Audit_id ignorado (não existe em MTF). Comparação é semântica: evidences (engine/timeframe/direction/strength/confidence/weight) + consensus (bias/alignment/status)."
}

OUT_JSON.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nWrote {OUT_JSON}")
print(f"OVERALL EQUIVALENCE: {report['overall']}")
if not overall_pass:
    print("FAIL details above")
    sys.exit(1)
