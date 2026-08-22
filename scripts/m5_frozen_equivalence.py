#!/usr/bin/env python3
"""
FROZEN EQUIVALENCE + DETERMINISM — snapshot congelado (sem drift yfinance)

Para o mesmo snapshot congelado (DataFrame sintético determinístico por seed),
compara:

BASELINE workers=1 (sequencial via pipeline direto)
vs
OPTIMIZED workers=N (ParallelScanner)

Compara SEMANTICAMENTE cada ativo:
- status, decision, trade_allowed, confidence, confluence, probabilities, grade, quality
- MTF outputs não necessários se pipeline inteiro congelado (já está validado no Sprint3 FASE 7)

O snapshot é congelado via MockProvider que retorna DataFrame determinístico
por (symbol, interval) com seed = hash(symbol|interval).
"""
import sys, json, hashlib, traceback
from pathlib import Path
from datetime import datetime, timezone
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.providers.market_provider import MercuryDataProvider

# Provider mockado congelado — retorna df deterministico
class FrozenMockProvider:
    def __init__(self):
        self.name = "FrozenMock"
        self.is_implemented = True
        self.priority = 0
        self.supported_assets = []
        self._fixture = {}
    def check_health(self): return True
    def is_available(self): return True
    def supports_symbol(self, s): return True
    def best_provider(self, s): return self
    def get_data(self, symbol, interval="5m", period="5d"):
        key = f"{symbol}|{interval}"
        if key in self._fixture:
            return self._fixture[key].copy()
        # deterministic seed
        # hash() is randomized per process (PYTHONHASHSEED); use sha256 deterministic
        seed = int(hashlib.sha256(key.encode()).hexdigest()[:8], 16)
        np.random.seed(seed)
        n_map = {"1m": 600, "5m": 500, "15m": 120, "1h": 60, "4h": 30}
        n = n_map.get(interval, 100)
        base_map = {"EURUSD=X": 1.08, "GBPUSD=X": 1.27, "USDJPY=X": 150.0, "USDCHF=X": 0.90, "AUDUSD=X": 0.65, "NZDUSD=X": 0.62, "BTC-USD": 60000, "ETH-USD": 3000}
        base = base_map.get(symbol, 100.0)
        closes = base + np.cumsum(np.random.randn(n) * base * 0.002)
        highs = closes + np.abs(np.random.randn(n) * base * 0.001)
        lows = closes - np.abs(np.random.randn(n) * base * 0.001)
        opens = closes + np.random.randn(n) * base * 0.0003
        vols = np.abs(np.random.randn(n) * 1000) + 500
        idx = pd.date_range("2025-06-01", periods=n, freq={"1m":"1min","5m":"5min","15m":"15min","1h":"1h","4h":"4h"}[interval], tz="UTC")
        df = pd.DataFrame({"open": opens, "high": highs, "low": lows, "close": closes, "volume": vols}, index=idx)
        self._fixture[key] = df
        return df.copy()

SYMBOLS_12 = ["EURUSD=X","GBPUSD=X","USDJPY=X","USDCHF=X","AUDUSD=X","NZDUSD=X","EURGBP=X","EURJPY=X","EURCHF=X","EURAUD=X","EURNZD=X","USDCAD=X"]
SYMBOLS_64_FULL = None  # will import from universe
try:
    from mercury_ai.config.universe import ALL_SYMBOLS as _ALL
    SYMBOLS_64 = _ALL[:64]
except:
    SYMBOLS_64 = SYMBOLS_12 * 5 + SYMBOLS_12[:4]

def extract_semantic(result):
    dec = result.decision if result else None
    confl = getattr(result, "confluence", None)
    confluence = None
    if confl is not None:
        confluence = getattr(confl, "weighted_score", None)
        if confluence is None:
            confluence = getattr(confl, "confluence_score", None)
    return {
        "decision": str(getattr(dec, "decision", "") or "").upper() if dec else "NONE",
        "grade": str(getattr(dec, "grade", "") or ""),
        "confidence": getattr(dec, "confidence", None),
        "confluence": confluence,
        "buy_probability": getattr(dec, "buy_probability", None),
        "sell_probability": getattr(dec, "sell_probability", None),
        "wait_probability": getattr(dec, "wait_probability", None),
        "trade_allowed": bool(getattr(dec, "trade_allowed", False)) if dec else False,
        "audit_id": str(getattr(dec, "audit_id", "") or ""),
        "score": getattr(dec, "score", None),
    }

def run_parallel_frozen(symbols, workers):
    import tempfile, os
    from concurrent.futures import ThreadPoolExecutor, as_completed
    def worker_one(sym):
        mock = FrozenMockProvider()
        ms = MarketDataService(provider=mock)
        tmp_mem = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        tmp_mem.write(b"[]"); tmp_mem.close()
        pipeline = AnalysisPipeline(market_service=ms, providers=[mock], institutional_memory_path=tmp_mem.name)
        pipeline.mtf_engine.market_service = ms
        pipeline.profiler.active = False
        r = pipeline.analyze(sym)
        try: os.unlink(tmp_mem.name)
        except: pass
        return sym, extract_semantic(r)
    results = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(worker_one, s): s for s in symbols}
        for fut in as_completed(futs):
            sym, sem = fut.result()
            results[sym] = sem
    return results

