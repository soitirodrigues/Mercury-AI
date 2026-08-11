import json
from unittest.mock import MagicMock

import pytest

from mercury_ai.analysis.institutional_analytics_engine import InstitutionalAnalyticsEngine
from mercury_ai.analysis.learning_engine import LearningEngine
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.version_metadata import VersionMetadata


def _make_snapshot(audit_id: str, session_id: str = "SESSION-123") -> DecisionSnapshot:
    decision_result = DecisionResult(
        decision="BUY",
        grade="A",
        confidence=0.75,
        clarity=0.9,
        risk_score=0.1,
        score=1.0,
        quality=1.0,
        expected_strength=1.0,
        buy_probability=0.7,
        sell_probability=0.2,
        wait_probability=0.1,
        expected_risk=0.1,
        expected_reward=0.2,
        expected_drawdown=0.05,
        audit_id=audit_id,
        version_metadata=VersionMetadata("1.2.0", "1.2.0", "1.2.0", "1.2.0"),
        summary="s",
        explanation=TradingExplanation(
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
        ),
        technical_reason="",
        warnings=(),
        weaknesses=(),
        blockers=(),
        institutional_alignment=True,
        evidence_ranking=None,
        explainability=None,
    )
    placeholder_context = MarketContext(
        market=MagicMock(),
        trend=(),
        price_action=MagicMock(),
        support_resistance=MagicMock(),
        smart_money=MagicMock(),
        liquidity=MagicMock(),
        market_state=MagicMock(),
        market_regime=MagicMock(),
        mtf_consensus=MagicMock(),
        risk_assessment=MagicMock(),
    )

    return DecisionSnapshot(
        timestamp="2025-01-01T00:00:00Z",
        asset="BTC-USD",
        timeframe="5m",
        context=placeholder_context,
        evidence_bundle=MarketEvidenceBundle(evidences=(), timestamp="2025-01-01T00:00:00Z", asset="BTC-USD", timeframe="5m"),
        decision_result=decision_result,
        version_metadata=VersionMetadata("1.2.0", "1.2.0", "1.2.0", "1.2.0"),
        audit_events=(),
        session_id=session_id,
    )


def test_analytics_pairing_uses_replay_id(tmp_path):
    snapshot_dir = tmp_path / "snapshots"
    replay_dir = tmp_path / "replay"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)

    snapshot = _make_snapshot("A1", session_id="SESSION-1")
    logger = DecisionSnapshotLogger(base_path=str(snapshot_dir))
    logger.save(snapshot)

    replay_filepath = next(snapshot_dir.glob("*.json"))
    snapshot_data = json.loads(replay_filepath.read_text(encoding="utf-8"))
    replay_id = snapshot_data["replay_id"]

    metric_data = {
        "audit_id": snapshot_data["decision_result"]["audit_id"],
        "replay_id": replay_id,
        "hit": True,
        "pl": 1.0,
        "return_pct": 0.01,
    }
    (replay_dir / f"{replay_id}.json").write_text(json.dumps(metric_data), encoding="utf-8")

    eng = InstitutionalAnalyticsEngine(snapshot_dir=str(snapshot_dir), replay_dir=str(replay_dir))
    df = eng._load_data()

    assert len(df) == 1
    assert df.loc[0, "replay_id"] == replay_id
    assert df.loc[0, "audit_id"] == "A1"


def test_learning_pairing_prefers_replay_id(tmp_path):
    snapshot_dir = tmp_path / "snapshots"
    replay_dir = tmp_path / "replay"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)

    snapshot = _make_snapshot("A2", session_id="SESSION-2")
    logger = DecisionSnapshotLogger(base_path=str(snapshot_dir))
    logger.save(snapshot)

    snapshot_path = next(snapshot_dir.glob("*.json"))
    snapshot_data = json.loads(snapshot_path.read_text(encoding="utf-8"))
    replay_id = snapshot_data["replay_id"]

    metric_data = {
        "audit_id": snapshot_data["decision_result"]["audit_id"],
        "replay_id": replay_id,
        "hit": True,
        "pl": 2.0,
    }
    (replay_dir / f"{replay_id}.json").write_text(json.dumps(metric_data), encoding="utf-8")

    engine = LearningEngine(metrics_dir=str(replay_dir), snapshots_dir=str(snapshot_dir))
    report = engine.run_learning()

    assert report["best_assets"][0]["asset"] == "BTC-USD"
