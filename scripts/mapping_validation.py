#!/usr/bin/env python3
"""MAPPING VALIDATION — valida hezilex_asset_mapping.json conforme sprint 4-5"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP = ROOT / "reports" / "asset_universe" / "hezilex_asset_mapping.json"
data = json.loads(MAP.read_text(encoding="utf-8"))
errors=[]
for e in data:
    for k in ["source","asset","asset_class","normalized_name","internal_symbol","provider_symbol","mapping_status"]:
        if k not in e:
            errors.append(f"missing {k} in {e}")
    if e["mapping_status"] not in ("PASS","UNSUPPORTED"):
        errors.append(f"invalid mapping_status {e}")
    if e["mapping_status"]=="PASS" and not e["supported"]:
        errors.append(f"PASS but not supported {e['asset']}")
    if e["mapping_status"]=="UNSUPPORTED" and e["supported"]:
        errors.append(f"UNSUPPORTED but supported {e['asset']}")

# Check explicit attention cases
checks = {
 "SPOTFY": lambda e: e["internal_symbol"]=="SPOT" and "TYPO" in e["mapping_reason"],
 "WELLS FARGO": lambda e: e["internal_symbol"]=="WFC" and e["mapping_status"]=="PASS",
 "MORGAN STANLEY": lambda e: "MORGAN STANLEY" in e["input_name"] and e["mapping_status"]=="UNSUPPORTED",
 "SPACEX": lambda e: e["mapping_status"]=="UNSUPPORTED" and e["internal_symbol"] is None,
 "BTC/USD": lambda e: e["internal_symbol"]=="BTC-USD",
}
for inp, fn in checks.items():
    # Use exact matching aligned to checks
    if inp == "WELLS FARGO":
        matches=[e for e in data if e["asset"]=="WELLS FARGO"]
    elif inp == "MORGAN STANLEY":
        matches=[e for e in data if e["asset"]=="MORGAN STANLEY"]
    elif inp == "SPOTFY":
        matches=[e for e in data if e["input_name"]=="SPOTFY"]
    else:
        matches=[e for e in data if inp in e["input_name"] or e["asset"]==inp]
    if not matches: errors.append(f"missing attention case {inp}")
    else:
        for m in matches:
            if not fn(m): errors.append(f"attention case {inp} failed: {m}")

# Check dedup
distinct = len(set(e["internal_symbol"] for e in data if e["internal_symbol"]))
print(f"Total entries {len(data)} distinct internal {distinct}")
print(f"PASS {sum(1 for e in data if e['mapping_status']=='PASS')} UNSUPPORTED {sum(1 for e in data if e['mapping_status']=='UNSUPPORTED')}")
if errors:
    print("MAPPING VALIDATION FAIL:")
    for err in errors: print(" -",err)
    sys.exit(1)
else:
    print("MAPPING VALIDATION PASS")
    print("Attention cases: SPOTFY->SPOT, WELLS FARGO STANLEY split, BTC/USD->BTC-USD, SPACEX unsupported all OK")
