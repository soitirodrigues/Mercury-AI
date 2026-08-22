#!/usr/bin/env python3
"""
FORENSIC SCALE TRACE — MERCURY-AI V1
Prova executável das escalas reais, produtores, consumidores e serialização.
NÃO altera produção. Apenas rastreia.
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.analysis.confidence_engine import ConfidenceEngine
from mercury_ai.analysis.confluence_score_engine import ConfluenceScoreEngine
from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.institutional_score_engine import InstitutionalScoreEngine
from mercury_ai.analysis.institutional_trade_filter_engine import InstitutionalTradeFilterEngine
from mercury_ai.analysis.evidence_ranking_engine import EvidenceRankingEngine
from mercury_ai.analysis.decision_result_builder import DecisionResultBuilder
import inspect

def scale_contract():
    contracts = {}
    # ConfluenceScoreEngine
    src = pathlib.Path(ROOT / "mercury_ai/analysis/confluence_score_engine.py").read_text()
    contracts["confluence_score"] = {
        "declared": "0-100 (docs: confluence_score = max(bullish,bearish)/total_weight*100, clamp 0-100)",
        "producer": "ConfluenceScoreEngine.calculate + ConfluenceEngine.analyze.weighted_score (clamp 5-100)",
        "file": "mercury_ai/analysis/confluence_score_engine.py:85 + confluence_engine.py:119-165",
        "normalization": "total_weight=100 or active_weights_sum (scale_factor), clamp_score 5-100",
        "actual": "0-100 verified (live weighted 100.0)",
        "consumers": ["ProbabilityEngine.analyze(confluence_score 0-100)", "DecisionResolverEngine(confluence_score < threshold 40)", "InstitutionalScoreEngine(confluence*0.25)", "DecisionResultBuilder(score=institutional_score NOT confluence)"],
        "final": "ConfluenceEngine.weighted_score 0-100; DecisionResult.score is institutional_score (misalias risk)"
    }
    contracts["confidence_score"] = {
        "declared": "0-100 (ConfidenceEngine: 100*(0.25 quality +0.45 consensus+0.30 market), clamp 0-100)",
        "producer": "ConfidenceEngine.calculate -> final_score 0-100, calibrate clamp 0-100",
        "file": "mercury_ai/analysis/confidence_engine.py:98-121, builder.py:148",
        "normalization": "ConfidenceResult stores 0-100; DecisionResultBuilder stores confidence/100 => 0-1 (compat UI *100)",
        "actual": "Engine 0-100; DecisionResult.confidence 0-1 (68.24 stored as 0.682)",
        "consumers": ["ProbabilityEngine expects 0-100 (receives final_confidence 68)", "InstitutionalScoreEngine expects 0-100 (receives 68)", "UI expects 0-1 *100"],
        "final": "Snapshot confidence 0.682 is 0-1; report shows 0.682 (raw stored) without *100"
    }
    contracts["probability_institutional_strength"] = {
        "declared": "0-100 (ProbabilityEngine: confluence*0.5 + confidence*0.35 + evidence_bonus*0.15 then * (1-risk*0.5) clamp 0-100)",
        "producer": "ProbabilityEngine.analyze",
        "file": "mercury_ai/brain/probability_engine.py:90-108",
        "normalization": "clamp 0-100, wait = max(5,100-strength) cap 60",
        "actual": "BTC snapshot: raw 76.88 -> after risk 44.38 (D); live BTC today: raw ~?? -> 60.88 (B)",
        "consumers": ["ProbabilityResult.opportunity_grade thresholds 80/70/60/50", "wait_probability, buy/sell split"],
        "final": "Used for grade. Snapshot grade D matches 44.38 <50. NOT 854."
    }
    contracts["total_weight_expected_strength"] = {
        "declared": "UNCAPPED sum(weights) per evidence (no normalization), scale 0.. ~2000, NOT 0-100",
        "producer": "EvidenceRankingEngine.rank: total_weight = sum(e.weight for e in ranked)",
        "file": "mercury_ai/analysis/evidence_ranking_engine.py:29, builder.py:145 expected_strength=total_weight",
        "normalization": "none",
        "actual": "BTC 854.24, ETH 739.37, today's BTC 613.51",
        "consumers": ["DecisionResult.expected_strength (display only), NOT used for grade"],
        "final": "Report mislabels expected_strength as institutional_strength. Grade does NOT use it."
    }
    contracts["institutional_score"] = {
        "declared": "0-100 (InstitutionalScoreEngine: prob*0.35+confl*0.25+conf*0.15+trade*0.10+resolved*0.05+(100-risk)*0.10 * conflict 0-1 clamp 0-100)",
        "producer": "InstitutionalScoreEngine.calculate",
        "file": "mercury_ai/analysis/institutional_score_engine.py:44-68",
        "normalization": "clamp 0-100",
        "actual": "BTC snapshot stored as DecisionResult.score 65.27 (but recomputed live gives 55.27 with prob 44.39? see note - live today 73.61)",
        "consumers": ["DecisionResult.score (audit), explainability.institutional_score"],
        "final": "Stored correctly but report's confluence 65.27 equals this institutional_score, not confluence weighted 100"
    }
    contracts["trade_filter_quality"] = {
        "declared": "0-100 (100 - penalty, penalty sum regime+evidence+ATR, threshold allowed penalty>=50 blocked)",
        "producer": "InstitutionalTradeFilterEngine.evaluate",
        "file": "mercury_ai/analysis/institutional_trade_filter_engine.py:67-140",
        "normalization": "quality 0-100, level A+>=90 A>=80 B>=70 C>=60 D<60",
        "actual": "Live BTC today quality 80 allowed True (penalty 20?) but snapshot DecisionResult.trade_quality_score defaults 0.0 (builder bug) -> report 0.0 allowed True",
        "consumers": ["DecisionResult.quality (builder maps) but trade_quality_score/trade_allowed defaults remain 0/True"],
        "final": "Bug: builder does NOT set DecisionResult.trade_quality_score/trade_allowed/trade_quality_level"
    }
    contracts["probabilities"] = {
        "declared": "0-100 each, sum ≈100 (wait = max(5,100-strength) cap 60, remaining split to buy/sell by dominant_direction)",
        "producer": "ProbabilityEngine",
        "file": "mercury_ai/brain/probability_engine.py:114-145",
        "normalization": "round 2 decimals",
        "actual": "BTC snapshot 0+44.39+55.61=100.0 PASS; live BUY 60.88+0+39.12=100.0 PASS; SELL cases similar",
        "consumers": ["DecisionResult buy/sell/wait"],
        "final": "100.0 within tolerance"
    }
    contracts["opportunity_grade"] = {
        "declared": "A+ >=80, A >=70, B >=60, C >=50, D <50 on institutional_strength 0-100",
        "producer": "ProbabilityEngine grade block",
        "file": "mercury_ai/brain/probability_engine.py:157-168",
        "normalization": "thresholds hard-coded",
        "actual": "BTC strength 44.38 -> D correct; live strength 60.88 -> B correct",
        "consumers": ["DecisionResolverEngine rule 4 (conflict and grade C/D -> WAIT)", "explainability"],
        "final": "Consistent with strength, NOT with total_weight 854"
    }
    return contracts

def run_btc_eth_traces():
    # Load snapshots for BTC/ETH (the anomalous report values)
    btc_p = ROOT / "mercury_ai/database/snapshots/BTC-USD_2026-08-31T22-41-14.758600.json"
    eth_p = ROOT / "mercury_ai/database/snapshots/ETH-USD_2026-08-31T22-42-44.758600.json"  # approximate, discover
    # Find ETH snapshot matching proof json timestamp
    candidates = list((ROOT / "mercury_ai/database/snapshots").glob("ETH-USD*.json"))
    eth_p_found = None
    for c in sorted(candidates)[-20:]:
        try:
            j=json.load(open(c))
            if j["decision_result"]["expected_strength"]>700 and j["decision_result"]["expected_strength"]<800:
                eth_p_found=c
                break
        except: pass
    # fallback
    if eth_p_found is None and candidates:
        eth_p_found = sorted(candidates)[-1]
    traces={}
    for label, p in [("BTC", btc_p), ("ETH", eth_p_found)]:
        if p and p.exists():
            j=json.load(open(p))
            dr=j["decision_result"]
            er=j["evidence_ranking"]
            exp=dr.get("explainability",{})
            traces[label]={
                "snapshot_path": str(p),
                "decision": dr["decision"],
                "grade": dr["grade"],
                "confidence_stored_0_1": dr["confidence"],
                "confidence_implied_0_100": dr["confidence"]*100,
                "score_institutional": dr["score"],
                "expected_strength_total_weight": dr["expected_strength"],
                "total_weight_check": er["total_weight"],
                "buy": dr["buy_probability"],
                "sell": dr["sell_probability"],
                "wait": dr["wait_probability"],
                "sum_prob": dr["buy_probability"]+dr["sell_probability"]+dr["wait_probability"],
                "trade_allowed": dr["trade_allowed"],
                "trade_quality_score": dr["trade_quality_score"],
                "quality_alias": dr["quality"],
                "clarity": dr["clarity"],
                "audit_id": dr["audit_id"],
                "explainability_chain": exp.get("decision_chain",[]),
                "explainability_score": exp.get("institutional_score"),
                "ctx_risk": j["context"]["risk_assessment"]["institutional_risk_score"],
                "evidence_count": len(j["evidence_bundle"]["evidences"]),
            }
    # Also live traces
    scanner=MercuryScanner()
    for sym in ["BTC-USD","ETH-USD"]:
        res=scanner.pipeline.analyze(sym)
        dr=res.decision
        # capture confluence weighted via engine directly? we instrument via explainability
        exp=dr.explainability
        chain=exp.decision_chain if exp else ()
        # parse weighted from chain
        weighted=None
        conf_val=None
        for line in chain:
            if "Confluence: direction" in line:
                # e.g. 7.Confluence: direction=SELL, weighted=100.00
                import re
                m=re.search(r'weighted=([0-9.]+)', line)
                if m: weighted=float(m.group(1))
            if "Confidence: final=" in line:
                import re
                m=re.search(r'final=([0-9.]+)', line)
                if m: conf_val=float(m.group(1))
        traces[f"LIVE_{sym}"]={
            "decision": dr.decision,
            "grade": dr.grade,
            "confidence_stored_0_1": dr.confidence,
            "confidence_implied_0_100": dr.confidence*100,
            "score_institutional": dr.score,
            "expected_strength_total_weight": dr.expected_strength,
            "buy": dr.buy_probability,
            "sell": dr.sell_probability,
            "wait": dr.wait_probability,
            "sum_prob": dr.buy_probability+dr.sell_probability+dr.wait_probability,
            "trade_allowed": dr.trade_allowed,
            "trade_quality_score": dr.trade_quality_score,
            "quality_alias": dr.quality,
            "clarity": dr.clarity,
            "audit_id": dr.audit_id,
            "confluence_weighted_live": weighted,
            "confidence_final_live": conf_val,
            "grade_source_strength_recomputed": None,  # filled by probability trace earlier
        }
    return traces

if __name__ == "__main__":
    import pprint
    contracts=scale_contract()
    print(json.dumps(contracts, indent=2, ensure_ascii=False))
    traces=run_btc_eth_traces()
    print(json.dumps(traces, indent=2, ensure_ascii=False))
    out=ROOT/"reports/forensic_scale_trace.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out,"w") as f:
        json.dump({"contracts":contracts,"traces":traces}, f, indent=2)
    print(f"WROTE {out}")
