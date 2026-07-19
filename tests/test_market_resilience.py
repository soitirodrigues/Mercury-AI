import pytest
from unittest.mock import MagicMock
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.core.exceptions import MarketClosedException
import pandas as pd
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

def test_pipeline_handles_market_closed():
    mock_provider = MagicMock()
    mock_provider.get_data.side_effect = MarketClosedException("Market closed or insufficient data")
    mock_provider.is_available.return_value = True
    mock_provider.supports_symbol.return_value = True
    mock_provider.source_name.return_value = "MockProvider"
    
    pipeline = AnalysisPipeline(market_service=MarketDataService(providers=[mock_provider]), providers=[mock_provider])
    
    result = pipeline.analyze("EURUSD=X")
    
    assert result.decision.decision == 'WAIT'
    assert "Market closed" in result.decision.summary

def test_market_service_raises_on_empty_df():
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
    
    service = MarketDataService(providers=[YahooFinanceProvider()])
    # Mock yfinance to return empty
    import yfinance as yf
    with pytest.MonkeyPatch.context() as m:
        m.setattr(yf.Ticker, "history", MagicMock(return_value=pd.DataFrame()))
        
        with pytest.raises(MarketClosedException):
            service.get_data("TEST")

def test_market_service_raises_on_insufficient_candles():
    from mercury_ai.data.market_data import MarketDataService
    from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider
    
    service = MarketDataService(providers=[YahooFinanceProvider()])
    # Mock yfinance to return < 20 candles
    import yfinance as yf
    with pytest.MonkeyPatch.context() as m:
        df = pd.DataFrame({'Open': [1]*10, 'High': [1]*10, 'Low': [1]*10, 'Close': [1]*10, 'Volume': [1]*10})
        m.setattr(yf.Ticker, "history", MagicMock(return_value=df))
        
        with pytest.raises(MarketClosedException):
            service.get_data("TEST")