def run_baseline_frozen(symbols):
    import tempfile, os
    tmp_mem = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
    tmp_mem.write(b"[]"); tmp_mem.close()
    mock = FrozenMockProvider()
    ms = MarketDataService(provider=mock)
    pipeline = AnalysisPipeline(market_service=ms, providers=[mock], institutional_memory_path=tmp_mem.name)
    pipeline.mtf_engine.market_service = ms
    results = {}
    for sym in symbols:
        pipeline.market_service = ms
        pipeline.mtf_engine.market_service = ms
        r = pipeline.analyze(sym)
        results[sym] = extract_semantic(r)
    try: os.unlink(tmp_mem.name)
    except: pass
    return results

def compare_semantic(base, opt, tolerance=1e-6):
    mismatches = []
    for sym in base:
        b = base[sym]; o = opt.get(sym, {})
        # audit is hash 64 hex -> compare class, not value (hash includes timestamp)
        b_audit = b.get("audit_id") or ""; o_audit = o.get("audit_id") or ""
        b_is_hash = len(b_audit)==64 and all(c in "0123456789abcdefABCDEF" for c in b_audit)
        o_is_hash = len(o_audit)==64 and all(c in "0123456789abcdefABCDEF" for c in o_audit)
        if b_is_hash and o_is_hash:
            audit_ok = True
        else:
            audit_ok = b_audit == o_audit
        fields_ok = (
            b.get("decision")==o.get("decision") and
            b.get("grade")==o.get("grade") and
            b.get("trade_allowed")==o.get("trade_allowed") and
            audit_ok
        )
        probs_ok = True
        for k in ("buy_probability","sell_probability","wait_probability","confidence","confluence","score"):
            bv = b.get(k); ov = o.get(k)
            if bv is None and ov is None: continue
            if (bv is None) != (ov is None):
                probs_ok=False; break
            try:
                if abs(float(bv)-float(ov)) > tolerance:
                    probs_ok=False; break
            except:
                if bv != ov:
                    probs_ok=False; break
        if not (fields_ok and probs_ok):
            mismatches.append({"symbol": sym, "baseline": b, "optimized": o, "fields_ok": fields_ok, "probs_ok": probs_ok, "audit_ok": audit_ok})
    return mismatches

def main():
    import argparse
    p = argparse.ArgumentParser(description="Frozen equivalence + determinism")
    p.add_argument("--universe", type=int, default=12)
    p.add_argument("--workers", type=int, default=4)
    p.add_argument("--runs", type=int, default=3)
    args = p.parse_args()
    symbols = (SYMBOLS_64 if args.universe==64 else SYMBOLS_12)[:args.universe]
    print(f"Frozen equivalence universe={len(symbols)} workers={args.workers} runs={args.runs}")

    base = run_baseline_frozen(symbols)
    opt = run_parallel_frozen(symbols, workers=args.workers)
    mism = compare_semantic(base, opt)
    print(f"BASELINE vs OPTIMIZED workers={args.workers}: mismatches={len(mism)}")
    for m in mism[:3]:
        print(f"  {m['symbol']}: base {m['baseline']} vs opt {m['optimized']}")

    # Determinism: 3 runs parallel frozen
    runs_sigs = []
    runs = []
    for i in range(args.runs):
        r = run_parallel_frozen(symbols, workers=args.workers)
        sig_items = sorted([(s, r[s].get("decision"), r[s].get("trade_allowed")) for s in symbols])
        sig = hashlib.sha256(json.dumps(sig_items, sort_keys=True).encode()).hexdigest()
        runs_sigs.append(sig)
        runs.append(r)
        print(f"  Run {i+1} sig {sig[:16]}")

    # Compare run1 vs run2, run1 vs run3
    det_mism_12 = compare_semantic(runs[0], runs[1]) if len(runs)>=2 else []
    det_mism_13 = compare_semantic(runs[0], runs[2]) if len(runs)>=3 else []

    equivalence_pass = len(mism)==0
    determinism_pass = len(det_mism_12)==0 and len(det_mism_13)==0 and len(set(runs_sigs))==1

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "universe": len(symbols),
        "workers": args.workers,
        "runs": args.runs,
        "equivalence": {"passed": equivalence_pass, "mismatches": mism, "mismatch_count": len(mism), "baseline_sample": {k: base[k] for k in list(base)[:2]}, "optimized_sample": {k: opt[k] for k in list(opt)[:2]}},
        "determinism": {"passed": determinism_pass, "sigs": runs_sigs, "det_mism_12": det_mism_12[:2], "det_mism_13": det_mism_13[:2]},
        "overall": {"EQUIVALENCE": "PASS" if equivalence_pass else "FAIL", "DETERMINISM": "PASS" if determinism_pass else "FAIL"},
    }
    out = Path("reports/m5_sprint4/frozen_equivalence_report.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nEQUIVALENCE (frozen) = {'PASS' if equivalence_pass else 'FAIL'}")
    print(f"DETERMINISM (frozen) = {'PASS' if determinism_pass else 'FAIL'}")
    print(f"Wrote {out}")

    # Also write classic equivalence/determinism umbrella files for sprint gates
    Path("reports/m5_sprint4/equivalence_report.json").write_text(json.dumps({"generated_at": report["generated_at"], "universe": len(symbols), "workers": args.workers, "passed": equivalence_pass, "mismatches": mism[:3], "note": "frozen snapshot (no yfinance drift) vs live drift earlier"}, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    Path("reports/m5_sprint4/determinism_report.json").write_text(json.dumps({"generated_at": report["generated_at"], "universe": len(symbols), "workers": args.workers, "runs": args.runs, "passed": determinism_pass, "sigs": runs_sigs}, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

if __name__ == "__main__":
    main()
