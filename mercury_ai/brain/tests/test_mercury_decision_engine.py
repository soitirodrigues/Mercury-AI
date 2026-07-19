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
from mercury_ai.models.trade_filter_result import TradeFilterResult
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def decision_engine():
    # Setup mocks for internal engines
    executor = PipelineExecutor()
    engine = MercuryDecisionEngine(executor)
    
    # Mocking internal engines
    engine.validation.validate = MagicMock(return_value=(True, []))
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
    engine.confidence.calculate = MagicMock(return_value=ConfidenceResult(confidence_score=85.0, final_confidence=85.0, confidence_grade="A", is_high=True, average_quality=80.0, consensus_score=75.0, market_score=70.0, confirmation_count=3))
    engine.probability_engine = MagicMock()
    engine.probability_engine.analyze = MagicMock(return_value=ProbabilityResult(buy_probability=80.0, sell_probability=10.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    engine.explanation = MagicMock()
    # Replace explanation generation with NarrativeEngine mock
    engine.narrative = MagicMock()
    engine.narrative.generate = MagicMock(side_effect=lambda *args, **kwargs: TradingExplanation(
        exec_summary=f"Institutional {args[0] if args else 'WAIT'} signal triggered at 100.00000. Confidence: 85.00%. Conflict Score: 0.00.",
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
    from mercury_ai.models.market_data import MarketData
    from mercury_ai.models.market_context import MarketContext
    from mercury_ai.models.price_action import PriceActionAnalysis
    from mercury_ai.models.support_resistance import SupportResistanceAnalysis
    from mercury_ai.models.smart_money import SmartMoneyAnalysis
    from mercury_ai.models.market_structure import MarketStructure
    from mercury_ai.models.liquidity_profile import LiquidityProfile
    from mercury_ai.models.market_state import MarketState
    from mercury_ai.models.market_regime import MarketRegime
    from mercury_ai.models.market_regime_enum import MarketRegimeEnum
    from mercury_ai.models.market_state_enum import MarketStateEnum
    from mercury_ai.models.mtf_consensus import MTFConsensus
    from mercury_ai.models.risk_assessment import RiskAssessment

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1H",
        close=100.0,
        ema9=1.0,
        ema21=1.0,
        ema50=1.0,
        rsi=50.0,
        atr=1.0,
        adx=1.0,
        macd=0.0,
        macd_signal=0.0,
        bollinger_upper=105.0,
        bollinger_lower=95.0,
        volume=1000.0
    )
    
    context = MarketContext(
        market=market_data,
        trend=[],
        price_action=MagicMock(
            spec=PriceActionAnalysis, 
            trend_structure="BULLISH", 
            last_event="BOS", 
            confidence=80, 
            explanation=[]
        ),
        support_resistance=MagicMock(
            spec=SupportResistanceAnalysis,
            support=90.0,
            resistance=110.0,
            distance_support=10.0,
            distance_resistance=10.0,
            explanation=[]
        ),
        smart_money=MagicMock(
            spec=SmartMoneyAnalysis,
            structure=MagicMock(spec=MarketStructure, trend="BULLISH")
        ),
        liquidity=MagicMock(spec=LiquidityProfile),
        market_state=MagicMock(
            spec=MarketState,
            state=MarketStateEnum.TRENDING,
            explanation="Market is trending"
        ),
        market_regime=MagicMock(
            spec=MarketRegime,
            regime=MarketRegimeEnum.ACCUMULATION,
            confidence=0.8,
            supporting_evidences=[]
        ),
        mtf_consensus=MagicMock(spec=MTFConsensus),
        risk_assessment=MagicMock(
            spec=RiskAssessment, 
            institutional_risk_score=0.2,
            suggested_stop=1.0,
            suggested_take_profit=3.0,
            risk_reward_ratio=3.0,
            expected_drawdown=0.1,
            expected_volatility=0.05,
            trade_quality=0.8,
            max_exposure=0.02,
            invalidation_point=1.0
        )
    )
    return context

def test_decision_engine_buy_scenario(decision_engine):
    context = _create_context()
    # Mock confluence to return a result with dominant_direction as an Enum-like object with a .value attribute
    confluence_mock = MagicMock()
    confluence_mock.buy_score = 80.0
    confluence_mock.sell_score = 10.0
    confluence_mock.weighted_score = 70.0
    confluence_mock.agreement_percentage = 90.0
    confluence_mock.confidence = 80.0
    confluence_mock.dominant_direction.value = "BUY"
    confluence_mock.conflicting_signals = False

    decision_engine.confluence.analyze = MagicMock(return_value=(confluence_mock, []))
    decision_engine.probability_engine.analyze = MagicMock(return_value=ProbabilityResult(buy_probability=80.0, sell_probability=10.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    
    # Bundle with bullish evidence
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle, TradeFilterResult(allowed=True))
    
    assert result.decision == "BUY"
    assert result.grade == "A"
    assert result.audit_id is not None
    assert result.confidence == 0.85
    assert "Institutional BUY signal triggered" in result.summary
    
def test_decision_engine_sell_scenario(decision_engine):
    context = _create_context()
    # Mock confluence to return a result with dominant_direction as an Enum-like object with a .value attribute
    confluence_mock = MagicMock()
    confluence_mock.buy_score = 10.0
    confluence_mock.sell_score = 80.0
    confluence_mock.weighted_score = 70.0
    confluence_mock.agreement_percentage = 90.0
    confluence_mock.confidence = 80.0
    confluence_mock.dominant_direction.value = "SELL"
    confluence_mock.conflicting_signals = False

    decision_engine.confluence.analyze = MagicMock(return_value=(confluence_mock, []))
    decision_engine.probability_engine.analyze = MagicMock(return_value=ProbabilityResult(buy_probability=10.0, sell_probability=80.0, neutral_probability=10.0, expected_risk=20.0, opportunity_grade="A", institutional_confidence=85.0))
    
    # Bundle with bearish evidence
    evidences = (
        Evidence("Test", "E1", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle, TradeFilterResult(allowed=True))
    
    assert result.decision == "SELL"
    assert result.grade == "A"
    assert "Institutional SELL signal triggered" in result.summary

def test_decision_engine_wait_scenario(decision_engine):
    context = _create_context()
    decision_engine.confluence.analyze = MagicMock(return_value=(MagicMock(buy_score=40.0, sell_score=40.0, weighted_score=40.0, agreement_percentage=20.0), []))
    decision_engine.probability_engine.analyze = MagicMock(return_value=ProbabilityResult(buy_probability=33.3, sell_probability=33.3, neutral_probability=33.4, expected_risk=20.0, opportunity_grade="C", institutional_confidence=50.0))

    # Bundle with conflicting evidence
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
        Evidence("Test", "E2", "BEARISH", 80.0, 90.0, "Bearish", 10.0, contribution_score=50.0, quality_score=80.0)
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    result = decision_engine.analyze(context, bundle, TradeFilterResult(allowed=True))
    
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
    
    result = decision_engine.analyze(context, bundle, TradeFilterResult(allowed=True))
    
    assert len(result.weaknesses) == 1
    assert "Test low quality" in result.weaknesses[0]
