import pytest
from mercury_ai.core.auto_health import MercuryAutoHealth
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider
from mercury_ai.core.asset_registry import AssetRegistry

def test_auto_health_checks():
    manager = MercuryDataProvider()
    registry = AssetRegistry()
    registry.register_asset("BTC-USD", "Cripto", 5, "Demo")
    
    auto_health = MercuryAutoHealth(manager, registry)
    results = auto_health.run_all_checks()
    
    assert results["Providers"] is True
    assert results["Scanner"] is True
    assert results["AssetRegistry"] is True
    assert results["Logs"] is True
