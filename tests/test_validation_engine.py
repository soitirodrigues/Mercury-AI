import pytest
from unittest.mock import MagicMock
from mercury_ai.analysis.validation_engine import ValidationEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence

@pytest.fixture
def validation_engine():
    return ValidationEngine()

def test_validation_evidence_consistency_failure(validation_engine):
    context = MagicMock(spec=MarketContext)
    context.market = MagicMock()
    
    # Evidence with invalid strength
    evs = (Evidence("Engine", "E1", "BULLISH", 150.0, 50.0, "Desc", 1.0),)
    bundle = MarketEvidenceBundle(evidences=evs, timestamp="now", asset="EURUSD", timeframe="1H")
    
    is_valid, warnings = validation_engine.validate_all(context, bundle)
    
    assert is_valid is False
    assert "Evidence consistency failure" in warnings

def test_validation_context_consistency_failure(validation_engine):
    context = MagicMock(spec=MarketContext)
    context.market = None # Invalid context
    
    bundle = MarketEvidenceBundle(evidences=(), timestamp="now", asset="EURUSD", timeframe="1H")
    
    is_valid, warnings = validation_engine.validate_all(context, bundle)
    
    assert is_valid is False
    assert "Context consistency failure" in warnings
