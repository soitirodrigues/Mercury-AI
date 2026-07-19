import json
import os
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Asset:
    symbol: str
    category: str
    priority: int
    profile: str
    enabled: bool = True
    provider: str = "Yahoo"
    fallback_provider: str = "Polygon"
    market: str = "Stocks"
    timeframe: str = "5m"
    tick_size: float = 0.01
    pip_size: float = 0.0001
    trading_session: str = "Standard"
    liquidity: float = 1.0
    spread: float = 0.01
    favorite: bool = False
    last_operated: float = 0.0
    previous_score: float = 0.0

class AssetRegistry:
    def __init__(self, registry_file: str = "data/asset_registry.json"):
        self.registry_file = registry_file
        self.assets: Dict[str, Asset] = {}
        self._load_from_file()

    def _load_from_file(self):
        if os.path.exists(self.registry_file):
            with open(self.registry_file, "r") as f:
                try:
                    data = json.load(f)
                    for symbol, details in data.items():
                        self.assets[symbol] = Asset(**details)
                except json.JSONDecodeError:
                    pass

    def save(self):
        os.makedirs(os.path.dirname(self.registry_file), exist_ok=True)
        with open(self.registry_file, "w") as f:
            json.dump({s: a.__dict__ for s, a in self.assets.items()}, f, indent=4)

    def register_asset(self, symbol: str, category: str, priority: int, profile: str, enabled: bool = True,
                       provider: str = "Yahoo", fallback_provider: str = "Polygon", market: str = "Stocks",
                       timeframe: str = "5m", tick_size: float = 0.01, pip_size: float = 0.0001,
                       trading_session: str = "Standard", liquidity: float = 1.0, spread: float = 0.01,
                       favorite: bool = False, last_operated: float = 0.0, previous_score: float = 0.0):
        self.assets[symbol] = Asset(symbol, category, priority, profile, enabled, provider, fallback_provider,
                                    market, timeframe, tick_size, pip_size, trading_session, liquidity, spread,
                                    favorite, last_operated, previous_score)
        self.save()

    def set_enabled(self, symbol: str, enabled: bool):
        if symbol in self.assets:
            self.assets[symbol].enabled = enabled
            self.save()

    def set_priority(self, symbol: str, priority: int):
        if symbol in self.assets:
            self.assets[symbol].priority = priority
            self.save()

    def update_asset_stats(self, symbol: str, score: float):
        if symbol in self.assets:
            self.assets[symbol].last_operated = time.time()
            self.assets[symbol].previous_score = score
            self.save()

    def get_enabled_assets(self) -> List[str]:
        return [s for s, a in self.assets.items() if a.enabled]

    def get_assets_for_broker(self, broker_name: str) -> List[str]:
        broker_file = f"data/brokers/{broker_name}.json"
        if not os.path.exists(broker_file):
            return []
        with open(broker_file, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

    def search_assets(self, query: str) -> List[Asset]:
        query = query.lower()
        return [a for a in self.assets.values() if query in a.symbol.lower()]

    def filter_assets(self, category: Optional[str] = None) -> List[Asset]:
        if not category:
            return list(self.assets.values())
        return [a for a in self.assets.values() if a.category == category]
