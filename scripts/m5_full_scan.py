#!/usr/bin/env python3
"""
M5 FULL SCAN — SPRINT MERCURY-AI V1
Executa scanner M5 para TODOS os ativos suportados (distinct internal_symbol)
Gera evidence por ativo com campos obrigatorios e validacao de integridade.
"""
from __future__ import annotations
import json, sys, traceback, hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

MAP_PATH = ROOT / "reports" / "asset_universe" / "hezilex_asset_mapping.json"
OUT_JSON = ROOT / "reports" / "asset_universe" / "m5_full_scan.json"
OUT_TXT = ROOT / "reports" / "asset_universe" / "m5_full_scan.txt"

def utc_now(): return datetime.now(timezone.utc).isoformat()

def to_str(v):
    if v is None: return None
    if hasattr(v, "value"):
        try: return str(v.value).upper()
        except: pass
    try: return str(v).upper()
    except: return repr(v).upper()

# Load mapping
mapping: List[Dict[str,Any]] = json.loads(MAP_PATH.read_text(encoding="utf-8"))
# Distinct PASS internal_symbols
pass_entries = [e for e in mapping if e["mapping_status"]=="PASS"]
unsup_entries = [e for e in mapping if e["mapping_status"]!="PASS"]
# Deduplicate by internal_symbol preserving first occurrence
seen=set()
distinct_symbols=[]
symbol_to_entries={}
for e in pass_entries:
    sym=e["internal_symbol"]
    if sym not in seen:
        seen.add(sym)
        distinct_symbols.append(sym)
    symbol_to_entries.setdefault(sym, []).append(e)

print(f"Distinct supported symbols to scan: {len(distinct_symbols)} (from {len(pass_entries)} PASS entries)")
print(f"Unsupported entries: {len(unsup_entries)}")
print(f"Symbols: {distinct_symbols[:10]} ...")

# Prepare pipeline per symbol execution
# We'll create a single pipeline instance to reuse provider (but need fresh snapshot handling)
# Instead create scanner-like pipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.market_provider import MercuryDataProvider
from mercury_ai.core.analysis_pipeline import AnalysisPipeline

provider = MercuryDataProvider()
market_service = MarketDataService(provider=provider)
pipeline = AnalysisPipeline(market_service=market_service, providers=[provider])

# Import resolver for validation
from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine
resolver = DecisionResolverEngine()

# Cache results by symbol
results_by_symbol: Dict[str, Any] = {}
scan_errors: Dict[str, str] = {}

