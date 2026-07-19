import pytest
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

def test_determinism():
    # Setup
    provider = YahooFinanceProvider()
    pipeline = AnalysisPipeline(
        market_service=MarketDataService(providers=[provider]),
        providers=[provider]
    )
    symbol = "GC=F"
    
    # Run twice
    res1 = pipeline.analyze(symbol)
    res2 = pipeline.analyze(symbol)
    
    # Compare DecisionResults
    assert res1.decision.audit_id == res2.decision.audit_id
    assert res1.decision.decision == res2.decision.decision
    assert res1.decision.confidence == res2.decision.confidence
    assert res1.decision.buy_probability == res2.decision.buy_probability
    
    # Compare Explanation (summary and technical_reason are key)
    assert res1.decision.summary == res2.decision.summary
    assert res1.decision.technical_reason == res2.decision.technical_reason
    
    # Compare Snapshots
    snap1 = pipeline.last_snapshots[symbol]
    snap2 = pipeline.last_snapshots[symbol]
    
    assert snap1.decision_result == snap2.decision_result
    assert snap1.evidence_ranking == snap2.evidence_ranking
    assert snap1.evidence_bundle == snap2.evidence_bundle
