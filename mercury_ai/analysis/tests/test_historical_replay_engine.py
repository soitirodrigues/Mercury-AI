"""
Testes para HistoricalReplayEngine (Sprint 1.9, Bloco 5)
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch, PropertyMock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.replay_cache import ReplayCache
from mercury_ai.database.replay_storage import ReplayMetrics

# Timeout estendido: run_replay executa pipeline.analyze() (~20+ engines pesados)
# para cada candle. Com 100 candles + n_candles=5, são 35 iterações.
pytestmark = pytest.mark.timeout(300)


@pytest.fixture
def sample_df():
    """DataFrame com 100 candles de dados simulados (OHLCV)."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100, freq="5min")
    close = 100.0 + np.cumsum(np.random.randn(100) * 0.3)
    return pd.DataFrame({
        "open": close - 0.1,
        "high": close + 0.2,
        "low": close - 0.2,
        "close": close,
        "volume": np.random.randint(1000, 10000, 100),
    }, index=dates)


class TestHistoricalReplayEngineConstructor:
    """Testes do construtor."""

    def test_default_cache(self):
        engine = HistoricalReplayEngine()
        assert engine.cache is not None
        assert isinstance(engine.cache, ReplayCache)

    def test_custom_cache(self):
        cache = ReplayCache(maxsize=50)
        engine = HistoricalReplayEngine(cache=cache)
        assert engine.cache is cache

    def test_replay_stats_initial(self):
        engine = HistoricalReplayEngine()
        stats = engine.replay_stats
        assert isinstance(stats, dict)


class TestHistoricalReplayEngineBasic:
    """Testes básicos do run_replay."""

    def test_run_replay_returns_list(self, sample_df):
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        assert isinstance(metrics, list)

    def test_run_replay_returns_replay_metrics(self, sample_df):
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        if len(metrics) > 0:
            assert isinstance(metrics[0], ReplayMetrics)

    def test_run_replay_insufficient_data_returns_empty(self):
        """DataFrame muito pequeno (< 60 + n_candles) retorna lista vazia."""
        df = pd.DataFrame({
            "open": [100.0] * 10,
            "high": [101.0] * 10,
            "low": [99.0] * 10,
            "close": [100.5] * 10,
            "volume": [5000] * 10,
        })
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("TINY", df, n_candles=5, silent=True)
        assert metrics == []

    def test_run_replay_empty_dataframe(self):
        df = pd.DataFrame()
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("EMPTY", df, n_candles=5, silent=True)
        assert metrics == []

    def test_run_replay_updates_stats(self, sample_df):
        engine = HistoricalReplayEngine()
        engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        stats = engine.replay_stats
        assert "total_candles" in stats
        assert "wall_time" in stats
        assert "cache_hit_rate" in stats


class TestReplayCacheIntegration:
    """Testes de integração com ReplayCache."""

    def test_cache_populated_after_run(self, sample_df):
        cache = ReplayCache(maxsize=200)
        engine = HistoricalReplayEngine(cache=cache)
        engine.run_replay("CACHE-TEST", sample_df, n_candles=5, silent=True)
        # Cache deve ter entradas após execução
        assert cache.size > 0

    def test_second_run_uses_cache(self, sample_df):
        cache = ReplayCache(maxsize=200)
        engine = HistoricalReplayEngine(cache=cache)

        # Primeira execução
        engine.run_replay("CACHE-TEST", sample_df, n_candles=5, silent=True)
        hits_after_first = cache.stats["hits"]
        misses_after_first = cache.stats["misses"]

        # Segunda execução com mesmo símbolo e dados
        engine.run_replay("CACHE-TEST", sample_df, n_candles=5, silent=True)
        hits_after_second = cache.stats["hits"]

        # Deve ter mais hits na segunda execução
        assert hits_after_second > hits_after_first

    def test_different_symbols_separate_cache(self, sample_df):
        cache = ReplayCache(maxsize=200)
        engine = HistoricalReplayEngine(cache=cache)

        engine.run_replay("SYM-A", sample_df, n_candles=5, silent=True)
        size_after_a = cache.size

        engine.run_replay("SYM-B", sample_df, n_candles=5, silent=True)
        size_after_b = cache.size

        # Cache deve crescer com símbolos diferentes
        assert size_after_b > size_after_a


class TestSilentMode:
    """Testes do modo silencioso."""

    def test_silent_mode_no_output(self, sample_df, capsys):
        engine = HistoricalReplayEngine()
        engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_verbose_mode_has_output(self, sample_df, capsys):
        engine = HistoricalReplayEngine()
        engine.run_replay("TEST", sample_df, n_candles=5, silent=False)
        captured = capsys.readouterr()
        # Modo verbose deve imprimir progresso
        assert "Progresso" in captured.out or len(captured.out) > 0


class TestReplayEdgeCases:
    """Casos de borda."""

    def test_n_candles_large(self, sample_df):
        """n_candles grande reduz candles processáveis."""
        engine = HistoricalReplayEngine()
        metrics_small = engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        metrics_large = engine.run_replay("TEST", sample_df, n_candles=20, silent=True)
        # Mais candles forward = menos iterações
        assert len(metrics_large) <= len(metrics_small)

    def test_replay_stats_after_insufficient_data(self):
        df = pd.DataFrame({
            "open": [100.0] * 10,
            "high": [101.0] * 10,
            "low": [99.0] * 10,
            "close": [100.5] * 10,
            "volume": [5000] * 10,
        })
        engine = HistoricalReplayEngine()
        engine.run_replay("TINY", df, n_candles=5, silent=True)
        stats = engine.replay_stats
        assert stats["total_candles"] == 0
        assert stats["wall_time"] == 0.0

    def test_metrics_have_expected_fields(self, sample_df):
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("TEST", sample_df, n_candles=5, silent=True)
        if metrics:
            m = metrics[0]
            assert hasattr(m, 'mae')
            assert hasattr(m, 'mfe')
            assert hasattr(m, 'pl')
            assert hasattr(m, 'hit')