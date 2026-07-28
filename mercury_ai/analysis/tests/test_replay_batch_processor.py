"""
Testes para ReplayBatchProcessor (Sprint 1.9, Bloco 5)
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import MagicMock, patch
from mercury_ai.analysis.replay_batch_processor import (
    ReplayBatchProcessor,
    BatchReplayResult,
    BatchReplayReport,
)
from mercury_ai.database.replay_storage import ReplayMetrics
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance


@pytest.fixture
def sample_data_map():
    """Mapa de símbolos para DataFrames de 100 candles (OHLCV lowercase)."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100, freq="5min")
    data_map = {}
    for symbol in ["BTC-USD", "ETH-USD", "SOL-USD"]:
        close = 100.0 + np.cumsum(np.random.randn(100) * 0.3)
        data_map[symbol] = pd.DataFrame({
            "open": close - 0.1,
            "high": close + 0.2,
            "low": close - 0.2,
            "close": close,
            "volume": np.random.randint(1000, 10000, 100),
        }, index=dates)
    return data_map


class TestBatchReplayResult:
    """Testes do dataclass BatchReplayResult."""

    def test_creation(self):
        result = BatchReplayResult(
            symbol="BTC-USD",
            metrics=(),
            asset_performance=None,
            wall_time=150.0,
            cache_stats={"hits": 10, "misses": 5},
            error=None,
        )
        assert result.symbol == "BTC-USD"
        assert result.wall_time == 150.0
        assert result.cache_stats == {"hits": 10, "misses": 5}
        assert result.error is None

    def test_frozen(self):
        result = BatchReplayResult(
            symbol="ETH-USD",
            metrics=(),
            asset_performance=None,
            wall_time=0.0,
            cache_stats={},
            error=None,
        )
        with pytest.raises(Exception):
            result.symbol = "BTC-USD"  # type: ignore

    def test_with_error(self):
        result = BatchReplayResult(
            symbol="FAIL-USD",
            metrics=(),
            asset_performance=None,
            wall_time=0.0,
            cache_stats={},
            error="Timeout",
        )
        assert result.error == "Timeout"


class TestBatchReplayReport:
    """Testes do dataclass BatchReplayReport."""

    def test_creation(self):
        report = BatchReplayReport(
            version="1.0",
            total_symbols=0,
            successful=0,
            failed=0,
            total_wall_time=0.0,
            results=(),
            universe_performance=None,
            aggregate_cache_stats={},
            errors=(),
        )
        assert report.total_symbols == 0
        assert report.successful == 0
        assert report.failed == 0

    def test_frozen(self):
        report = BatchReplayReport(
            version="1.0",
            total_symbols=0,
            successful=0,
            failed=0,
            total_wall_time=0.0,
            results=(),
            universe_performance=None,
            aggregate_cache_stats={},
            errors=(),
        )
        with pytest.raises(Exception):
            report.total_symbols = 5  # type: ignore


class TestReplayBatchProcessorBasic:
    """Testes básicos do processador batch."""

    def test_constructor(self):
        processor = ReplayBatchProcessor(max_workers=4, symbol_timeout=30.0)
        assert processor.max_workers == 4
        assert processor.symbol_timeout == 30.0

    def test_constructor_defaults(self):
        processor = ReplayBatchProcessor()
        assert processor.max_workers == 4
        assert processor.symbol_timeout == 300.0

    def test_run_batch_empty_data_map(self):
        processor = ReplayBatchProcessor()
        report = processor.run_batch({}, n_candles=10)
        assert isinstance(report, BatchReplayReport)
        assert report.total_symbols == 0
        assert report.results == ()

    def test_run_batch_single_symbol(self, sample_data_map):
        single_map = {"BTC-USD": sample_data_map["BTC-USD"]}
        processor = ReplayBatchProcessor(max_workers=1)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(single_map, n_candles=5)

        assert report.total_symbols == 1
        assert len(report.results) == 1
        assert report.results[0].symbol == "BTC-USD"
        assert report.results[0].error is None

    def test_run_batch_multiple_symbols(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=2)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(sample_data_map, n_candles=5)

        assert report.total_symbols == 3
        assert len(report.results) == 3
        symbols = {r.symbol for r in report.results}
        assert symbols == {"BTC-USD", "ETH-USD", "SOL-USD"}

    def test_run_batch_all_success_no_errors(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=2)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(sample_data_map, n_candles=5)

        assert report.failed == 0
        assert report.successful == 3
        assert all(r.error is None for r in report.results)


class TestBatchProcessorErrorHandling:
    """Testes de tratamento de erros."""

    def test_symbol_error_is_captured(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=1)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_engine.run_replay.side_effect = RuntimeError("Falha simulada")
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(
                {"FAIL-USD": sample_data_map["BTC-USD"]}, n_candles=5
            )

        assert report.failed == 1
        assert report.successful == 0
        assert report.results[0].error == "Falha simulada"

    def test_partial_failure_mixed_results(self, sample_data_map):
        """Um símbolo falha, outros sucedem."""
        processor = ReplayBatchProcessor(max_workers=2)

        original_engine = MagicMock()
        mock_metrics = MagicMock(spec=ReplayMetrics)
        mock_metrics.pl = 0.0
        original_engine.run_replay.return_value = [mock_metrics] * 5

        failing_engine = MagicMock()
        failing_engine.run_replay.side_effect = ValueError("Erro no ETH")

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine",
            side_effect=[original_engine, failing_engine, original_engine],
        ):
            report = processor.run_batch(sample_data_map, n_candles=5)

        assert report.failed >= 1
        success_count = sum(1 for r in report.results if r.error is None)
        error_count = sum(1 for r in report.results if r.error is not None)
        assert success_count + error_count == 3


class TestCacheAggregation:
    """Testes de agregação de estatísticas de cache."""

    def test_aggregate_cache_stats_present(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=1)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(sample_data_map, n_candles=5)

        # aggregate_cache_stats é um dict
        assert isinstance(report.aggregate_cache_stats, dict)

    def test_successful_and_failed_counts(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=1)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(sample_data_map, n_candles=5)

        assert report.successful == 3
        assert report.failed == 0
        assert report.total_symbols == 3

    def test_total_wall_time(self, sample_data_map):
        processor = ReplayBatchProcessor(max_workers=1)

        with patch(
            "mercury_ai.analysis.replay_batch_processor.HistoricalReplayEngine"
        ) as mock_engine_class:
            mock_engine = MagicMock()
            mock_metrics = MagicMock(spec=ReplayMetrics)
            mock_metrics.pl = 0.0
            mock_engine.run_replay.return_value = [mock_metrics] * 5
            mock_engine_class.return_value = mock_engine

            report = processor.run_batch(sample_data_map, n_candles=5)

        assert report.total_wall_time >= 0.0