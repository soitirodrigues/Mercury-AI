import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle

class MockRiskContext:
    def __init__(self, risk_score):
        self.risk_score = risk_score

def test_probability_engine_calculation():
    engine = ProbabilityEngine()
    
    # Needs MarketContext and MarketEvidenceBundle for analyze()
    context = MagicMock(spec=MarketContext)
    
    # Mock some evidences
    evs = [
        Evidence("TrendAnalyzer", "Trend", "BULLISH", 80.0, 90.0, "Desc", 1.0, contribution_score=80.0)
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evs), timestamp="now", asset="EURUSD", timeframe="1H")
    
    # Confluence 80.0, Confidence 85.0
    result = engine.analyze(context, bundle, 80.0, 85.0)
    
    # The logic in analysis/probability_engine.py is deterministic
    # trend_score = 80.0, others=50.0 (default)
    # raw_bias = (80*0.4) + (50*0.3) + (50*0.2) + (50*0.1) = 32 + 15 + 10 + 5 = 62.0
    # final_score = (62*0.6) + (80*0.4) = 37.2 + 32 = 69.2
    # final_score > 60: buy_prob = min(90, 69.2 + 10) = 79.2
    # sell_prob = 100 - 79.2 - 5 = 15.8
    
    assert result.buy_probability == pytest.approx(79.2)
    assert result.sell_probability == pytest.approx(15.8)
    assert result.opportunity_grade == "A"
