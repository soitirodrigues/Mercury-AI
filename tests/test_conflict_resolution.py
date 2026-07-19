import pytest
from unittest.mock import MagicMock
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine

def test_conflict_resolution_consensus():
    resolver = ConflictResolutionEngine()
    context = MagicMock(spec=MarketContext)
    context.market_regime = None
    evidences = [
        Evidence(engine_name="A", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=10.0),
        Evidence(engine_name="B", evidence_name="E2", direction="BULLISH", strength=60.0, confidence=60.0, description="", weight=20.0)
    ]
    resolved, score = resolver.resolve(evidences, context)
    assert len(resolved) == 2
    assert score == 1.0

def test_conflict_resolution_simple_conflict():
    resolver = ConflictResolutionEngine()
    context = MagicMock(spec=MarketContext)
    context.market_regime = None
    evidences = [
        Evidence(engine_name="A", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=10.0),
        Evidence(engine_name="B", evidence_name="E2", direction="BEARISH", strength=60.0, confidence=60.0, description="", weight=20.0)
    ]
    resolved, score = resolver.resolve(evidences, context)
    assert len(resolved) == 1
    assert resolved[0].direction == "BEARISH"
    # Weight diff: 20-10 = 10. Total 30. Score = 10/30 = 0.33
    assert score == pytest.approx(10.0/30.0)

def test_conflict_resolution_multiple_engines():
    resolver = ConflictResolutionEngine()
    context = MagicMock(spec=MarketContext)
    context.market_regime = None
    evidences = [
        Evidence(engine_name="A", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=10.0),
        Evidence(engine_name="B", evidence_name="E2", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=10.0),
        Evidence(engine_name="C", evidence_name="E3", direction="BEARISH", strength=60.0, confidence=60.0, description="", weight=40.0)
    ]
    resolved, score = resolver.resolve(evidences, context)
    assert len(resolved) == 1
    assert resolved[0].direction == "BEARISH"
    # Bullish weight: 10+10=20. Bearish: 40. Total: 60. Score = (40-20)/60 = 20/60 = 0.33
    assert score == pytest.approx(20.0/60.0)
