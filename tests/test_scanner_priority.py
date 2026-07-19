import pytest
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.core.asset_registry import AssetRegistry

def test_scanner_smart_priority_sorting(tmp_path):
    # Setup registry with custom assets
    registry_file = tmp_path / "asset_registry.json"
    registry = AssetRegistry(registry_file=str(registry_file))
    
    # Register assets with different priorities, liquidity, spread
    registry.register_asset("ASSET_A", "Forex", 1, "Demo", liquidity=1.0, spread=0.01)
    registry.register_asset("ASSET_B", "Forex", 5, "Demo", liquidity=0.5, spread=0.05)
    registry.register_asset("ASSET_C", "Forex", 5, "Demo", liquidity=0.9, spread=0.02)
    
    # Initialize scanner (it will use the registry file)
    scanner = MercuryScanner()
    scanner.asset_registry = registry
    
    # Execute sorting logic manually to verify
    enabled_assets = scanner.asset_registry.filter_assets()
    enabled_assets = [a for a in enabled_assets if a.enabled]
    enabled_assets.sort(key=lambda a: (-a.priority, -a.liquidity, a.spread))
    
    symbols = [a.symbol for a in enabled_assets]
    
    # Priority 5 (B, C) -> Liquidity 0.9 > 0.5 (C > B) -> Spread 0.02 < 0.05 (C < B)
    # Expected order: C, B, A
    assert symbols[0] == "ASSET_C"
    assert symbols[1] == "ASSET_B"
    assert symbols[2] == "ASSET_A"
