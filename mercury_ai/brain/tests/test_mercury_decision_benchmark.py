import time
from unittest.mock import MagicMock
from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.data_quality_result import DataQualityResult
from mercury_ai.models.trade_filter_result import TradeFilterResult
from mercury_ai.core.pipeline_executor import PipelineExecutor

def test_decision_engine_benchmark():
    executor = PipelineExecutor()
    engine = MercuryDecisionEngine(executor)
    
    # Mocking internal engines
    engine.validation.validate_all = MagicMock(return_value=(True, []))
    engine.quality.evaluate = MagicMock(return_value=[]) # Changed to an empty list
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
    engine.confidence.calculate = MagicMock(return_value=ConfidenceResult(confidence_score=85.0, final_confidence=85.0, confidence_grade="A", is_high=True, average_quality=70.0, consensus_score=75.0, market_score=70.0, confirmation_count=3))
    
    context = MagicMock(spec=MarketContext)
    context.market = MagicMock()
    context.market.close = 1.1000
    context.market.atr = 0.0010
    context.trend = MagicMock()
    context.smart_money = MagicMock()
    context.smart_money.structure = MagicMock()
    context.smart_money.structure.trend = "NEUTRAL"
    context.price_action = MagicMock()
    context.price_action.trend_structure = "NEUTRAL"
    context.liquidity = MagicMock()
    context.liquidity.liquidity_sweep = False
    context.support_resistance = MagicMock()
    context.support_resistance.distance_support = 100.0
    context.support_resistance.distance_resistance = 100.0
    context.market_state = MagicMock()
    context.market_state.state = "RANGING"
    context.market_regime = MagicMock()
    context.market_regime.regime = "ACCUMULATION"
    context.risk_assessment = MagicMock()
    context.risk_assessment.risk_score = 0.2
    context.risk_assessment.institutional_risk_score = 0.2
    
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    start_time = time.time()
    for _ in range(100):
        engine.analyze(context, bundle, TradeFilterResult(allowed=True))
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 100
    print(f"Average execution time: {avg_time:.6f}s")
    assert avg_time < 0.1 # Ensure reasonable performance
