import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence

def test_probability_calculation():
    weights = {"Trend": 1.0, "Volume": 1.0}
    engine = ProbabilityEngine(weights=weights)
    context = MagicMock(spec=MarketContext)
    context.risk_assessment = MagicMock()
    context.risk_assessment.institutional_risk_score = 10.0

    # Evidence from different engines
    evs = [
        Evidence("TrendAnalyzer", "Trend", "BULLISH", 80.0, 90.0, "Desc", 1.0, contribution_score=80.0),
        Evidence("MarketStructureIntelligenceEngine", "BOS", "BULLISH", 70.0, 80.0, "Desc", 1.0, contribution_score=70.0),
        Evidence("LiquidityEngine", "Pool", "BULLISH", 60.0, 70.0, "Desc", 1.0, contribution_score=60.0),
        Evidence("VolatilityEngine", "Vol", "BULLISH", 50.0, 60.0, "Desc", 1.0, contribution_score=50.0),
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evs), timestamp="now", asset="EURUSD", timeframe="1H")

    # High confluence and confidence
    result = engine.analyze(context, bundle, confluence_score=80.0, confidence_score=85.0)

    assert result.buy_probability > 50.0
    assert result.opportunity_grade in ("HIGH", "MEDIUM", "LOW")
    assert result.institutional_confidence == 85.0
    assert pytest.approx(result.buy_probability + result.sell_probability + result.neutral_probability) == 100.0

