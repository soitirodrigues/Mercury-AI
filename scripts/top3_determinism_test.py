#!/usr/bin/env python3
"""Teste de determinismo do ranking Top-3"""
import json, pathlib, subprocess, sys, hashlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
RUN1 = ROOT / "reports" / "asset_universe" / "top3_scanner.json"
# Re-run scanner
subprocess.run([sys.executable, str(ROOT/"scripts/top3_scanner.py")], check=True)
data1 = json.loads(RUN1.read_text(encoding="utf-8"))
hash1 = hashlib.sha256(json.dumps(data1["top3"], sort_keys=True).encode()).hexdigest()
print(f"RUN1 hash {hash1}")
# Run again
subprocess.run([sys.executable, str(ROOT/"scripts/top3_scanner.py")], check=True)
data2 = json.loads(RUN1.read_text(encoding="utf-8"))
hash2 = hashlib.sha256(json.dumps(data2["top3"], sort_keys=True).encode()).hexdigest()
print(f"RUN2 hash {hash2}")
if hash1==hash2:
    print("TOP_3_DETERMINISM = PASS")
    print(f"RUN 1 TOP3 == RUN 2 TOP3: {data1['top3'] == data2['top3']}")
else:
    print("TOP_3_DETERMINISM = FAIL")
    print(data1["top3"])
    print(data2["top3"])
    sys.exit(1)
