"""
Replay Batch Processor - Parallel multi-symbol replay (Sprint 1.9, Bloco 5)

Processa replay histórico para múltiplos símbolos em paralelo usando
ThreadPoolExecutor, com coleta de métricas agregadas e relatório consolidado.

Melhorias sobre o loop sequencial:
- Paralelismo por símbolo (não por candle)
- Coleta de métricas de performance por worker
- Timeout configurável por símbolo
- Fallback graceful em caso de falha de um símbolo
"""

import time
import threading
import logging
import json
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import pandas as pd

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.analysis.replay_cache import ReplayCache
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
from mercury_ai.database.replay_storage import ReplayMetrics
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class BatchReplayResult:
    """Resultado de replay para um único símbolo no batch."""
    symbol: str
    metrics: Tuple[ReplayMetrics, ...]
    asset_performance: AssetPerformance
    wall_time: float
    cache_stats: dict
    error: Optional[str] = None


@dataclass(frozen=True)
class BatchReplayReport:
    """Relatório consolidado de replay em batch."""
    version: str = "2.0"
    total_symbols: int = 0
    successful: int = 0
    failed: int = 0
    total_wall_time: float = 0.0
    results: Tuple[BatchReplayResult, ...] = ()
    universe_performance: Optional[UniversePerformance] = None
    aggregate_cache_stats: Dict[str, float] = field(default_factory=dict)
    errors: Tuple[str, ...] = ()


class ReplayBatchProcessor:
    """
    Processador de replay em batch com paralelismo.

    Uso:
        processor = ReplayBatchProcessor(max_workers=4, cache_size=512)
        data_map = {"BTC-USD": df_btc, "ETH-USD": df_eth}
        report = processor.run_batch(data_map, n_candles=20)
    """

    def __init__(
        self,
        max_workers: int = 4,
        cache_size: int = 256,
        symbol_timeout: float = 300.0,
        risk_free_rate: float = 0.0,
    ):
        """
        Args:
            max_workers: Número máximo de workers paralelos.
            cache_size: Tamanho máximo do cache LRU por worker.
            symbol_timeout: Timeout em segundos por símbolo.
            risk_free_rate: Taxa livre de risco para Sharpe/Sortino.
        """
        self.max_workers = max_workers
        self.cache_size = cache_size
        self.symbol_timeout = symbol_timeout
        self.risk_free_rate = risk_free_rate

    def run_batch(
        self,
        data_map: Dict[str, pd.DataFrame],
        n_candles: int = 20,
    ) -> BatchReplayReport:
        """
        Executa replay em paralelo para múltiplos símbolos.

        Args:
            data_map: Dicionário {symbol: DataFrame} com dados históricos.
            n_candles: Número de candles à frente para cálculo de PL/MAE/MFE.

        Returns:
            BatchReplayReport com resultados consolidados.
        """
        if not data_map:
            return BatchReplayReport()

        results: List[BatchReplayResult] = []
        errors: List[Tuple[str, str]] = []
        all_asset_metrics: Dict[str, List[ReplayMetrics]] = {}

        start_time = time.perf_counter()

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {
                executor.submit(
                    self._run_single_symbol, symbol, df, n_candles
                ): symbol
                for symbol, df in data_map.items()
            }

            for future in as_completed(futures):
                symbol = futures[future]
                try:
                    result = future.result(timeout=self.symbol_timeout)
                    results.append(result)
                    if result.error is None:
                        all_asset_metrics[symbol] = list(result.metrics)
                    else:
                        errors.append((symbol, result.error))
                except TimeoutError:
                    errors.append((symbol, f"Timeout após {self.symbol_timeout}s"))
                except (RuntimeError, ValueError, TypeError, KeyError, OSError, AttributeError) as e:
                    errors.append((symbol, str(e)))

        total_wall_time = time.perf_counter() - start_time

        # Calcula performance do universo
        perf_engine = PerformanceEngine(risk_free_rate=self.risk_free_rate)
        universe_perf = None
        if all_asset_metrics:
            universe_perf = perf_engine.calculate_universe_performance(all_asset_metrics)

        # Agrega estatísticas de cache
        aggregate_cache = self._aggregate_cache_stats(results)

        # Persiste a memória institucional ao final do batch
        try:
            InstitutionalMemoryEngine().flush()
        except (OSError, json.JSONDecodeError, TypeError, RuntimeError) as e:
            logger.error("Failed to flush institutional memory at end of batch: %s", e, exc_info=True)

        return BatchReplayReport(
            version="2.0",
            total_symbols=len(data_map),
            successful=len([r for r in results if r.error is None]),
            failed=len(errors),
            total_wall_time=total_wall_time,
            results=tuple(results),
            universe_performance=universe_perf,
            aggregate_cache_stats=aggregate_cache,
            errors=tuple(errors),
        )

    def _run_single_symbol(
        self,
        symbol: str,
        df: pd.DataFrame,
        n_candles: int,
    ) -> BatchReplayResult:
        """Executa replay para um único símbolo (chamado em thread separada)."""
        import time as time_module

        cache = ReplayCache(maxsize=self.cache_size)
        engine = HistoricalReplayEngine(cache=cache)

        t0 = time_module.perf_counter()
        try:
            metrics = engine.run_replay(symbol, df, n_candles=n_candles)
        except (RuntimeError, ValueError, TypeError, KeyError, OSError, IndexError) as e:
            wall_time = time_module.perf_counter() - t0
            return BatchReplayResult(
                symbol=symbol,
                metrics=(),
                asset_performance=AssetPerformance(
                    asset=symbol, total_trades=0, pnl_accumulated=0.0,
                    win_rate=0.0, profit_factor=0.0, expectancy=0.0,
                    avg_win=0.0, avg_loss=0.0, max_drawdown=0.0,
                    recovery_time_candles=0, sharpe_ratio=0.0,
                    sortino_ratio=0.0, equity_curve=()
                ),
                wall_time=time_module.perf_counter() - t0,
                cache_stats=cache.stats,
                error=str(e),
            )

        wall_time = time_module.perf_counter() - t0

        # Calcula performance do ativo
        perf_engine = PerformanceEngine(risk_free_rate=self.risk_free_rate)
        asset_perf = perf_engine.calculate_asset_performance(symbol, metrics)

        return BatchReplayResult(
            symbol=symbol,
            metrics=tuple(metrics),
            asset_performance=asset_perf,
            wall_time=wall_time,
            cache_stats=cache.stats,
        )

    @staticmethod
    def _aggregate_cache_stats(results: List[BatchReplayResult]) -> Dict[str, float]:
        """Agrega estatísticas de cache de todos os resultados."""
        total_hits = sum(r.cache_stats.get("hits", 0) for r in results)
        total_misses = sum(r.cache_stats.get("misses", 0) for r in results)
        total_requests = total_hits + total_misses
        return {
            "total_hits": total_hits,
            "total_misses": total_misses,
            "aggregate_hit_rate": total_hits / total_requests if total_requests > 0 else 0.0,
            "total_cache_entries": sum(r.cache_stats.get("size", 0) for r in results),
        }