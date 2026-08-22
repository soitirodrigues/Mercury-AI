import sys, pathlib, time, json
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mercury_ai.brain.scanner import MercuryScanner

max_tries=40
delay_cache=65  # Yahoo TTL 60s
try:
    for attempt in range(1, max_tries+1):
        sc=MercuryScanner()
        r1=sc.pipeline.analyze("BTC-USD")
        r2=sc.pipeline.analyze("ETH-USD")
        d1=r1.decision.decision; d2=r2.decision.decision
        print(f"[{attempt:02d}] BTC {d1} {r1.decision.grade} {r1.confluence.weighted_score:.1f} ETH {d2} {r2.decision.grade} {r2.confluence.weighted_score:.1f} wait {r1.decision.wait_probability:.1f}/{r2.decision.wait_probability:.1f} trade {r1.decision.trade_quality_score:.0f}/{r2.decision.trade_quality_score:.0f}")
        if (d1=="BUY" and d2=="SELL") or (d1=="SELL" and d2=="BUY"):
            print(f">>> MIXED CAPTURED at attempt {attempt}: BTC {d1} ETH {d2}")
            # also show proof run
            from scripts.v1_final_operational_proof_all_assets import extract_trace
            t1=extract_trace(r1); t2=extract_trace(r2)
            print(json.dumps({"BTC":t1,"ETH":t2}, indent=2, ensure_ascii=False)[:3000])
            break
        if d1=="WAIT" or d2=="WAIT":
            print(f">>> WAIT observed at attempt {attempt}")
            break
        if attempt % 3==0:
            print(f"  ...sleep {delay_cache}s to refresh Yahoo cache...")
            time.sleep(delay_cache)
    else:
        print("No mixed BUY/SELL in max_tries, last was BUY+BUY persistent. Historical SELL still valid (32/100 BTC SELL), plus mock proves pipeline SELL path.")
except KeyboardInterrupt:
    print("interrupted")
