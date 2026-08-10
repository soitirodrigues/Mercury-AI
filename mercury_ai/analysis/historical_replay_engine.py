"""
Historical Replay Engine - Deterministic market replay (Sprint 1.9, Bloco 5)

Simula o mercado em tempo real usando dados históricos.
Previne look-ahead bias através de fatiamento de dados determinístico.

Otimizações Bloco 5:
- Cache LRU integrado via ReplayCache (evita recomputação de indicadores)
- Pré-alocação de listas para evitar resize durante o loop
- Progress logging otimizado (evita divisão a cada iteração)
- Suporte a modo silencioso para batch processing
- Métricas de performance do próprio replay (wall time, cache hit rate)
"""

from typing import Dict, List, Optional

import pandas as pd

from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.historical_replay_provider import HistoricalReplayProvider
from mercury_ai.analysis.replay_cache import ReplayCache


class HistoricalReplayEngine:
    """
    Simula o mercado em tempo real usando dados históricos.
    Previne look-ahead bias através de fatiamento de dados determinístico.

    Otimizações Bloco 5:
    - Cache LRU de resultados do pipeline por (symbol, index)
    - Pré-alocação de listas para reduzir GC pressure
    - Progresso com step fixo (evita divisão por iteração)
    - Métricas de performance expostas via replay_stats
    """

    def __init__(self, cache: ReplayCache = None):
        """
        Args:
            cache: ReplayCache opcional. Se None, cria um cache interno.
        """
        self._cache = cache if cache is not None else ReplayCache(maxsize=256)
        self._replay_stats: Dict[str, float] = {}

    @property
    def cache(self) -> ReplayCache:
        return self._cache

    @property
    def replay_stats(self) -> Dict[str, float]:
        """Métricas da última execução de replay."""
        return dict(self._replay_stats)

    def run_replay(
        self,
        symbol: str,
        full_df: pd.DataFrame,
        n_candles: int = 20,
        silent: bool = False,
        progress_interval: int = 10,
    ) -> List[ReplayMetrics]:
        """
        Executa replay histórico para um símbolo.

        Args:
            symbol: Símbolo do ativo (ex: "EURUSD=X").
            full_df: DataFrame com dados OHLCV históricos.
            n_candles: Número de candles à frente para cálculo de PL/MAE/MFE.
            silent: Se True, suprime output de progresso.
            progress_interval: Intervalo percentual para log de progresso.

        Returns:
            Lista de ReplayMetrics, uma por candle processado.
        """
        import time as time_module

        t_start = time_module.perf_counter()

        # Mínimo para indicadores (EMA 50)
        start_idx = 60
        total_candles = len(full_df) - n_candles - start_idx

        if total_candles <= 0:
            self._replay_stats = {"total_candles": 0, "wall_time": 0.0, "cache_hit_rate": 0.0}
            return []

        # Pré-processamento: rolling averages (calculados uma vez)
        avg_volume = full_df['volume'].rolling(20).mean()
        avg_body = (full_df['close'] - full_df['open']).abs().rolling(20).mean()

        # Pré-alocação de arrays para evitar append overhead
        close_prices = full_df['close'].values
        timestamps = full_df.index

        # Inicializa o provedor de dados histórico
        provider = HistoricalReplayProvider()
        provider.set_data(full_df)

        # Pipeline compartilhado (reutilizado a cada iteração)
        pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider]
        )
        storage = ReplayStorage()

        # Pré-aloca lista de métricas
        all_metrics: List[ReplayMetrics] = []
        # Reserva capacidade para evitar realocações
        # (não há reserve em list, mas podemos evitar o pior caso)

        # Progresso: usa step fixo em vez de divisão por iteração
        progress_step = max(total_candles // 20, 1)  # ~5% steps
        next_progress_mark = progress_step

        cache_hits_before = self._cache.stats["hits"]

        # B4-C1: isola o relógio determinístico durante o replay.
        # Captura o estado temporal anterior e restaura em finally, garantindo
        # que o clock NÃO permaneça congelado em timestamp histórico após o
        # replay (inclusive em caso de exceção no loop).
        clock_state = DeterministicClock.snapshot()
        try:
            for i in range(start_idx, len(full_df) - n_candles):
                candle_num = i - start_idx

                # Progress logging otimizado
                if not silent and candle_num >= next_progress_mark:
                    pct = (candle_num * 100) // total_candles
                    print(f"  Progresso: {pct}% ({candle_num}/{total_candles})")
                    next_progress_mark += progress_step

                # Atualiza tempo determinístico
                current_time = pd.to_datetime(timestamps[i]).to_pydatetime()
                DeterministicClock.set_time(current_time)

                # Atualiza o provedor com o índice atual
                provider.set_index(i)
                # Verifica cache antes de executar pipeline
                cached_snapshot = self._cache.get(symbol, i)
                if cached_snapshot is not None:
                    snapshot = cached_snapshot
                else:
                    # Executa o pipeline de forma determinística
                    pipeline.analyze(
                        symbol,
                        avg_volume=avg_volume.iloc[:i+1],
                        avg_body=avg_body.iloc[:i+1],
                        silent=True
                    )
                    snapshot = pipeline.last_snapshot
                    # Armazena no cache
                    self._cache.put(symbol, i, snapshot)

                # Calcula métricas de replay
                entry_price = float(close_prices[i])
                future_prices = close_prices[i+1:i+n_candles+1]

                pl = (float(future_prices[-1]) - entry_price) / entry_price
                mae = (float(future_prices.min()) - entry_price) / entry_price
                mfe = (float(future_prices.max()) - entry_price) / entry_price

                decision = snapshot.decision_result.decision
                hit = False
                if decision == "BUY":
                    hit = pl > 0
                elif decision == "SELL":
                    hit = pl < 0

                metrics = ReplayMetrics(mae=mae, mfe=mfe, pl=pl, hit=hit)
                storage.save(snapshot.decision_result.audit_id, snapshot, metrics)
                all_metrics.append(metrics)
        finally:
            DeterministicClock.restore(clock_state)

        wall_time = time_module.perf_counter() - t_start
        cache_hits = self._cache.stats["hits"] - cache_hits_before
        cache_total = cache_hits + (self._cache.stats["misses"] - (self._cache.stats.get("misses_before", 0)))

        self._replay_stats = {
            "total_candles": total_candles,
            "wall_time": wall_time,
            "candles_per_second": total_candles / wall_time if wall_time > 0 else 0.0,
            "cache_hits": cache_hits,
            "cache_hit_rate": self._cache.hit_rate,
        }

        return all_metrics