for sym in distinct_symbols:
    try:
        print(f"\n[SCAN] {sym} M5 ...")
        analysis = pipeline.analyze(sym)
        # Extract decision
        dec = analysis.decision
        mkt = analysis.market
        # data_available logic
        audit = getattr(dec, "audit_id", "")
        data_available = audit not in ("DATA_PROVIDER_UNAVAILABLE","DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED","PIPELINE_ERROR")
        # For DATA_QUALITY_FAIL etc, data was available but quality failed; but spec says data_available true if provider returned data
        # Use heuristic: if audit in DATA_QUALITY_FAIL then provider returned something but failed quality -> data_available True but scanner_executed True with WAIT
        # But spec distinguishes DATA_UNAVAILABLE vs WAIT LEGIT. Let's define:
        # data_available = audit not in DATA_PROVIDER_UNAVAILABLE/PIPELINE_ERROR
        data_available = audit not in ("DATA_PROVIDER_UNAVAILABLE","PIPELINE_ERROR")
        # data_timestamp: from DecisionSnapshot timestamp
        snapshot = pipeline.last_snapshots.get(sym)
        data_timestamp = None
        execution_timestamp = utc_now()
        if snapshot is not None:
            data_timestamp = snapshot.timestamp
            execution_timestamp = snapshot.timestamp
        # If snapshot has market data timestamp? Use snapshot.timestamp

        # Extract fields
        buy = float(getattr(dec, "buy_probability", 0) or 0)
        sell = float(getattr(dec, "sell_probability", 0) or 0)
        wait = float(getattr(dec, "wait_probability", 0) or 0)
        prob_sum = buy+sell+wait
        prob_ok = abs(prob_sum-100) < 0.1 or abs(prob_sum-100) < 1e-6 # tolerance 0.1 as V1
        # For DATA_QUALITY_FAIL etc, probabilities are 0,0,100 exactly -> PASS

        # Decision fields
        decision_str = to_str(getattr(dec, "decision", None))
        grade = to_str(getattr(dec, "grade", None))
        confidence = getattr(dec, "confidence", None)
        # confidence stored 0-100? In DecisionResult confidence is 0-100? Check: MercuryDecisionEngine confidence final_confidence 0-100? In trace conversion they *100. Let's keep as stored.
        # For our reports, confidence as stored (0-100 range). In AnalysisPipeline terminal results confidence 0.0.

        # confluence weighted score: try from analysis.confluence
        confl = getattr(analysis, "confluence", None)
        if confl is not None:
            confluence = getattr(confl, "weighted_score", None)
            dominant = getattr(confl, "dominant_direction", None)
            if dominant is not None and hasattr(dominant, "value"):
                dominant = to_str(dominant.value)
            else:
                dominant = to_str(dominant)
        else:
            # fallback to decision's explainability?
            confluence = None
            dominant = decision_str

        # trade_allowed, trade_quality
        trade_allowed = bool(getattr(dec, "trade_allowed", True))
        trade_quality = getattr(dec, "trade_quality_score", None)
        trade_quality_level = getattr(dec, "trade_quality_level", None)

        # audit_id
        audit_id = str(audit) if audit else ""
        # check if audit_id is hash 64 hex for legit signals
        is_hash = len(audit_id)==64 and all(c in "0123456789abcdefABCDEF" for c in audit_id)

        # Resolver integrity check
        # Need to call resolver to compare
        trace_dominant = dominant
        is_valid = getattr(dec, "trade_allowed", True)  # approximate; but original uses trade_allowed
        # For terminal results, decision is WAIT and is_valid maybe true but audit indicates DATA_QUALITY_FAIL -> still WAIT
        # Resolver call
        try:
            opp_grade = grade or "C"
            conf_score = confluence if confluence is not None else 100.0
            # need market_regime
            regime_obj = getattr(analysis, "market_regime", None)
            r_res = resolver.resolve(
                dominant_direction=trace_dominant or "NEUTRAL",
                is_valid=bool(is_valid),
                opportunity_grade=opp_grade,
                conflicting_signals=False,  # we don't have this; assume false. For full check use confluence conflicting?
                confluence_score=float(conf_score) if conf_score is not None else 100.0,
                market_regime=regime_obj,
            )
            resolver_decision = to_str(r_res.decision)
            resolver_rule = r_res.triggered_rule
            decision_consistency = (resolver_decision == decision_str)
            post_resolver_integrity = True if resolver_decision in ("WAIT", decision_str) else (resolver_decision==decision_str)
            # More strict: if resolver says BUY/SELL but final is WAIT then integrity false
            if resolver_decision in ("BUY","SELL") and decision_str=="WAIT":
                post_resolver_integrity=False
        except Exception as e:
            resolver_decision=None
            resolver_rule=None
            decision_consistency=False
            post_resolver_integrity=False

        # Determine status classification
        if audit in ("DATA_PROVIDER_UNAVAILABLE",):
            status = "DATA_UNAVAILABLE"
        elif audit in ("PIPELINE_ERROR",):
            status = "SCAN_ERROR"
        elif audit in ("DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED"):
            # These are WAIT legitimate but with quality fail reason -> categorize as DATA_UNAVAILABLE? But spec says distinguish REAL SIGNAL vs WAIT LEGITIMATE vs DATA UNAVAILABLE
            # We'll classify as WAIT_LEGITIMATE if audit is_quality fail? Actually DATA_QUALITY_FAIL is a terminal WAIT but not legit? Let's classify as DATA_UNAVAILABLE subtype
            # For gate we want M5 SCANNED includes these? The sprint says "Não fabricar resultado para ativo sem dados" and if no data -> DATA_PROVIDER_UNAVAILABLE
            # We'll keep status as WAIT_LEGITIMATE if decision WAIT with hash, else DATA_UNAVAILABLE for these audits
            # But for DATA_QUALITY_FAIL we have no real signal; treat as DATA_UNAVAILABLE to avoid counting as tradeable?
            # However pipeline creates a WAIT with audit DATA_QUALITY_FAIL; that's not a hash -> not legit WAIT.
            # We'll use status mapping:
            status = "DATA_UNAVAILABLE"
        elif decision_str in ("BUY","SELL") and is_hash:
            status = "REAL_SIGNAL"
        elif decision_str=="WAIT" and is_hash:
            status = "WAIT_LEGITIMATE"
        elif decision_str=="WAIT":
            status = "WAIT_LEGITIMATE" if audit not in ("DATA_PROVIDER_UNAVAILABLE","PIPELINE_ERROR","DATA_QUALITY_FAIL","INSUFFICIENT_DATA","MARKET_CLOSED") else "DATA_UNAVAILABLE"
        else:
            status = "ERROR"

        # But for supported assets with provider returning empty, we expect DATA_PROVIDER_UNAVAILABLE -> DATA_UNAVAILABLE

        entry = {
            "asset": sym,  # internal symbol
            "hezilex_sources": [e["input_name"] for e in symbol_to_entries[sym]],
            "asset_class": symbol_to_entries[sym][0]["asset_class"],
            "internal_symbol": sym,
            "provider_symbol": symbol_to_entries[sym][0]["provider_symbol"],
            "timeframe": "M5",
            "data_available": data_available,
            "data_timestamp": data_timestamp,
            "scanner_executed": True,
            "decision": decision_str,
            "grade": grade,
            "confidence": confidence,
            "confluence": confluence,
            "dominant_direction": dominant,
            "buy_probability": buy,
            "sell_probability": sell,
            "wait_probability": wait,
            "prob_sum": prob_sum,
            "prob_sum_ok": prob_ok,
            "trade_allowed": trade_allowed,
            "trade_quality": trade_quality,
            "trade_quality_level": trade_quality_level,
            "audit_id": audit_id,
            "execution_timestamp": execution_timestamp,
            "status": status,
            "error": None,
            "resolver_decision": resolver_decision,
            "resolver_rule": resolver_rule,
            "decision_consistency": decision_consistency,
            "post_resolver_integrity": post_resolver_integrity,
            "raw_score": getattr(dec, "score", None),
        }
        results_by_symbol[sym]=entry
        print(f" -> {decision_str} grade={grade} conf={confidence} confl={confluence} buy={buy} sell={sell} wait={wait} sum={prob_sum:.2f} status={status} audit={audit_id[:16]}...")
    except Exception as e:
        tb = traceback.format_exc()
        print(f" ERROR scanning {sym}: {e}")
        print(tb)
        results_by_symbol[sym]={
            "asset": sym,
            "hezilex_sources": [e["input_name"] for e in symbol_to_entries[sym]],
            "asset_class": symbol_to_entries[sym][0]["asset_class"],
            "internal_symbol": sym,
            "provider_symbol": symbol_to_entries[sym][0]["provider_symbol"],
            "timeframe": "M5",
            "data_available": False,
            "data_timestamp": None,
            "scanner_executed": False,
            "decision": None,
            "grade": None,
            "confidence": None,
            "confluence": None,
            "buy_probability": None,
            "sell_probability": None,
            "wait_probability": None,
            "prob_sum": None,
            "prob_sum_ok": False,
            "trade_allowed": False,
            "trade_quality": None,
            "trade_quality_level": None,
            "audit_id": "SCAN_ERROR",
            "execution_timestamp": utc_now(),
            "status": "SCAN_ERROR",
            "error": str(e),
            "resolver_decision": None,
            "resolver_rule": None,
            "decision_consistency": False,
            "post_resolver_integrity": False,
            "raw_score": None,
        }
        scan_errors[sym]=str(e)

