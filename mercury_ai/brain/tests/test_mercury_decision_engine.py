import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.probability_result import ProbabilityResult
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def decision_engine():
    # Setup mocks for internal engines
    executor = PipelineExecutor()
    engine = MercuryDecisionEngine(executor)
    
    # Mocking internal engines
    engine.validation.validate = MagicMock(return_value=None)
    engine.quality.evaluate = MagicMock(return_value=[]) # Updated to match engine logic
    engine.ranking.rank = MagicMock(return_value=EvidenceRankingResult(
        ranked_evidences=[],
        contribution_percentage={},
        strongest_evidence=None,
        weakest_evidence=None,
        total_weight=0.8,
        bullish_weight=0.5,
        bearish_weight=0.3,
        neutral_weight=0.0,
        bullish_score=0.5,
        bearish_score=0.3,
        neutral_score=0.0
    ))
    engine.confidence.calculate = MagicMock(return_value=ConfidenceResult(confidence_score=85.0, confidence_grade="A", is_high=True))
    engine.probability_engine = MagicMock()
    engine.probability_engine.calculate = MagicMock(return_value=ProbabilityResult(buy_probability=80.0, sell_probability=10.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    engine.explanation = MagicMock()
    # Replace explanation generation with NarrativeEngine mock
    engine.narrative = MagicMock()
    engine.narrative.generate = MagicMock(return_value=TradingExplanation(
        exec_summary="Institutional BUY signal triggered at 100.00000. Confidence: 85.00%. Conflict Score: 0.00.",
        decision_rationale="Thesis",
        market_context="Context",
        trend_context="Trend",
        liquidity_context="Liquidity",
        momentum_context="Momentum",
        structure_context="Structure",
        volume_context="Volume",
        smart_money_context="SM",
        confluence_context="Conf",
        risk_assessment="Risk",
        confidence_rationale="High",
        strong_evidences=("E1",),
        weak_evidences=(),
        missing_confirmations=(),
        detected_risks=(),
        machine_readable={},
        engine_weights={}
    ))

    # Remove confluence.analyze from fixture

    return engine

def _create_context():
    context = MagicMock(spec=MarketContext)
    context.trend = []
    context.market = MagicMock()
    context.market.atr = 1.0
    context.market.ema9 = 1.0
    context.market.adx = 1.0
    context.market.close = 100.0
    context.mtf_consensus = None
    context.smart_money = None
    context.risk_assessment = MagicMock()
    context.risk_assessment.risk_score = 0.2
    return context

def test_decision_engine_buy_scenario(decision_engine):
    context = _create_context()
    decision_engine.confluence.analyze = MagicMock(return_value=MagicMock(buy_score=80.0, sell_score=10.0, weighted_score=70.0, agreement_percentage=90.0))
    decision_engine.probability_engine.calculate = MagicMock(return_value=ProbabilityResult(buy_probability=80.0, sell_probability=10.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    
    # Bundle with bullish evidence
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle)
    
    assert result.decision == "BUY"
    assert result.grade == "A"
    assert result.audit_id is not None
    assert result.confidence == 0.85
    assert "Institutional BUY signal triggered" in result.summary
    
def test_decision_engine_sell_scenario(decision_engine):
    context = _create_context()
    decision_engine.confluence.analyze = MagicMock(return_value=MagicMock(buy_score=10.0, sell_score=80.0, weighted_score=70.0, agreement_percentage=90.0))
    decision_engine.probability_engine.calculate = MagicMock(return_value=ProbabilityResult(buy_probability=10.0, sell_probability=80.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    
    # Bundle with bearish evidence
    evidences = (
        Evidence("Test", "E1", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle)
    
    assert result.decision == "SELL"
    assert result.grade == "A"
    assert "Institutional SELL signal triggered" in result.summary

def test_decision_engine_wait_scenario(decision_engine):
    context = _create_context()
    decision_engine.confluence.analyze = MagicMock(return_value=MagicMock(buy_score=40.0, sell_score=40.0, weighted_score=40.0, agreement_percentage=20.0))
    decision_engine.probability_engine.calculate = MagicMock(return_value=ProbabilityResult(buy_probability=33.3, sell_probability=33.3, neutral_probability=33.4, expected_risk=20.0, opportunity_grade="C", institutional_confidence=50.0))

    # Bundle with conflicting evidence
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle)
    
    assert result.decision == "WAIT"
    assert result.grade == "C"

def test_decision_engine_low_quality_scenario(decision_engine):
    context = _create_context()
    
    # Mock low quality
    low_quality_ev = Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=20.0)
    decision_engine.quality.evaluate = MagicMock(return_value=[low_quality_ev])
    
    # Bundle with low quality evidence
    evidences = (low_quality_ev,)
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle)
    
    assert len(result.weaknesses) == 1
    assert "Test low quality" in result.weaknesses[0]
