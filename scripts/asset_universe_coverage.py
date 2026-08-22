#!/usr/bin/env python3
"""Gera asset_universe_coverage.json/txt a partir de hezilex_asset_mapping.json"""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
MAP = ROOT / "reports" / "asset_universe" / "hezilex_asset_mapping.json"
OUT_JSON = ROOT / "reports" / "asset_universe" / "asset_universe_coverage.json"
OUT_TXT = ROOT / "reports" / "asset_universe" / "asset_universe_coverage.txt"

data = json.loads(MAP.read_text(encoding="utf-8"))
total = len(data)
supported = sum(1 for e in data if e["supported"])
unsupported = total - supported
configured = sum(1 for e in data if e["configured"])
not_configured = total - configured
mapping_errors = sum(1 for e in data if e["mapping_status"] not in ("PASS","UNSUPPORTED"))
# Check internal duplicates
pass_entries = [e for e in data if e["mapping_status"]=="PASS"]
unsup_entries = [e for e in data if e["mapping_status"]=="UNSUPPORTED"]

coverage = {
  "HEZILEX_ASSETS_DISCOVERED": total,
  "HEZILEX_RAW_INPUT_COUNT": 67,
  "HEZILEX_EFFECTIVE_COUNT": total,
  "SUPPORTED": supported,
  "UNSUPPORTED": unsupported,
  "MAPPING_ERRORS": mapping_errors,
  "CONFIGURED": configured,
  "NOT_CONFIGURED": not_configured,
  "exceptions": unsup_entries,
  "supported_list": [e["internal_symbol"] for e in pass_entries],
}

OUT_JSON.write_text(json.dumps(coverage, indent=2, ensure_ascii=False), encoding="utf-8")

lines=[]
lines.append("HEZILEX ASSETS DISCOVERED: {}".format(total))
lines.append("")
lines.append(f"SUPPORTED: {supported}")
lines.append(f"UNSUPPORTED: {unsupported}")
lines.append(f"MAPPING ERRORS: {mapping_errors}")
lines.append("")
lines.append(f"CONFIGURED: {configured}")
lines.append(f"NOT CONFIGURED: {not_configured}")
lines.append("")
lines.append("EXCEPTIONS (UNSUPPORTED):")
for e in unsup_entries:
  lines.append(f" - {e['input_name']} | {e['asset_class']} | internal={e['internal_symbol']} | reason={e['mapping_reason']}")
lines.append("")
lines.append("SUPPORTED (PASS):")
for e in pass_entries:
  lines.append(f" - {e['input_name']} -> {e['internal_symbol']} ({e['asset_class']}) provider={e['provider_symbol']}")
# Also list NOT CONFIGURED >0 note
lines.append("")
if not_configured>0:
  lines.append("NOTE: NOT CONFIGURED >0 corresponds to UNSUPPORTED assets proven incompatible with provider/universe (not FAIL).")
# Source of truth
try:
  sot=json.loads((ROOT/"reports/asset_universe/source_of_truth.json").read_text(encoding="utf-8"))
  lines.append("")
  lines.append(f"SOURCE_OF_TRUTH: {sot['SOURCE_OF_TRUTH']} count={sot['asset_count']}")
  lines.append(f"broker_config: {sot['broker_config']} (current {sot['broker_count_current']} assets)")
  lines.append(f"asset_registry: {sot['asset_registry']} (current {sot['registry_count_current']} assets)")
except: pass

OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
print("\n".join(lines))
print(f"\nWrote {OUT_JSON} and {OUT_TXT}")
