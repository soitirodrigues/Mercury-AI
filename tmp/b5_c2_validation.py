import json
import os
import time
from pathlib import Path
from typing import List

from mercury_ai.analysis.decision_result_builder import DecisionResultBuilder
from mercury_ai.analysis.institutional_analytics_engine import InstitutionalAnalyticsEngine
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.direction import AnalysisDirection
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.trading_explanation import TradingExplanation


def make_evidence(name: str, timestamp: str, engine: str = "ENG") -> Evidence:
    return Evidence(
        engine_name=engine,
        evidence_name=name,
        direction="BULLISH",
        strength=50.0,
        confidence=50.0,
        description="desc",
        weight=1.0,
        timestamp=timestamp,
    )


def make_bundle(names: List[str], timestamps: List[str], asset="TEST", timeframe="1H") -> MarketEvidenceBundle:
    evidences = tuple(make_evidence(name, ts) for name, ts in zip(names, timestamps))
    return MarketEvidenceBundle(
        evidences=evidences,
        timestamp=timestamps[-1],
        asset=asset,
        timeframe=timeframe,
    )


def make_explanation():
    return TradingExplanation(
        exec_summary="s",
        decision_rationale="r",
        market_context="",
        trend_context="",
        liquidity_context="",
        structure_context="",
        momentum_context="",
        volume_context="",
        smart_money_context="",
        confluence_context="",
        risk_assessment="",
        confidence_rationale="",
        warnings=(),
        conflicts=(),
    )


def make_confluence():
    return ConfluenceResult(
        buy_score=100.0,
        sell_score=0.0,
        neutral_score=0.0,
        agreement_percentage=100.0,
        conflicting_signals=False,
        independent_confirmations=0,
        weighted_score=100.0,
        confidence=100.0,
        dominant_direction=AnalysisDirection.BUY,
        evidences=(),
        warnings=(),
    )


def make_ranked():
    ev = make_evidence("EV", "2025-01-01T00:00:00Z")
    return EvidenceRankingResult(
        ranked_evidences=(ev,),
        contribution_percentage={},
        strongest_evidence=ev,
        weakest_evidence=ev,
        total_weight=1.0,
        bullish_weight=1.0,
        bearish_weight=0.0,
        neutral_weight=0.0,
        bullish_score=1.0,
        bearish_score=0.0,
        neutral_score=0.0,
    )


def build_audit_id(bundle: MarketEvidenceBundle) -> str:
    builder = DecisionResultBuilder()
    result = builder.build(
        final_decision="BUY",
        grade="A",
        calibrated_confidence=80.0,
        confluence_result=make_confluence(),
        risk_score=0.1,
        institutional_score=1.0,
        trade_quality_score=1.0,
        ranked_result=make_ranked(),
        buy_prob=0.7,
        sell_prob=0.2,
        wait_prob=0.1,
        expected_risk=0.1,
        expected_reward=0.2,
        expected_drawdown=0.05,
        explanation=make_explanation(),
        resolved_bundle=bundle,
        final_warnings=[],
        confidence_result=ConfidenceResult(
            confidence_score=80.0,
            final_confidence=80.0,
            confidence_grade="A",
            is_high=True,
            average_quality=100.0,
            consensus_score=100.0,
            market_score=100.0,
            confirmation_count=1,
        ),
    )
    return result.audit_id


def bulk_audit_ids(count: int):
    ids = []
    for i in range(count):
        names = [f"EV-{i}-{j}" for j in range(3)]
        timestamps = [f"2025-01-01T00:00:0{j}Z" for j in range(3)]
        bundle = make_bundle(names, timestamps)
        ids.append(build_audit_id(bundle))
    return ids


def test_replay_storage(tmpdir):
    out = {}
    storage = ReplayStorage(output_dir=str(tmpdir))
    bundle = make_bundle(["EV1"], ["2025-01-01T00:00:00Z"])
    aid = build_audit_id(bundle)
    snapshot = type("snap", (), {})()
    snapshot.decision_result = type("dr", (), {"decision":"BUY", "confidence":0.75, "audit_id":aid})
    snapshot.timestamp = "2025-01-01T00:00:00Z"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.5, hit=True)
    storage.save(aid, snapshot, metrics)
    storage.save(aid, snapshot, metrics)
    out["storage_files"] = [p.name for p in Path(tmpdir).glob("*.json")]
    return out


