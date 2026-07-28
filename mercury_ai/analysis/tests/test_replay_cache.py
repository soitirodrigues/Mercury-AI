"""
Testes para ReplayCache (Sprint 1.9, Bloco 5)
"""

import pytest
import threading
from mercury_ai.analysis.replay_cache import ReplayCache


class TestReplayCacheBasic:
    """Testes básicos de put/get/contains."""

    def test_put_and_get(self):
        cache = ReplayCache(maxsize=10)
        cache.put("BTC-USD", 100, {"score": 0.85})
        result = cache.get("BTC-USD", 100)
        assert result == {"score": 0.85}

    def test_get_miss_returns_none(self):
        cache = ReplayCache(maxsize=10)
        assert cache.get("BTC-USD", 100) is None

    def test_contains(self):
        cache = ReplayCache(maxsize=10)
        cache.put("ETH-USD", 50, "data")
        assert ("ETH-USD", 50) in cache
        assert ("ETH-USD", 51) not in cache

    def test_different_symbols_same_index(self):
        cache = ReplayCache(maxsize=10)
        cache.put("BTC-USD", 100, "btc")
        cache.put("ETH-USD", 100, "eth")
        assert cache.get("BTC-USD", 100) == "btc"
        assert cache.get("ETH-USD", 100) == "eth"

    def test_same_symbol_different_index(self):
        cache = ReplayCache(maxsize=10)
        cache.put("BTC-USD", 100, "t100")
        cache.put("BTC-USD", 101, "t101")
        assert cache.get("BTC-USD", 100) == "t100"
        assert cache.get("BTC-USD", 101) == "t101"

    def test_overwrite_existing_key(self):
        cache = ReplayCache(maxsize=10)
        cache.put("BTC-USD", 100, "old")
        cache.put("BTC-USD", 100, "new")
        assert cache.get("BTC-USD", 100) == "new"
        assert cache.size == 1


class TestReplayCacheLRU:
    """Testes de evicção LRU."""

    def test_evicts_oldest_when_full(self):
        cache = ReplayCache(maxsize=3)
        cache.put("A", 1, "a1")
        cache.put("A", 2, "a2")
        cache.put("A", 3, "a3")
        cache.put("A", 4, "a4")  # deve evictar (A, 1)
        assert cache.get("A", 1) is None
        assert cache.get("A", 2) == "a2"
        assert cache.get("A", 3) == "a3"
        assert cache.get("A", 4) == "a4"

    def test_get_refreshes_lru_order(self):
        cache = ReplayCache(maxsize=3)
        cache.put("A", 1, "a1")
        cache.put("A", 2, "a2")
        cache.put("A", 3, "a3")
        # Acessa (A, 1) — agora (A, 2) é o mais antigo
        cache.get("A", 1)
        cache.put("A", 4, "a4")  # deve evictar (A, 2)
        assert cache.get("A", 1) == "a1"
        assert cache.get("A", 2) is None
        assert cache.get("A", 3) == "a3"
        assert cache.get("A", 4) == "a4"

    def test_put_refreshes_lru_order(self):
        cache = ReplayCache(maxsize=3)
        cache.put("A", 1, "a1")
        cache.put("A", 2, "a2")
        cache.put("A", 3, "a3")
        cache.put("A", 1, "updated")  # atualiza (A, 1), não evicta
        assert cache.size == 3
        assert cache.get("A", 1) == "updated"

    def test_maxsize_one(self):
        cache = ReplayCache(maxsize=1)
        cache.put("A", 1, "first")
        cache.put("A", 2, "second")
        assert cache.get("A", 1) is None
        assert cache.get("A", 2) == "second"
        assert cache.size == 1


