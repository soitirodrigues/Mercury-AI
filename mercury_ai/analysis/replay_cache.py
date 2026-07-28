"""
Replay Cache - LRU caching layer for Historical Replay Engine (Sprint 1.9, Bloco 5)

Fornece cache determinístico para resultados intermediários do pipeline durante
replay histórico, reduzindo recomputação de indicadores e análises já calculadas.

Estratégia de cache:
- Cache por (symbol, index) para resultados de análise
- Cache por (symbol, index, window) para indicadores rolantes
- LRU eviction com maxsize configurável
- Thread-safe para uso com ReplayBatchProcessor
"""

import threading
from collections import OrderedDict
from typing import Any, Optional, Tuple


class ReplayCache:
    """
    Cache LRU thread-safe para resultados de replay.

    Uso:
        cache = ReplayCache(maxsize=512)
        cache.put("BTC-USD", 100, snapshot)
        cached = cache.get("BTC-USD", 100)
    """

    def __init__(self, maxsize: int = 256):
        self._maxsize = max(maxsize, 1)
        self._cache: OrderedDict[Tuple[str, int], Any] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, symbol: str, index: int) -> Optional[Any]:
        """Recupera um resultado do cache. Retorna None se não encontrado."""
        key = (symbol, index)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._hits += 1
                return self._cache[key]
            self._misses += 1
            return None

    def put(self, symbol: str, index: int, value: Any) -> None:
        """Armazena um resultado no cache com evicção LRU."""
        key = (symbol, index)
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
            else:
                if len(self._cache) >= self._maxsize:
                    self._cache.popitem(last=False)
            self._cache[key] = value

    def clear(self) -> None:
        """Limpa o cache completamente."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    @property
    def hit_rate(self) -> float:
        """Taxa de acerto do cache (0.0 a 1.0)."""
        total = self._hits + self._misses
        if total == 0:
            return 0.0
        return self._hits / total

    @property
    def size(self) -> int:
        """Número atual de entradas no cache."""
        with self._lock:
            return len(self._cache)

    @property
    def stats(self) -> dict:
        """Estatísticas do cache."""
        with self._lock:
            return {
                "size": len(self._cache),
                "maxsize": self._maxsize,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": self.hit_rate,
            }

    def __len__(self) -> int:
        return self.size

    def __contains__(self, key: Tuple[str, int]) -> bool:
        with self._lock:
            return key in self._cache