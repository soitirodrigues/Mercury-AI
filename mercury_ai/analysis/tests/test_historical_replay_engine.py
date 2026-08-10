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
from mercury_ai.utils.deterministic_clock import DeterministicClock

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


class TestDeterministicClockIsolation:
    """B4-C1: DeterministicClock deve ser isolado durante o replay.

    O replay congela o relógio em timestamps históricos (set_time por candle);
    após run_replay, o clock NÃO pode permanecer no passado (contaminação
    temporal). A correção usa snapshot/restore em finally.
    """

    def test_clock_restored_after_normal_replay(self, sample_df):
        """A) Restauração normal: clock volta ao relógio real após replay."""
        DeterministicClock.reset()
        engine = HistoricalReplayEngine()
        engine.run_replay("CLK-A", sample_df, n_candles=5, silent=True)
        # Depois do replay, _current_time deve ser None (relógio real)
        assert DeterministicClock._current_time is None

    def test_clock_restored_after_exception(self, sample_df):
        """B) Restauração após exceção: clock volta ao real mesmo com erro.

        A exceção original NÃO é mascarada; o finally restaura o relógio.
        """
        DeterministicClock.reset()

        class FailingPipeline:
            last_snapshot = None

            def __init__(self, *a, **k):
                pass

            def analyze(self, *a, **k):
                raise RuntimeError("intentional replay failure")

        engine = HistoricalReplayEngine()
        with patch(
            "mercury_ai.analysis.historical_replay_engine.AnalysisPipeline",
            FailingPipeline,
        ):
            with pytest.raises(RuntimeError, match="intentional replay failure"):
                engine.run_replay("CLK-B", sample_df, n_candles=5, silent=True)

        # Exceção propagada; relógio deve estar restaurado
        assert DeterministicClock._current_time is None

    def test_double_replay_deterministic_and_clock_restored(self, sample_df):
        """C) Replay duplo: A == B e clock_after_A/B fora do estado histórico."""
        DeterministicClock.reset()
        engine = HistoricalReplayEngine()

        metrics_a = engine.run_replay("CLK-C1", sample_df, n_candles=5, silent=True)
        clock_after_a = DeterministicClock._current_time

        metrics_b = engine.run_replay("CLK-C2", sample_df, n_candles=5, silent=True)
        clock_after_b = DeterministicClock._current_time

        # Determinístico: listas de P/L idênticas
        pl_a = [m.pl for m in metrics_a]
        pl_b = [m.pl for m in metrics_b]
        assert pl_a == pl_b
        # Sem contaminação residual
        assert clock_after_a is None
        assert clock_after_b is None

    def test_no_contamination_of_normal_execution(self, sample_df):
        """D) Ausência de contaminação: NORMAL -> REPLAY -> NORMAL -> REPLAY.

        Execuções normais intercaladas com replays devem usar relógio real.
        """
        DeterministicClock.reset()
        engine = HistoricalReplayEngine()

        # NORMAL 1
        assert DeterministicClock._current_time is None
        # REPLAY 1
        engine.run_replay("CLK-D1", sample_df, n_candles=5, silent=True)
        # NORMAL 2 (após replay) — não contaminado
        assert DeterministicClock._current_time is None
        # REPLAY 2
        engine.run_replay("CLK-D2", sample_df, n_candles=5, silent=True)
        # NORMAL 3 (após segundo replay) — não contaminado
        assert DeterministicClock._current_time is None

    def test_empty_replay_does_not_touch_clock(self):
        """Replay vazio (dados insuficientes) não altera o estado do clock."""
        DeterministicClock.reset()
        df = pd.DataFrame({
            "open": [100.0] * 10,
            "high": [101.0] * 10,
            "low": [99.0] * 10,
            "close": [100.5] * 10,
            "volume": [5000] * 10,
        })
        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("CLK-E", df, n_candles=5, silent=True)
        assert metrics == []
        assert DeterministicClock._current_time is None