class TestCacheStats:
    """Testes de estatísticas do cache."""

    def test_initial_stats(self):
        cache = ReplayCache(maxsize=10)
        stats = cache.stats
        assert stats["size"] == 0
        assert stats["maxsize"] == 10
        assert stats["hits"] == 0
        assert stats["misses"] == 0
        assert stats["hit_rate"] == 0.0

    def test_hit_rate(self):
        cache = ReplayCache(maxsize=10)
        cache.put("A", 1, "data")
        cache.get("A", 1)  # hit
        cache.get("A", 2)  # miss
        assert cache.hit_rate == 0.5

    def test_hit_rate_zero_requests(self):
        cache = ReplayCache(maxsize=10)
        assert cache.hit_rate == 0.0

    def test_hit_rate_all_hits(self):
        cache = ReplayCache(maxsize=10)
        cache.put("A", 1, "data")
        cache.get("A", 1)
        cache.get("A", 1)
        cache.get("A", 1)
        assert cache.hit_rate == 1.0

    def test_clear_resets_stats(self):
        cache = ReplayCache(maxsize=10)
        cache.put("A", 1, "data")
        cache.get("A", 1)
        cache.get("A", 2)
        cache.clear()
        assert cache.size == 0
        assert cache.hit_rate == 0.0
        assert cache.stats["hits"] == 0
        assert cache.stats["misses"] == 0

    def test_len(self):
        cache = ReplayCache(maxsize=10)
        assert len(cache) == 0
        cache.put("A", 1, "a")
        cache.put("A", 2, "b")
        assert len(cache) == 2


class TestReplayCacheThreadSafety:
    """Testes de segurança para uso concorrente."""

    def test_concurrent_puts(self):
        cache = ReplayCache(maxsize=100)
        errors = []

        def put_entries(symbol, start, count):
            try:
                for i in range(start, start + count):
                    cache.put(symbol, i, f"{symbol}-{i}")
            except Exception as e:
                errors.append(str(e))

        threads = [
            threading.Thread(target=put_entries, args=("A", 0, 50)),
            threading.Thread(target=put_entries, args=("B", 0, 50)),
            threading.Thread(target=put_entries, args=("C", 0, 50)),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Erros em threads: {errors}"
        # Com maxsize=100 e 150 entradas, apenas as últimas 100 sobrevivem (LRU)
        # As entradas mais antigas (índices 0-49 de A e B) podem ter sido evictadas
        # Verifica que pelo menos as entradas de C (últimas inseridas) estão presentes
        for i in range(50):
            assert cache.get("C", i) == f"C-{i}"
        # Verifica que o cache está no tamanho máximo
        assert cache.size == 100

    def test_concurrent_gets_and_puts(self):
        cache = ReplayCache(maxsize=200)
        # Pre-popula
        for i in range(100):
            cache.put("X", i, f"val-{i}")

        errors = []

        def reader():
            try:
                for _ in range(200):
                    for i in range(100):
                        cache.get("X", i)
            except Exception as e:
                errors.append(str(e))

        def writer():
            try:
                for i in range(100, 200):
                    cache.put("X", i, f"val-{i}")
            except Exception as e:
                errors.append(str(e))

        threads = [
            threading.Thread(target=reader),
            threading.Thread(target=reader),
            threading.Thread(target=writer),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert not errors, f"Erros: {errors}"


class TestReplayCacheEdgeCases:
    """Casos de borda."""

    def test_maxsize_zero_clamped_to_one(self):
        cache = ReplayCache(maxsize=0)
        assert cache.stats["maxsize"] == 1

    def test_negative_maxsize_clamped_to_one(self):
        cache = ReplayCache(maxsize=-5)
        assert cache.stats["maxsize"] == 1

    def test_clear_empty_cache(self):
        cache = ReplayCache(maxsize=10)
        cache.clear()
        assert cache.size == 0

    def test_large_number_of_entries(self):
        cache = ReplayCache(maxsize=1000)
        for i in range(500):
            cache.put("SYM", i, f"data-{i}")
        assert cache.size == 500
        for i in range(500):
            assert cache.get("SYM", i) == f"data-{i}"