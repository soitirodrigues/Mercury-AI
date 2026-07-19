import time
from unittest.mock import MagicMock
from mercury_ai.brain.mercury_decision_engine import MercuryDecisionEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.data_quality_result import DataQualityResult
from mercury_ai.core.pipeline_executor import PipelineExecutor

def test_decision_engine_benchmark():
    executor = PipelineExecutor()
    engine = MercuryDecisionEngine(executor)
    
    # Mocking internal engines
    engine.validation.validate = MagicMock(return_value=None)
    engine.quality.analyze = MagicMock(return_value=DataQualityResult(score=90.0, warnings=(), missing_inputs=(), stale_data=False, quality_level="HIGH"))
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
    
    context = MagicMock(spec=MarketContext)
    context.risk_assessment = MagicMock()
    context.risk_assessment.risk_score = 0.2
    
    evidences = (
        Evidence("Test", "E1", "BULLISH", 80.0, 90.0, "Bullish", 10.0, contribution_score=50.0, quality_score=80.0),
    )
    bundle = MarketEvidenceBundle(evidences=evidences, timestamp="now", asset="EURUSD", timeframe="1H")
    
    start_time = time.time()
    for _ in range(100):
        engine.analyze(context, bundle)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 100
    print(f"Average execution time: {avg_time:.6f}s")
    assert avg_time < 0.1 # Ensure reasonable performance
