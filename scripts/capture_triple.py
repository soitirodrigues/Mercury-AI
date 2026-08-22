import sys, pathlib, time, json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mercury_ai.brain.scanner import MercuryScanner

max_tries=30
delay=65
for attempt in range(1, max_tries+1):
    sc=MercuryScanner()
    traces={}
    for sym in ["BTC-USD","ETH-USD","GC=F"]:
        try:
            r=sc.pipeline.analyze(sym)
            traces[sym]=(r.decision.decision, r.decision.grade, round(r.confluence.weighted_score,1) if hasattr(r.confluence,'weighted_score') else 0, r.decision.audit_id)
        except Exception as e:
            traces[sym]=("ERR", str(e)[:40])
    line=" | ".join(f"{k} {v[0]} {v[1]}" for k,v in traces.items())
    print(f"[{attempt:02d}] {line}")
    decisions=[v[0] for v in traces.values()]
    has_buy="BUY" in decisions
    has_sell="SELL" in decisions
    has_wait="WAIT" in decisions
    if has_buy and has_sell and has_wait:
        print(f">>> TRIPLE CAPTURED at {attempt}: BUY+SELL+WAIT")
        # run official proof now to persist
        import subprocess
        subprocess.run([sys.executable, str(ROOT/"scripts/v1_final_operational_proof_all_assets.py")])
        break
    if attempt % 3==0 and attempt != max_tries:
        print(f"  ...sleep {delay}s for Yahoo cache...")
        time.sleep(delay)
else:
    print("No triple in max_tries; last was", traces)
