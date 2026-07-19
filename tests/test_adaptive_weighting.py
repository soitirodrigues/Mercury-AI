import pytest
from unittest.mock import MagicMock
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.market_regime_enum import MarketRegimeEnum
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine

@pytest.fixture
def base_context():
    context = MagicMock(spec=MarketContext)
    context.market_state = MarketRegime(regime=MarketRegimeEnum.STRONG_UPTREND, confidence=100.0, supporting_evidences=[])
    context.market_regime = MarketRegime(regime=MarketRegimeEnum.STRONG_UPTREND, confidence=100.0, supporting_evidences=[])
    return context

def test_adaptive_weighting_impact(base_context):
    resolver = ConflictResolutionEngine()
    
    evidences = [
        Evidence(engine_name="TrendEngine", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="VolatilityEngine", evidence_name="E2", direction="BEARISH", strength=50.0, confidence=50.0, description="", weight=1.0)
    ]
    
    # In Trending regime, Trend weight is 1.5, Volatility is 1.0 (base)
    # New weights: Trend=1.5, Volatility=1.0
    
    resolved, score = resolver.resolve(evidences, base_context)
    
    assert len(resolved) == 1
    assert resolved[0].engine_name == "TrendEngine"
    assert resolved[0].weight == 1.5
