import hashlib
from mercury_ai.analysis.decision_result_builder import DecisionResultBuilder
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.direction import AnalysisDirection


class DummyDecisionResultBuilder(DecisionResultBuilder):
    def build(
        self,
        *,
        final_decision: str,
        grade: str,
        calibrated_confidence: float,
        confluence_result: ConfluenceResult,
        risk_score: float,
        institutional_score: float,
        trade_quality_score: float,
        ranked_result: EvidenceRankingResult,
        buy_prob: float,
        sell_prob: float,
        wait_prob: float,
        expected_risk: float,
        expected_reward: float,
        expected_drawdown: float,
        explanation: TradingExplanation,
        resolved_bundle: MarketEvidenceBundle,
        final_warnings: list[str],
        confidence_result: ConfidenceResult,
        explainability=None,
    ):
        return super().build(
            final_decision=final_decision,
            grade=grade,
            calibrated_confidence=calibrated_confidence,
            confluence_result=confluence_result,
            risk_score=risk_score,
            institutional_score=institutional_score,
            trade_quality_score=trade_quality_score,
            ranked_result=ranked_result,
            buy_prob=buy_prob,
            sell_prob=sell_prob,
            wait_prob=wait_prob,
            expected_risk=expected_risk,
            expected_reward=expected_reward,
            expected_drawdown=expected_drawdown,
            explanation=explanation,
            resolved_bundle=resolved_bundle,
            final_warnings=final_warnings,
            confidence_result=confidence_result,
            explainability=explainability,
        )


def make_evidence(engine_name: str, evidence_name: str, timestamp: str):
    return Evidence(
        engine_name=engine_name,
        evidence_name=evidence_name,
        direction="BULLISH",
        strength=50.0,
        confidence=50.0,
        description="desc",
        weight=1.0,
        timestamp=timestamp,
    )


def test_audit_id_changes_for_different_evidence_content():
    builder = DecisionResultBuilder()
    common_bundle = MarketEvidenceBundle(
        evidences=(make_evidence("E1", "EV1", "2025-01-01T00:00:00Z"),),
        timestamp="2025-01-01T00:00:00Z",
        asset="TEST",
        timeframe="1H",
    )

    other_bundle = MarketEvidenceBundle(
        evidences=(make_evidence("E1", "EV2", "2025-01-01T00:00:00Z"),),
        timestamp="2025-01-01T00:00:00Z",
        asset="TEST",
        timeframe="1H",
    )

    explanation = TradingExplanation(
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
    confluence_result = ConfluenceResult(
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
    ranked_result = EvidenceRankingResult(
        ranked_evidences=(),
        contribution_percentage={},
        strongest_evidence=make_evidence("E1", "EV1", "2025-01-01T00:00:00Z"),
        weakest_evidence=make_evidence("E1", "EV1", "2025-01-01T00:00:00Z"),
        total_weight=1.0,
        bullish_weight=1.0,
        bearish_weight=0.0,
        neutral_weight=0.0,
        bullish_score=1.0,
        bearish_score=0.0,
        neutral_score=0.0,
    )
    confidence_result = ConfidenceResult(
        confidence_score=80.0,
        final_confidence=80.0,
        confidence_grade="A",
        is_high=True,
        average_quality=100.0,
        consensus_score=100.0,
        market_score=100.0,
        confirmation_count=1,
    )

    result_a = builder.build(
        final_decision="BUY",
        grade="A",
        calibrated_confidence=80.0,
        confluence_result=confluence_result,
        risk_score=0.1,
        institutional_score=1.0,
        trade_quality_score=1.0,
        ranked_result=ranked_result,
        buy_prob=0.7,
        sell_prob=0.2,
        wait_prob=0.1,
        expected_risk=0.1,
        expected_reward=0.2,
        expected_drawdown=0.05,
        explanation=explanation,
        resolved_bundle=common_bundle,
        final_warnings=[],
        confidence_result=confidence_result,
    )

    result_b = builder.build(
        final_decision="BUY",
        grade="A",
        calibrated_confidence=80.0,
        confluence_result=confluence_result,
        risk_score=0.1,
        institutional_score=1.0,
        trade_quality_score=1.0,
        ranked_result=ranked_result,
        buy_prob=0.7,
        sell_prob=0.2,
        wait_prob=0.1,
        expected_risk=0.1,
        expected_reward=0.2,
        expected_drawdown=0.05,
        explanation=explanation,
        resolved_bundle=other_bundle,
        final_warnings=[],
        confidence_result=confidence_result,
    )

    assert result_a.audit_id != result_b.audit_id
    assert len(result_a.audit_id) == 64
    assert len(result_b.audit_id) == 64
