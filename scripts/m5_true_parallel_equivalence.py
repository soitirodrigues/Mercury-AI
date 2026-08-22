#!/usr/bin/env python3
"""
EQUIVALENCE verdadeira para Sprint 4 — snapshot congelado mas SEM drift de yfinance
e SEM pollution de InstitutionalMemory mal isolado.

Para equivalência canônica, o contrato diz: pipeline OFICIAL identico, apenas
paralelismo inter-asset. A forma correta de comparar é:

- Baseline workers=1 via ParallelScanner com 1 worker (cada worker tem seu pipeline isolado mas memória vazia)
- Optimized workers=N via ParallelScanner com N workers (mesma isolação)

Ambos passam pelo mesmo `ParallelScanner` path — única diferença é workers count.
Se equivalência falhar, é bug de thread-safety (memória compartilhada, profiler global).

Para determinismo, 3 runs workers=N devem dar mesmo Top-3 final (audit hash class equivalence).
"""
import sys, json, hashlib
from pathlib import Path
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.m5_inter_asset_parallel_scanner import ParallelScanner
from mercury_ai.config.universe import ALL_SYMBOLS

def fingerprint(per_asset):
    # Use decision+grade+trade_allowed+prob sum hash class equivalence
    items=[]
    for sym in sorted(per_asset):
        r=per_asset[sym]
        audit=r.get("audit_id") or ""
        is_hash=len(audit)==64 and all(c in "0123456789abcdefABCDEF" for c in audit)
        items.append((sym, r.get("decision"), r.get("grade"), r.get("trade_allowed"), "HASH" if is_hash else audit[:8], round(float(r.get("confidence") or 0),2), round(float(r.get("confluence") or 0),1)))
    return hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()

def run(universe_n, workers):
    from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
    # Reset singleton before each run to avoid pollution across runs
    InstitutionalMemoryEngine._instance=None
    symbols=ALL_SYMBOLS[:universe_n]
    sc=ParallelScanner(symbols, workers=workers, executor_type="thread", disable_profiler=True)
    res=sc.scan()
    # reset after
    InstitutionalMemoryEngine._instance=None
    return res

# 12 assets
print("EQUIVALENCE 12 assets workers=1 vs 4 and vs 8")
for n in [12, 64]:
    print(f"\n{'='*70}\nUniverse {n}")
    base=run(n, 1)
    base_fp=fingerprint(base.get("per_asset",{}))
    base_top3=[(r.get("symbol"),r.get("decision")) for r in base.get("top3",[])]
    print(f"  baseline workers=1 fp={base_fp[:16]} top3={base_top3} wall={base.get('wall_s')}s")
    for w in [2,4,8]:
        opt=run(n, w)
        opt_fp=fingerprint(opt.get("per_asset",{}))
        opt_top3=[(r.get("symbol"),r.get("decision")) for r in opt.get("top3",[])]
        # Detailed compare: same decision+status class?
        per_base=base.get("per_asset",{}); per_opt=opt.get("per_asset",{})
        mism=[]
        for sym in ALL_SYMBOLS[:n]:
            b=per_base.get(sym,{}); o=per_opt.get(sym,{})
            # status class equivalence: both REAL_SIGNAL or both DATA_UNAVAILABLE etc.
            if b.get("status")!=o.get("status"):
                mism.append(f"{sym} status {b.get('status')} vs {o.get('status')}")
            elif b.get("decision")!=o.get("decision"):
                mism.append(f"{sym} decision {b.get('decision')} vs {o.get('decision')}")
            # audit class
            ba=b.get("audit_id") or ""; oa=o.get("audit_id") or ""
            ba_hash=len(ba)==64 and all(c in "0123456789abcdefABCDEF" for c in ba)
            oa_hash=len(oa)==64 and all(c in "0123456789abcdefABCDEF" for c in oa)
            if ba_hash!=oa_hash:
                mism.append(f"{sym} audit class hash {ba_hash} vs {oa_hash}")
        passed=len(mism)==0
        print(f"  workers={w} fp={opt_fp[:16]} top3={opt_top3} wall={opt.get('wall_s')}s -> {'PASS' if passed else 'FAIL'} mism={mism[:3]}")

# Determinism 3 runs same workers
print(f"\n{'='*70}\nDETERMINISM 12 workers=4 runs=3 (fingerprint)")
fps=[]
for i in range(3):
    r=run(12,4)
    fp=fingerprint(r.get("per_asset",{}))
    fps.append(fp)
    print(f"  run {i+1} fp={fp[:16]} top3={[x.get('symbol') for x in r.get('top3',[])]}")
print(f"  all equal? {len(set(fps))==1}")

# Write report
report={
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "note": "Fingerprint usa decision+grade+trade_allowed+audit hash class — ignora prob float drift dentro de 0.01 e audit hash value",
    "12_workers1_vs_4": "see above",
}
Path("reports/m5_sprint4/true_equivalence_probe.json").write_text(json.dumps({"fps":fps}, indent=2), encoding="utf-8")
