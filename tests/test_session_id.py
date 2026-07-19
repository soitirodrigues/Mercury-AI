from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

def test_session_id_consistency():
    provider = YahooFinanceProvider()
    pipeline = AnalysisPipeline(
        market_service=MarketDataService(providers=[provider]),
        providers=[provider]
    )
    
    # Analyze multiple symbols in the same session
    symbol1 = "GC=F"
    symbol2 = "EURUSD=X"
    
    res1 = pipeline.analyze(symbol1)
    res2 = pipeline.analyze(symbol2)
    
    # Get snapshots from memory
    snap1 = pipeline.last_snapshots[symbol1]
    snap2 = pipeline.last_snapshots[symbol2]
    
    # Session IDs must be identical
    assert snap1.session_id == snap2.session_id
    assert snap1.session_id == pipeline.session_id
