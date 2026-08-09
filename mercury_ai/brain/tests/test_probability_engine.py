import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle

def test_probability_engine_calculation():
    """Testa o cálculo de probabilidade com a composição canônica (Sprint 1.7)."""
    engine = ProbabilityEngine(weights={
        "trend": 0.4,
        "structure": 0.3,
        "liquidity": 0.2,
        "volatility": 0.1,
    })

    context = MagicMock(spec=MarketContext)
    context.risk_assessment = MagicMock()
    context.risk_assessment.institutional_risk_score = 0.2

    evs = [
        Evidence("TrendAnalyzer", "Trend", "BULLISH", 80.0, 90.0, "Desc", 1.0, contribution_score=80.0)
    ]
    bundle = MarketEvidenceBundle(evidences=tuple(evs), timestamp="now", asset="EURUSD", timeframe="1H")

    # Assinatura real: analyze(context, evidence_bundle, confluence_score, confidence_score, dominant_direction)
    result = engine.analyze(context, bundle, 80.0, 85.0, "BUY")

    # Composição canônica: confluence*0.50 + confidence*0.35 + evidence_bonus*0.15
    # confluence=80, confidence=85, evidence_bonus=min(1*4,20)=4
    # institutional_strength = 80*0.50 + 85*0.35 + 4*0.15 = 70.35
    # penalidade de risco: 70.35 * (1 - (0.2/100)*0.50) = 70.2797
    # grade A (>=70); buy = 100 - wait; wait = max(5, 100-70.2797) capped at 60 = 29.72
    assert result.buy_probability == pytest.approx(70.28)
    assert result.sell_probability == pytest.approx(0.0)
    assert result.neutral_probability == pytest.approx(29.72)
    assert result.opportunity_grade == "A"
    assert result.institutional_confidence > 0
    assert result.expected_risk >= 0
