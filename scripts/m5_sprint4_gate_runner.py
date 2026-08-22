#!/usr/bin/env python3
"""GATE RUNNER Sprint4 — roda regression gates leves e preserva fixtures existentes"""
import sys, subprocess, json, pathlib
from datetime import datetime, timezone

ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

gates=[]
def run_gate(name, cmd):
    print(f"\n=== GATE {name}: {' '.join(cmd)} ===")
    r=subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    ok=r.returncode==0
    print(r.stdout[-4000:] if r.stdout else "")
    if r.stderr:
        print(r.stderr[-3000:])
    print(f"GATE {name}: {'PASS' if ok else 'FAIL'} (exit {r.returncode})")
    gates.append({"gate":name,"pass":ok,"exit":r.returncode})
    return ok

# 1) top3_scanner
run_gate("top3_scanner", [sys.executable, "scripts/top3_scanner.py"])
run_gate("top3_determinism", [sys.executable, "scripts/top3_determinism_test.py"])

# 2) pytest gates que existem — rodar m5_incremental e ranking leve
run_gate("pytest_m5_incremental", [sys.executable, "-m", "pytest", "tests/test_m5_incremental.py", "-q"])
run_gate("pytest_m5_ranking", [sys.executable, "-m", "pytest", "-q", "-k", "ranking or Ranking"])

# 3) Verificar Fixtures: FRESHNESS_GATE não aceita STALE como FRESH — já coberto em early_emission stal
import json
try:
    ee=json.loads(pathlib.Path("reports/m5_sprint4/early_emission_report.json").read_text())
    ok=ee.get("stale_as_fresh",1)==0
    gates.append({"gate":"FRESHNESS_GATE","pass":ok,"exit":0 if ok else 1})
    print(f"\nGATE FRESHNESS_GATE: {'PASS' if ok else 'FAIL'} stale_as_fresh={ee.get('stale_as_fresh')}")
except Exception as e:
    gates.append({"gate":"FRESHNESS_GATE","pass":False,"exit":1,"error":str(e)})

# DECISION_INTEGRITY / PROBABILITY_SUM / RESOLVER_INTEGRITY já validados no pipeline via classify_status / prob_sum_ok
# Mas rodar pytest decision se existir
run_gate("pytest_decision", [sys.executable, "-m", "pytest", "-q", "-k", "decision"])

overall=all(g["pass"] for g in gates)
out={"generated_at":datetime.now(timezone.utc).isoformat(),"gates":gates,"overall": "PASS" if overall else "FAIL"}
path=ROOT/"reports/m5_sprint4/regression_gates.json"
path.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding="utf-8")
print(f"\nWrote {path}")
print(json.dumps(out,indent=2))
