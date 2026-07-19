import pytest
import os
import json
from mercury_ai.core.asset_registry import AssetRegistry
from mercury_ai.brain.scanner import MercuryScanner

def test_asset_registry_crud(tmp_path):
    registry_file = tmp_path / "asset_registry.json"
    registry = AssetRegistry(registry_file=str(registry_file))
    
    registry.register_asset("BTC-USD", "Cripto", 5, "Produção")
    registry.register_asset("EURUSD", "Forex", 4, "Produção", enabled=False)
    
    assert len(registry.get_enabled_assets()) == 1
    assert "BTC-USD" in registry.get_enabled_assets()
    
    registry.set_enabled("EURUSD", True)
    assert len(registry.get_enabled_assets()) == 2
    
    registry.set_priority("BTC-USD", 1)
    assert registry.assets["BTC-USD"].priority == 1

def test_scanner_integration():
    scanner = MercuryScanner()
    # The scanner should now use the AssetRegistry
    assert hasattr(scanner, 'asset_registry')
    assert isinstance(scanner.asset_registry, AssetRegistry)
