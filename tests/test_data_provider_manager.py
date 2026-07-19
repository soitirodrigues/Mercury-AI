import pytest
from mercury_ai.data.mercury_data_provider import MercuryDataProvider, YahooProvider, BinanceProvider

def test_data_provider_manager():
    manager = MercuryDataProvider()
    yahoo = YahooProvider()
    binance = BinanceProvider()
    
    # Set Binance as higher priority than Yahoo for the test
    yahoo.priority = 2
    binance.priority = 1
    
    manager.register_provider(yahoo)
    manager.register_provider(binance)
    
    assert "Yahoo" in manager.list_providers()
    assert manager.provider_status("Yahoo") is True
    
    # Check best provider for BTC-USD (should be Binance priority 1)
    best = manager.best_provider("BTC-USD")
    assert best.name == "Binance"
    
    # Check healthcheck
    health = manager.healthcheck()
    assert health["Yahoo"] is True
    assert health["Binance"] is True
