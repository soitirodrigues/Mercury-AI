import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle

def test_probability_engine_calculation():
    """Testa o cálculo de probabilidade com os pesos institucionais reais."""
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

    # Valores verificados via execução real do engine
    assert result.buy_probability == pytest.approx(40.0)
    assert result.sell_probability == pytest.approx(0.0)
    assert result.neutral_probability == pytest.approx(60.0)
    assert result.opportunity_grade == "D"
    assert result.institutional_confidence > 0
    assert result.expected_risk >= 0