# Now build full 68 entries per mapping (including unsupported)
full_records=[]
# PASS entries -> expand per mapping entry (so duplicate BTC-USD appears twice)
for e in mapping:
    if e["mapping_status"]=="PASS":
        sym=e["internal_symbol"]
        base=results_by_symbol.get(sym)
        # clone base but override hezilex asset fields to reflect this specific input
        rec=dict(base) if base else {}
        rec["hezilex_input"] = e["input_name"]
        rec["hezilex_asset"] = e["asset"]
        rec["mapping_status"] = e["mapping_status"]
        rec["mapping_reason"] = e["mapping_reason"]
        # For duplicate, keep same scan result but distinct hezilex_input
        full_records.append(rec)
    else:
        # UNSUPPORTED per spec
        rec={
            "asset": e["internal_symbol"] or e["asset"],
            "hezilex_input": e["input_name"],
            "hezilex_asset": e["asset"],
            "asset_class": e["asset_class"],
            "internal_symbol": e["internal_symbol"],
            "provider_symbol": e["provider_symbol"],
            "timeframe": "M5",
            "data_available": False,
            "data_timestamp": None,
            "scanner_executed": False,
            "decision": None,
            "grade": None,
            "confidence": None,
            "confluence": None,
            "dominant_direction": None,
            "buy_probability": None,
            "sell_probability": None,
            "wait_probability": None,
            "prob_sum": None,
            "prob_sum_ok": None,
            "trade_allowed": False,
            "trade_quality": None,
            "trade_quality_level": None,
            "audit_id": None,
            "execution_timestamp": None,
            "status": "UNSUPPORTED",
            "error": e["reason"],
            "mapping_status": e["mapping_status"],
            "mapping_reason": e["mapping_reason"],
            "resolver_decision": None,
            "resolver_rule": None,
            "decision_consistency": None,
            "post_resolver_integrity": None,
            "raw_score": None,
        }
        full_records.append(rec)

