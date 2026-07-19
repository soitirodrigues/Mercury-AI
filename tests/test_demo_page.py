from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

def test_demo_execution_logic():
    # Verify the demo execution logic (pipeline analyze) works
    provider = YahooFinanceProvider()
    pipeline = AnalysisPipeline(
        market_service=MarketDataService(providers=[provider]),
        providers=[provider]
    )
    
    # Run a dummy analysis
    result = pipeline.analyze("BTC-USD")
    assert result.decision is not None
