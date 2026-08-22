#!/usr/bin/env python3
"""Sync data/brokers/XP.json e data/asset_registry.json com o universo suportado (62 distintos)."""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mercury_ai.config.universe import OPERATIONAL_UNIVERSE

MAP = pathlib.Path(ROOT / "reports" / "asset_universe" / "hezilex_asset_mapping.json")
mapping = json.loads(MAP.read_text(encoding="utf-8"))
distinct_supported = sorted(set(e["internal_symbol"] for e in mapping if e["mapping_status"]=="PASS"))
print(f"Distinct supported from Hezilex mapping: {len(distinct_supported)}")
print(distinct_supported)

# Update XP.json
xp_path = ROOT / "data" / "brokers" / "XP.json"
old_xp = json.loads(xp_path.read_text(encoding="utf-8")) if xp_path.exists() else []
print(f"Old XP.json: {old_xp}")
xp_path.write_text(json.dumps(distinct_supported, indent=2), encoding="utf-8")
print(f"Wrote {xp_path} with {len(distinct_supported)} symbols")

# Update asset_registry.json — preserve existing BTC-USD/ETH-USD entries but create entries for all distinct
reg_path = ROOT / "data" / "asset_registry.json"
old_reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
# Build new registry from universe
new_reg = {}
for sym in distinct_supported:
    asset = OPERATIONAL_UNIVERSE[sym]
    # Map market to category: FOREX->Forex, CRYPTO->Cripto, STOCK->Stocks, COMMODITY->Commodities
    cat_map = {"FOREX":"Forex","CRYPTO":"Cripto","STOCK":"Stocks","COMMODITY":"Commodities"}
    category = cat_map.get(asset.market, asset.market)
    # reuse old entry if exists to preserve last_operated etc, but update core fields
    if sym in old_reg:
        entry = old_reg[sym]
        # ensure enabled
        entry["enabled"]=True
        entry["category"]=category
        entry["symbol"]=sym
        entry["market"]=category
    else:
        entry = {
            "symbol": sym,
            "category": category,
            "priority": asset.priority,
            "profile": "Demo",
            "enabled": True,
            "provider": "Yahoo",
            "fallback_provider": "Polygon",
            "market": category,
            "timeframe": "5m",
            "tick_size": 0.01,
            "pip_size": 0.0001,
            "trading_session": "Standard",
            "liquidity": 1.0,
            "spread": 0.01,
            "favorite": False,
            "last_operated": 0,
            "previous_score": 0
        }
    new_reg[sym]=entry

# Keep any old entries not in distinct_supported but enabled? No, we replace fully with distinct
reg_path.write_text(json.dumps(new_reg, indent=4, ensure_ascii=False), encoding="utf-8")
print(f"Wrote {reg_path} with {len(new_reg)} entries")
print("Categories:", {v["category"] for v in new_reg.values()})
