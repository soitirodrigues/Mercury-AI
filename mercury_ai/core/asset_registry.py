import json
import os
import tempfile
import threading
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
    """Registro de ativos com persistência JSON thread-safe e atômica.

    - Thread-safe: threading.Lock protege todas as operações de leitura/escrita.
    - Escrita atômica: temp file + os.replace() para evitar corrupção.
    """

    def __init__(self, registry_file: str = "data/asset_registry.json"):
        self.registry_file = registry_file
        self.assets: Dict[str, Asset] = {}
        self._lock = threading.Lock()
        self._load_from_file()

    def _load_from_file(self):
        with self._lock:
            if os.path.exists(self.registry_file):
                try:
                    with open(self.registry_file, "r") as f:
                        data = json.load(f)
                    for symbol, details in data.items():
                        self.assets[symbol] = Asset(**details)
                except (json.JSONDecodeError, TypeError):
                    # Arquivo corrompido ou vazio — começa com registro limpo
                    pass

    def save(self):
        with self._lock:
            self._atomic_write()

    def _atomic_write(self):
        """Escrita atômica: temp file no mesmo diretório + os.replace()."""
        dir_name = os.path.dirname(self.registry_file) or "."
        os.makedirs(dir_name, exist_ok=True)
        data = json.dumps(
            {s: a.__dict__ for s, a in self.assets.items()}, indent=4
        )
        fd, tmp_path = tempfile.mkstemp(suffix=".tmp", prefix=".reg_", dir=dir_name)
        try:
            with os.fdopen(fd, "w") as f:
                f.write(data)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp_path, self.registry_file)
        except OSError:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    def register_asset(self, symbol: str, category: str, priority: int, profile: str, enabled: bool = True,
                       provider: str = "Yahoo", fallback_provider: str = "Polygon", market: str = "Stocks",
                       timeframe: str = "5m", tick_size: float = 0.01, pip_size: float = 0.0001,
                       trading_session: str = "Standard", liquidity: float = 1.0, spread: float = 0.01,
                       favorite: bool = False, last_operated: float = 0.0, previous_score: float = 0.0):
        with self._lock:
            self.assets[symbol] = Asset(symbol, category, priority, profile, enabled, provider, fallback_provider,
                                        market, timeframe, tick_size, pip_size, trading_session, liquidity, spread,
                                        favorite, last_operated, previous_score)
            self._atomic_write()

    def set_enabled(self, symbol: str, enabled: bool):
        with self._lock:
            if symbol in self.assets:
                self.assets[symbol].enabled = enabled
                self._atomic_write()

    def set_priority(self, symbol: str, priority: int):
        with self._lock:
            if symbol in self.assets:
                self.assets[symbol].priority = priority
                self._atomic_write()

    def update_asset_stats(self, symbol: str, score: float):
        with self._lock:
            if symbol in self.assets:
                self.assets[symbol].last_operated = time.time()
                self.assets[symbol].previous_score = score
                self._atomic_write()

    def get_enabled_assets(self) -> List[str]:
        with self._lock:
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
        with self._lock:
            query = query.lower()
            return [a for a in self.assets.values() if query in a.symbol.lower()]

    def filter_assets(self, category: Optional[str] = None) -> List[Asset]:
        with self._lock:
            if not category:
                return list(self.assets.values())
            return [a for a in self.assets.values() if a.category == category]