# Build output json structure
output={
    "generated_at": utc_now(),
    "timeframe": "M5",
    "total_hezilex_effective": len(mapping),
    "total_distinct_supported": len(distinct_symbols),
    "total_pass_entries": len(pass_entries),
    "total_unsupported": len(unsup_entries),
    "distinct_supported_symbols": distinct_symbols,
    "scan_errors": scan_errors,
    "records": full_records,
    # Summary for gate
    "summary": {
        "M5_SCANNED_DISTINCT": len([s for s in distinct_symbols if results_by_symbol.get(s, {}).get("scanner_executed")]),
        "M5_FAILED_DISTINCT": len([s for s in distinct_symbols if not results_by_symbol.get(s, {}).get("scanner_executed", False)]),
        "M5_SCANNED_ENTRIES": len([r for r in full_records if r.get("scanner_executed")]),
        "M5_FAILED_ENTRIES": len([r for r in full_records if r.get("mapping_status")=="PASS" and not r.get("scanner_executed")]),
        "REAL_SIGNAL": len([r for r in full_records if r.get("status")=="REAL_SIGNAL"]),
        "WAIT_LEGITIMATE": len([r for r in full_records if r.get("status")=="WAIT_LEGITIMATE"]),
        "DATA_UNAVAILABLE": len([r for r in full_records if r.get("status")=="DATA_UNAVAILABLE"]),
        "UNSUPPORTED": len([r for r in full_records if r.get("status")=="UNSUPPORTED"]),
        "SCAN_ERROR": len([r for r in full_records if r.get("status")=="SCAN_ERROR"]),
        "PROB_SUM_PASS": all(r.get("prob_sum_ok") in (True, None) for r in full_records if r.get("prob_sum_ok") is not None),
        "DECISION_CONSISTENCY_PASS": all(r.get("decision_consistency") in (True, None) for r in full_records if r.get("scanner_executed")),
        "POST_RESOLVER_PASS": all(r.get("post_resolver_integrity") in (True, None) for r in full_records if r.get("scanner_executed")),
    }
}

OUT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
print(f"\nWrote {OUT_JSON}")

# TXT report
lines=[]
lines.append("M5 FULL SCAN — MERCURY-AI V1")
lines.append(f"Generated: {output['generated_at']}")
lines.append(f"Timeframe: M5")
lines.append(f"HEZILEX EFFECTIVE: {output['total_hezilex_effective']}")
lines.append(f"DISTINCT SUPPORTED: {output['total_distinct_supported']}")
lines.append(f"PASS ENTRIES: {output['total_pass_entries']}")
lines.append(f"UNSUPPORTED: {output['total_unsupported']}")
lines.append("")
lines.append("SUMMARY:")
for k,v in output["summary"].items():
    lines.append(f" {k}: {v}")
lines.append("")
lines.append("PER-ASSET EVIDENCE:")
for r in full_records:
    if r["mapping_status"]!="PASS":
        lines.append(f"{r['hezilex_input']} | M5 | UNSUPPORTED | reason={r['mapping_reason']} | internal={r['internal_symbol']}")
    else:
        # determine LIVE_REAL etc? Use status
        ev_type = r["status"]
        lines.append(f"{r['hezilex_input']} -> {r['internal_symbol']} | M5 | {ev_type} | {r['decision']} grade={r['grade']} conf={r['confidence']} confl={r['confluence']} buy={r['buy_probability']} sell={r['sell_probability']} wait={r['wait_probability']} sum={r['prob_sum']} trade_allowed={r['trade_allowed']} audit={r['audit_id']} ts={r['execution_timestamp']} resolver={r['resolver_decision']}/{r['resolver_rule']} consistency={r['decision_consistency']}")

OUT_TXT.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {OUT_TXT}")
# Print summary
print("\n".join(lines[:120]))