def test_analytics(tmpdir):
    snapshot_dir = Path(tmpdir) / "snapshots"
    replay_dir = Path(tmpdir) / "replays"
    snapshot_dir.mkdir(parents=True)
    replay_dir.mkdir(parents=True)

    bundle_a = make_bundle(["EV-A"], ["2025-01-01T00:00:00Z"], asset="ASSET-A")
    bundle_b = make_bundle(["EV-B"], ["2025-01-01T00:00:00Z"], asset="ASSET-B")
    aid_a = build_audit_id(bundle_a)
    aid_b = build_audit_id(bundle_b)
    (snapshot_dir / f"{aid_a}.json").write_text(json.dumps({
        "asset":"ASSET-A",
        "timestamp":"2025-01-01T00:00:00Z",
        "decision_result":{"audit_id":aid_a, "decision":"BUY", "score":10.0, "confidence":0.8},
        "evidence_bundle":{"evidences":[{"evidence_name":"EV-A","engine_name":"ENG","direction":"BULLISH"}]},
    }))
    (snapshot_dir / f"{aid_b}.json").write_text(json.dumps({
        "asset":"ASSET-B",
        "timestamp":"2025-01-01T00:00:00Z",
        "decision_result":{"audit_id":aid_b, "decision":"SELL", "score":-5.0, "confidence":0.4},
        "evidence_bundle":{"evidences":[{"evidence_name":"EV-B","engine_name":"ENG","direction":"BEARISH"}]},
    }))
    (replay_dir / f"{aid_a}.json").write_text(json.dumps({
        "audit_id":aid_a,
        "decision":"BUY",
        "confidence":0.8,
        "mae":0.1,
        "mfe":0.3,
        "pl":1.0,
        "hit":True,
        "timestamp":"2025-01-01T01:00:00Z",
    }))
    (replay_dir / f"{aid_b}.json").write_text(json.dumps({
        "audit_id":aid_b,
        "decision":"SELL",
        "confidence":0.4,
        "mae":0.2,
        "mfe":0.1,
        "pl":-0.5,
        "hit":False,
        "timestamp":"2025-01-01T01:00:00Z",
    }))

    engine = InstitutionalAnalyticsEngine(snapshot_dir=str(snapshot_dir), replay_dir=str(replay_dir))
    report = engine.generate_quality_report()
    return {
        "records": engine._load_data().to_dict(orient="records"),
        "report_status": report.get("status"),
    }


def main():
    tmpdir = Path("tmp/b5_c2_probe")
    tmpdir.mkdir(parents=True, exist_ok=True)
    results = {
        "collision_controlled": {},
        "bulk_counts": {},
        "same_replay": {},
        "timestamp_diff": {},
        "order_stability": {},
        "large_content": {},
        "storage": {},
        "analytics": {},
    }

    bundle_a = make_bundle(["EV1"], ["2025-01-01T00:00:00Z"], asset="TEST")
    bundle_b = make_bundle(["EV2"], ["2025-01-01T00:00:01Z"], asset="TEST")
    results["collision_controlled"] = {
        "asset": bundle_a.asset,
        "timeframe": bundle_a.timeframe,
        "len_evidences": len(bundle_a.evidences),
        "audit_id_a": build_audit_id(bundle_a),
        "audit_id_b": build_audit_id(bundle_b),
        "equal": build_audit_id(bundle_a) == build_audit_id(bundle_b),
    }

    for n in [100, 500, 1000]:
        ids = bulk_audit_ids(n)
        unique = len(set(ids))
        results["bulk_counts"][n] = {
            "total": n,
            "unique": unique,
            "duplicates": n - unique,
        }

    bundle_same_1 = make_bundle(["EV1"], ["2025-01-01T00:00:00Z"], asset="TEST")
    bundle_same_2 = make_bundle(["EV1"], ["2025-01-01T00:00:00Z"], asset="TEST")
    results["same_replay"] = {
        "audit_id_1": build_audit_id(bundle_same_1),
        "audit_id_2": build_audit_id(bundle_same_2),
        "equal": build_audit_id(bundle_same_1) == build_audit_id(bundle_same_2),
    }

    bundle_ts1 = make_bundle(["EV1"], ["2025-01-01T00:00:00Z"], asset="TEST")
    bundle_ts2 = make_bundle(["EV1"], ["2025-01-01T00:00:00+00:00"], asset="TEST")
    results["timestamp_diff"] = {
        "audit_id_t1": build_audit_id(bundle_ts1),
        "audit_id_t2": build_audit_id(bundle_ts2),
        "equal": build_audit_id(bundle_ts1) == build_audit_id(bundle_ts2),
    }

    bundle_order_1 = make_bundle(["EV1", "EV2"], ["2025-01-01T00:00:00Z", "2025-01-01T00:01:00Z"], asset="TEST")
    bundle_order_2 = make_bundle(["EV2", "EV1"], ["2025-01-01T00:01:00Z", "2025-01-01T00:00:00Z"], asset="TEST")
    results["order_stability"] = {
        "audit_id_1": build_audit_id(bundle_order_1),
        "audit_id_2": build_audit_id(bundle_order_2),
        "equal": build_audit_id(bundle_order_1) == build_audit_id(bundle_order_2),
    }

    for count in [10, 50, 100]:
        names = [f"EV-{i}" for i in range(count)]
        timestamps = [f"2025-01-01T00:{i:02d}:00Z" for i in range(count)]
        bundle = make_bundle(names, timestamps, asset="TEST")
        start = time.perf_counter()
        aid = build_audit_id(bundle)
        elapsed = time.perf_counter() - start
        results["large_content"][count] = {
            "audit_id": aid,
            "time_s": elapsed,
            "len": count,
        }

    results["storage"] = test_replay_storage(tmpdir / "storage")
    analytics_results = test_analytics(tmpdir / "analytics")
    analytics_results["records"] = [
        {k: (v.isoformat() if hasattr(v, 'isoformat') else v) for k, v in r.items()}
        for r in analytics_results["records"]
    ]
    results["analytics"] = analytics_results

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
