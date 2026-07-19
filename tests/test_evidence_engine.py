import pytest
from mercury_ai.models.evidence import Evidence
from mercury_ai.analysis.evidence_engine import EvidenceEngine
from unittest.mock import MagicMock

def test_evidence_engine_deduplication():
    engine = EvidenceEngine()
    evs = [
        Evidence("Trend", "E1", "BULLISH", 50.0, 50.0, "Desc", 1.0),
        Evidence("Trend", "E1", "BULLISH", 50.0, 50.0, "Desc", 1.0), # Duplicate
        Evidence("Vol", "E2", "BULLISH", 50.0, 50.0, "Desc", 1.0)
    ]
    bundle = engine.process(evs, "EURUSD", "1H", context=MagicMock())
    assert len(bundle.evidences) == 2

def test_evidence_engine_normalization():
    engine = EvidenceEngine()
    evs = [
        Evidence("Trend", "E1", "BULLISH", 150.0, -50.0, "Desc", 1.0) # Invalid bounds
    ]
    bundle = engine.process(evs, "EURUSD", "1H", context=MagicMock())
    assert bundle.evidences[0].strength == 100.0
    assert bundle.evidences[0].confidence == 0.0

def test_evidence_engine_agreement():
    engine = EvidenceEngine()
    evs = [
        Evidence("Trend", "E1", "BULLISH", 50.0, 50.0, "Desc", 1.0),
        Evidence("Vol", "E2", "BULLISH", 50.0, 50.0, "Desc", 1.0),
        Evidence("SM", "E3", "BEARISH", 50.0, 50.0, "Desc", 1.0)
    ]
    # 2 BULLISH, 1 BEARISH. Total 3. Agreement = 2/3 = 0.66
    agreement = engine.calculate_agreement(evs)
    assert agreement == pytest.approx(2/3)
