import pytest
from mercury_ai.models.evidence import Evidence
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine

def test_evidence_quality_engine_independence():
    engine = EvidenceQualityEngine()
    evidences = [
        Evidence(engine_name="EngineA", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="EngineB", evidence_name="E2", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0)
    ]
    evaluated = engine.evaluate(evidences)
    assert evaluated[0].quality_score == 100.0
    assert evaluated[1].quality_score == 100.0

def test_evidence_quality_engine_redundancy():
    engine = EvidenceQualityEngine()
    evidences = [
        Evidence(engine_name="EngineA", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="EngineA", evidence_name="E2", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0)
    ]
    evaluated = engine.evaluate(evidences)
    assert evaluated[0].quality_score == 90.0
    assert evaluated[1].quality_score == 90.0

def test_evidence_quality_engine_conflict():
    engine = EvidenceQualityEngine()
    evidences = [
        Evidence(engine_name="EngineA", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="EngineB", evidence_name="E2", direction="BEARISH", strength=50.0, confidence=50.0, description="", weight=1.0)
    ]
    evaluated = engine.evaluate(evidences)
    assert evaluated[0].quality_score == 70.0
    assert evaluated[1].quality_score == 70.0

def test_evidence_quality_engine_redundancy_and_conflict():
    engine = EvidenceQualityEngine()
    evidences = [
        Evidence(engine_name="EngineA", evidence_name="E1", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="EngineA", evidence_name="E2", direction="BULLISH", strength=50.0, confidence=50.0, description="", weight=1.0),
        Evidence(engine_name="EngineB", evidence_name="E3", direction="BEARISH", strength=50.0, confidence=50.0, description="", weight=1.0)
    ]
    evaluated = engine.evaluate(evidences)
    # 0.9 (redundancy) * 0.7 (conflict) = 0.63
    assert evaluated[0].quality_score == pytest.approx(63.0)
    assert evaluated[1].quality_score == pytest.approx(63.0)
    assert evaluated[2].quality_score == pytest.approx(70.0)
