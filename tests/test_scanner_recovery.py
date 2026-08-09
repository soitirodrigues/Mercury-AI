import pytest
from unittest.mock import MagicMock
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.core.exceptions import ProviderError

def test_scanner_auto_recovery_triggers_failover():
    # Setup scanner with mocked pipeline and provider_manager
    scanner = MercuryScanner()
    
    # Clear the asset registry and add only our test assets
    scanner.asset_registry.assets.clear()
    scanner.asset_registry.register_asset("BTC-USD", "Cripto", 5, "Demo", enabled=True)
    scanner.asset_registry.register_asset("ETH-USD", "Cripto", 4, "Demo", enabled=True)
    
    # Mock get_assets_for_broker to return only our test assets
    scanner.asset_registry.get_assets_for_broker = MagicMock(return_value=["BTC-USD", "ETH-USD"])
    
    # Mock pipeline to raise an exception on first call (simulating provider failure)
    mock_analysis = MagicMock()
    # ... (same as before)
    mock_analysis.decision.score = 50.0 
    mock_analysis.market.symbol = "BTC-USD"
    mock_analysis.timestamp = "2026-07-14 00:00:00"
    mock_analysis.decision.decision = "BUY"
    mock_analysis.decision.confidence = 0.8
    mock_analysis.decision.buy_probability = 0.8
    mock_analysis.decision.sell_probability = 0.1
    mock_analysis.decision.wait_probability = 0.1
    mock_analysis.market_regime.regime = "BULLISH"
    
    scanner.pipeline.analyze = MagicMock(side_effect=[ProviderError("Provider Failed"), mock_analysis])
    
    # Mock printer methods
    scanner._print_report = MagicMock()
    scanner._print_ranking = MagicMock()
    scanner.brain.explain = MagicMock(return_value="Rationale")
    
    # Mock provider_manager to return True for trigger_failover
    scanner.provider_manager.trigger_failover = MagicMock(return_value=True)
    
    # Mock notification_center
    scanner.notification_center.send = MagicMock()
    
    # Run scan
    scanner.scan()
    
    # Verify failover was triggered
    assert scanner.provider_manager.trigger_failover.called
    assert scanner.notification_center.send.called
    assert scanner.pipeline.analyze.call_count == 2
