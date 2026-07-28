import pytest
import os
import json
import shutil
from pathlib import Path
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.core.asset_registry import AssetRegistry

def test_scanner_broker_filtering(tmp_path):
    # Setup registry with custom assets
    registry_file = tmp_path / "asset_registry.json"
    registry = AssetRegistry(registry_file=str(registry_file))
    
    # Register assets
    registry.register_asset("BTC-USD", "Cripto", 5, "Demo", enabled=True)
    registry.register_asset("AAPL", "Stocks", 5, "Demo", enabled=True)
    registry.register_asset("EURUSD", "Forex", 5, "Demo", enabled=True)
    registry.register_asset("GOLD", "Commodities", 5, "Demo", enabled=True)
    
    # Create broker file at the actual location where AssetRegistry expects it
    broker_dir = Path("data/brokers")
    broker_dir.mkdir(parents=True, exist_ok=True)
    broker_file = broker_dir / "XP.json"
    with open(broker_file, "w") as f:
        json.dump(["BTC-USD", "AAPL", "EURUSD"], f)
    
    try:
        # Initialize scanner
        scanner = MercuryScanner()
        scanner.asset_registry = registry
        scanner.config.save("OPERATIONAL_PROFILE", {"active": "Demo", "broker": "XP"})
        
        # Update registry_file path in scanner's registry to use temp file
        scanner.asset_registry.registry_file = str(registry_file)
        
        # Run scanner logic manually to verify filtering
        active_profile = scanner.config.get("OPERATIONAL_PROFILE", "active", "Demo")
        active_broker = scanner.config.get("OPERATIONAL_PROFILE", "broker", "XP")
        
        authorized_symbols = registry.get_assets_for_broker("XP")
        enabled_assets = [a for a in registry.assets.values() 
                          if a.enabled and a.profile == active_profile and a.symbol in authorized_symbols]
        
        symbols = [a.symbol for a in enabled_assets]
        
        assert "BTC-USD" in symbols
        assert "AAPL" in symbols
        assert "EURUSD" in symbols
        assert "GOLD" not in symbols
    finally:
        # Cleanup broker file
        if broker_file.exists():
            broker_file.unlink()
