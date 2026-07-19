import pytest
from mercury_ai.data.mercury_data_provider import (
    MercuryDataProvider, YahooProvider, PolygonProvider, 
    TwelveDataProvider, AlphaVantageProvider, BinanceProvider, MetaTrader5Provider
)
from mercury_ai.analysis.provider_priority_engine import ProviderPriorityEngine

def test_provider_priority_engine_ranking():
    manager = MercuryDataProvider()
    
    # Register all providers
    manager.register_provider(YahooProvider())
    manager.register_provider(PolygonProvider())
    manager.register_provider(TwelveDataProvider())
    manager.register_provider(AlphaVantageProvider())
    manager.register_provider(BinanceProvider())
    manager.register_provider(MetaTrader5Provider())
    
    engine = ProviderPriorityEngine(manager)
    
    # Test EURUSD: Should be MT5 (Priority 1)
    provider = engine.get_optimal_provider("EURUSD")
    assert provider.name == "MetaTrader5"
    
    # Test AAPL: Should be Polygon (Priority 2)
    provider_aapl = engine.get_optimal_provider("AAPL")
    assert provider_aapl.name == "Polygon"
