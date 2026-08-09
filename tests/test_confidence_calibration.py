import pytest
from unittest.mock import MagicMock
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_state import MarketState
from mercury_ai.models.market_state_enum import MarketStateEnum
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.analysis.confidence_engine import ConfidenceEngine

@pytest.fixture
def base_context():
    context = MagicMock(spec=MarketContext)
    context.trend = []
    context.mtf_consensus = None
    context.market_state = None
    context.risk_assessment = None
    context.market_regime = None
    return context

def test_confidence_calibration_optimal(base_context):
    engine = ConfidenceEngine()
    
    # High-quality, matching evidences across multiple distinct engines
    evidences = [
        Evidence(engine_name="TrendEngine", evidence_name="EMA Alignment", direction="BULLISH", strength=90.0, confidence=90.0, description="", weight=10.0, quality_score=100.0),
        Evidence(engine_name="SMEngine", evidence_name="CHoCH", direction="BULLISH", strength=85.0, confidence=85.0, description="", weight=15.0, quality_score=100.0),
        Evidence(engine_name="VolumeEngine", evidence_name="High Volume Buy", direction="BULLISH", strength=80.0, confidence=80.0, description="", weight=5.0, quality_score=100.0)
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evidences), timestamp="now", asset="BTC-USD", timeframe="5m")
    
    # Configure ideal market conditions
    base_context.trend = [evidences[0]] # Strong trend since strength >= 80
    base_context.mtf_consensus = MTFConsensus(global_bias="BULLISH", local_bias="BULLISH", conflict_detected=False, alignment_score=100.0, dominant_trend="BULLISH", institutional_consensus_strength=50.0, summary="")
    base_context.market_state = MarketState(state=MarketStateEnum.OPEN, explanation="")
    
    res = engine.calculate(base_context, bundle)
    assert res.confidence_score > 80.0
    assert res.confidence_grade == "A+"
    assert res.is_high is True

def test_confidence_calibration_pessimistic(base_context):
    engine = ConfidenceEngine()
    
    # Conflicting directions, low quality, fewer engines
    evidences = [
        Evidence(engine_name="TrendEngine", evidence_name="EMA Alignment", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=10.0, quality_score=40.0),
        Evidence(engine_name="SMEngine", evidence_name="CHoCH", direction="BEARISH", strength=50.0, confidence=50.0, description="", weight=10.0, quality_score=40.0)
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evidences), timestamp="now", asset="BTC-USD", timeframe="5m")
    
    # Unfavorable market conditions
    base_context.market_state = MarketState(state=MarketStateEnum.LOW_LIQUIDITY, explanation="")
    
    res = engine.calculate(base_context, bundle)
    assert res.confidence_score < 40.0
    assert res.confidence_grade in ("C", "D")
    assert res.is_high is False

def test_confidence_calibration_reproducibility(base_context):
    engine = ConfidenceEngine()
    
    evidences = [
        Evidence(engine_name="TrendEngine", evidence_name="EMA Alignment", direction="BULLISH", strength=80.0, confidence=80.0, description="", weight=10.0, quality_score=80.0),
        Evidence(engine_name="VolumeEngine", evidence_name="High Volume Buy", direction="BULLISH", strength=70.0, confidence=70.0, description="", weight=5.0, quality_score=80.0)
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evidences), timestamp="now", asset="BTC-USD", timeframe="5m")
    
    res1 = engine.calculate(base_context, bundle)
    res2 = engine.calculate(base_context, bundle)
    
    assert res1.confidence_score == res2.confidence_score
    assert res1.confidence_grade == res2.confidence_grade
    assert res1.is_high == res2.is_high
