from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.config import settings
from unittest.mock import MagicMock

def test_versioning():
    # Setup mock data for AnalysisResult (minimal)
    mock_market = MagicMock()
    mock_context = MagicMock()
    
    res = AnalysisResult(
        market=mock_market,
        context=mock_context,
        trend=[],
        mtf_evidences=[],
        smart_money=MagicMock(),
        market_regime=None,
        confluence=None,
        market_condition=None,
        market_state=None,
        candlestick_analysis=None,
        volatility_analysis=None,
        session_analysis=None,
        support_resistance=None,
        liquidity_analysis=None,
        risk_assessment=None,
        evidence_ranking=None,
        volume_analysis=None,
        structure_analysis=None,
        decision=None
    )
    
    assert res.version == settings.VERSION
    
    # Setup mock data for DecisionSnapshot (minimal)
    snap = DecisionSnapshot(
        timestamp="2026-01-01T00:00:00",
        asset="BTC-USD",
        timeframe="5m",
        context=mock_context,
        evidence_bundle=MagicMock(),
        decision_result=MagicMock(),
        version_metadata=MagicMock(),
        audit_events=(),
        session_id="dummy_session_id"
    )
    
    assert snap.version == settings.VERSION
    assert snap.session_id == "dummy_session_id"
