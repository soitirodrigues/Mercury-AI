"""
Mercury Benchmark Framework - Enhanced (Sprint 1.9, Bloco 3)

Melhorias:
- Outcomes reais via HistoricalReplayProvider (não mais dummy 0.01/-0.01)
- Integração com PerformanceEngine para métricas financeiras reais
- Suporte a múltiplos providers (YahooFinance + HistoricalReplay)
- Fase de warm-up/cool-down para evitar cold-start bias
- Comparação buy-and-hold como baseline
- Testes estatísticos (t-test de uma amostra, bootstrap confidence intervals)
- Execução paralela com ThreadPoolExecutor
- Relatório enriquecido com todas as novas métricas
"""

import time
import tracemalloc
import os
import psutil
import logging
import numpy as np
from typing import List, Dict, Optional, Tuple, Mapping
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.models.benchmark_report import BenchmarkRunResult, BenchmarkReport
from mercury_ai.analysis.metric_calculator import MetricCalculator, PerformanceMetrics
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance
from mercury_ai.utils.deterministic_clock import DeterministicClock

logger = logging.getLogger(__name__)
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider


@dataclass(frozen=True)
class StatisticalTestResult:
    """Resultado de testes estatísticos sobre os retornos."""
    t_statistic: float
    p_value: float
    is_significant_95: bool
    bootstrap_ci_lower: float
    bootstrap_ci_upper: float
    bootstrap_samples: int
    mean_return: float
    std_return: float


@dataclass(frozen=True)
class BuyAndHoldBaseline:
    """Resultado da estratégia buy-and-hold como baseline comparativa."""
    symbol: str
    total_return_pct: float
    max_drawdown_pct: float
    sharpe_ratio: float
    benchmark_outperformance_pct: float  # quanto a estratégia superou (ou não) o B&H


@dataclass(frozen=True)
class EnhancedBenchmarkReport:
    """Relatório de benchmark enriquecido com todas as métricas do Bloco 3."""
    version: str
    results: Tuple[BenchmarkRunResult, ...]
    average_execution_time: float
    performance_metrics: PerformanceMetrics
    # Novos campos Bloco 3
    asset_performances: Mapping[str, AssetPerformance]
    universe_performance: Optional[UniversePerformance]
    buy_and_hold_baselines: Mapping[str, BuyAndHoldBaseline]
    statistical_tests: Mapping[str, StatisticalTestResult]
    warm_up_trades_excluded: int
    cool_down_trades_excluded: int
    total_wall_time: float
    parallel_workers: int


class MercuryBenchmarkFramework:
    """
    Framework de benchmark institucional para o Mercury AI.

    Executa o pipeline de análise sobre uma lista de símbolos e coleta:
    - Tempo de execução por símbolo
    - Consumo de memória (tracemalloc + psutil RSS fallback)
    - Métricas de decisão (accuracy, precision, recall, F1, MCC)
    - Métricas financeiras (PnL, Sharpe, Sortino, drawdown) via PerformanceEngine
    - Comparação buy-and-hold como baseline
    - Testes estatísticos de significância
    - Fases de warm-up e cool-down para evitar viés de cold-start
    """

    def __init__(
        self,
        use_historical_replay: bool = True,
        warm_up_trades: int = 5,
        cool_down_trades: int = 3,
        max_workers: int = 4,
        risk_free_rate: float = 0.0,
        bootstrap_samples: int = 1000,
    ):
        """
        Args:
            use_historical_replay: Se True (default), obtém outcome REAL de mercado
                                   (via YahooFinanceProvider) — nunca deriva o outcome
                                   do próprio score do modelo. Se False, outcome neutro
                                   0.0 com aviso (correção B3: elimina auto-validação).
            warm_up_trades: Número de trades iniciais a descartar (cold-start).
            cool_down_trades: Número de trades finais a descartar.
            max_workers: Número de workers para execução paralela.
            risk_free_rate: Taxa livre de risco para Sharpe/Sortino.
            bootstrap_samples: Número de amostras bootstrap para intervalos de confiança.
        """
        self.warm_up_trades = warm_up_trades
        self.cool_down_trades = cool_down_trades
        self.max_workers = max_workers
        self.risk_free_rate = risk_free_rate
        self.bootstrap_samples = bootstrap_samples
        self.use_historical_replay = use_historical_replay

        # Provider principal
        provider = YahooFinanceProvider()
        self.pipeline = AnalysisPipeline(
            market_service=MarketDataService(providers=[provider]),
            providers=[provider]
        )

        # Performance Engine para métricas financeiras reais
        self.performance_engine = PerformanceEngine(risk_free_rate=risk_free_rate)

        tracemalloc.start()

    # ------------------------------------------------------------------
    # Execução single-symbol (usada internamente pelo paralelo)
    # ------------------------------------------------------------------
    def _run_single_symbol(self, symbol: str) -> Tuple[BenchmarkRunResult, List[float], List[str], List[float]]:
        """
        Executa o pipeline para um único símbolo e coleta métricas.
        Retorna: (BenchmarkRunResult, outcomes_list, decisions_list, scores_list)
        """
        process = psutil.Process(os.getpid())
        tracemalloc.clear_traces()
        start_time = time.perf_counter()

        result = self.pipeline.analyze(symbol)

        end_time = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()

        memory = float(peak)
        if memory == 0:
            memory = float(process.memory_info().rss)

        # Outcome REAL de mercado (não circular). NUNCA deriva o outcome do
        # próprio score/decision do modelo (evita auto-validação — achado B3).
        if self.use_historical_replay:
            outcome = self._get_real_outcome(symbol, result.decision.decision)
        else:
            # Replay desabilitado explicitamente: outcome NEUTRO (0.0) com aviso
            # claro — NÃO fabrica P/L a partir do score do modelo.
            logger.warning(
                "Real outcomes disabled (use_historical_replay=False); "
                "outcome=0.0 (neutral, non-circular) for %s", symbol
            )
            outcome = 0.0

        run_result = BenchmarkRunResult(
            timestamp=DeterministicClock.utcnow().isoformat(),
            symbol=symbol,
            decision_result=result.decision,
            execution_time=end_time - start_time,
            memory_usage=memory,
        )

        return run_result, [outcome], [result.decision.decision], [result.decision.score]

    def _get_real_outcome(self, symbol: str, decision: str) -> float:
        """
        Obtém o outcome real do mercado para o símbolo.
        Usa o YahooFinanceProvider para pegar o próximo candle e calcular retorno.
        """
        try:
            provider = YahooFinanceProvider()
            df = provider.get_data(symbol)
            if df is not None and len(df) >= 2:
                # Retorno do candle seguinte como outcome
                close_current = float(df.iloc[-2]["Close"])
                close_next = float(df.iloc[-1]["Close"])
                raw_return = (close_next - close_current) / close_current
                if decision == "SELL":
                    raw_return = -raw_return
                return raw_return
        except (ValueError, KeyError, IndexError, ConnectionError, OSError) as e:
            logger.warning(f"Could not get real outcome for {symbol}: {e}")
        # Fallback: outcome NEUTRO (0.0) — sem dados de mercado disponíveis.
        # NUNCA deriva o outcome do score/decision do modelo (correção B3).
        return 0.0

    # ------------------------------------------------------------------
    # Warm-up / Cool-down Filter
    # ------------------------------------------------------------------
    def _apply_warm_cool_filter(
        self, outcomes: List[float], decisions: List[str], scores: List[float]
    ) -> Tuple[List[float], List[str], List[float], int, int]:
        """
        Aplica filtro de warm-up e cool-down.
        Retorna: (filtered_outcomes, filtered_decisions, filtered_scores, excluded_warm, excluded_cool)
        """
        total = len(outcomes)
        if total <= self.warm_up_trades + self.cool_down_trades:
            # Dados insuficientes para filtrar
            return outcomes, decisions, scores, 0, 0

        start = self.warm_up_trades
        end = total - self.cool_down_trades
        excluded_warm = start
        excluded_cool = total - end

        return (
            outcomes[start:end],
            decisions[start:end],
            scores[start:end],
            excluded_warm,
            excluded_cool,
        )

    # ------------------------------------------------------------------
    # Buy-and-Hold Baseline
    # ------------------------------------------------------------------
    def _compute_buy_and_hold(self, symbol: str, strategy_returns: List[float]) -> BuyAndHoldBaseline:
        """
        Calcula o retorno buy-and-hold para o mesmo período como baseline.
        """
        try:
            provider = YahooFinanceProvider()
            df = provider.get_data(symbol)
            if df is not None and len(df) >= 2:
                first_close = df.iloc[0]["Close"]
                last_close = df.iloc[-1]["Close"]
                bh_return = (last_close - first_close) / first_close

                # Drawdown do B&H
                closes = df["Close"].values
                peak = np.maximum.accumulate(closes)
                dd = (closes - peak) / peak
                bh_max_dd = float(np.min(dd))

                # Sharpe do B&H
                daily_returns = np.diff(closes) / closes[:-1]
                bh_sharpe = float(np.mean(daily_returns) / np.std(daily_returns)) if np.std(daily_returns) > 0 else 0.0

                # Outperformance da estratégia vs B&H
                strategy_total = sum(strategy_returns) if strategy_returns else 0.0
                outperformance = strategy_total - bh_return

                return BuyAndHoldBaseline(
                    symbol=symbol,
                    total_return_pct=bh_return * 100,
                    max_drawdown_pct=bh_max_dd * 100,
                    sharpe_ratio=bh_sharpe,
                    benchmark_outperformance_pct=outperformance * 100,
                )
        except (ValueError, KeyError, IndexError, ConnectionError, OSError) as e:
            logger.warning(f"Could not compute buy-and-hold baseline for {symbol}: {e}")
        # Fallback: baseline NEUTRO (zeros) — sem dados de mercado (correção B3).
        return BuyAndHoldBaseline(
            symbol=symbol,
            total_return_pct=0.0,
            max_drawdown_pct=0.0,
            sharpe_ratio=0.0,
            benchmark_outperformance_pct=0.0,
        )

    # ------------------------------------------------------------------
    # Statistical Tests
    # ------------------------------------------------------------------
    def _run_statistical_tests(self, returns: List[float], label: str) -> StatisticalTestResult:
        """
        Executa testes estatísticos sobre a série de retornos:
        - t-test de uma amostra (H0: mean = 0)
        - Bootstrap confidence interval (95%)
        """
        arr = np.array(returns)
        n = len(arr)

        if n < 2:
            return StatisticalTestResult(
                t_statistic=0.0, p_value=1.0, is_significant_95=False,
                bootstrap_ci_lower=0.0, bootstrap_ci_upper=0.0,
                bootstrap_samples=0, mean_return=0.0, std_return=0.0,
            )

        mean_ret = float(np.mean(arr))
        std_ret = float(np.std(arr, ddof=1))

        # t-test: H0: mean = 0
        if std_ret > 0:
            t_stat = mean_ret / (std_ret / np.sqrt(n))
            # Aproximação da CDF t-Student usando scipy se disponível, senão normal
            try:
                from scipy import stats as scipy_stats
                p_value = 2.0 * scipy_stats.t.sf(abs(t_stat), df=n - 1)
            except ImportError:
                # Aproximação normal
                from math import erf, sqrt
                def norm_sf(x):
                    return 0.5 * (1.0 - erf(x / sqrt(2.0)))
                p_value = 2.0 * norm_sf(abs(t_stat))
        else:
            t_stat = 0.0
            p_value = 1.0

        # Bootstrap CI 95%
        rng = np.random.RandomState(42)
        bootstrap_means = []
        for _ in range(min(self.bootstrap_samples, 10000)):
            sample = rng.choice(arr, size=n, replace=True)
            bootstrap_means.append(np.mean(sample))
        bootstrap_means = np.sort(bootstrap_means)
        ci_lower = float(bootstrap_means[int(0.025 * len(bootstrap_means))])
        ci_upper = float(bootstrap_means[int(0.975 * len(bootstrap_means))])

        return StatisticalTestResult(
            t_statistic=float(t_stat),
            p_value=float(p_value),
            is_significant_95=(p_value < 0.05),
            bootstrap_ci_lower=ci_lower,
            bootstrap_ci_upper=ci_upper,
            bootstrap_samples=len(bootstrap_means),
            mean_return=mean_ret,
            std_return=std_ret,
        )

    # ------------------------------------------------------------------
    # Main Benchmark Runner
    # ------------------------------------------------------------------
    def run_benchmark(self, symbols: List[str]) -> EnhancedBenchmarkReport:
        """
        Executa o benchmark completo sobre a lista de símbolos.

        Fluxo:
        1. Executa pipeline em paralelo (ThreadPoolExecutor)
        2. Coleta outcomes, decisions, scores
        3. Aplica filtro warm-up/cool-down
        4. Calcula métricas via MetricCalculator
        5. Calcula métricas financeiras via PerformanceEngine
        6. Calcula baseline buy-and-hold
        7. Executa testes estatísticos
        8. Retorna EnhancedBenchmarkReport
        """
        wall_start = time.perf_counter()

        # Fase 1: Execução paralela
        all_run_results: List[BenchmarkRunResult] = []
        all_outcomes: List[float] = []
        all_decisions: List[str] = []
        all_scores: List[float] = []
        symbol_outcomes: Dict[str, List[float]] = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = {executor.submit(self._run_single_symbol, sym): sym for sym in symbols}
            for future in as_completed(futures):
                sym = futures[future]
                try:
                    run_result, outcomes, decisions, scores = future.result()
                    all_run_results.append(run_result)
                    all_outcomes.extend(outcomes)
                    all_decisions.extend(decisions)
                    all_scores.extend(scores)
                    symbol_outcomes[sym] = outcomes
                except (ValueError, KeyError, IndexError, ConnectionError, OSError) as e:
                    # Log and continue
                    print(f"[Benchmark] Erro ao processar {sym}: {e}")

        # Fase 2: Warm-up / Cool-down filter
        filtered_outcomes, filtered_decisions, filtered_scores, warm_excluded, cool_excluded = (
            self._apply_warm_cool_filter(all_outcomes, all_decisions, all_scores)
        )

        # Fase 3: Métricas de classificação
        metrics = MetricCalculator.calculate(filtered_decisions, filtered_outcomes, filtered_scores)

        # Fase 4: Métricas financeiras via PerformanceEngine
        # Constrói ReplayMetrics objects para o PerformanceEngine
        from mercury_ai.database.replay_storage import ReplayMetrics

        trades_for_engine = []
        for outcome in filtered_outcomes:
            trades_for_engine.append(ReplayMetrics(
                mae=0.0,
                mfe=0.0,
                pl=outcome,
                hit=outcome > 0,
            ))

        # Asset performances
        asset_performances: Dict[str, AssetPerformance] = {}
        for sym in symbols:
            sym_trades = [
                ReplayMetrics(
                    mae=0.0, mfe=0.0, pl=o, hit=o > 0,
                )
                for o in filtered_outcomes
            ]
            asset_performances[sym] = self.performance_engine.calculate_asset_performance(sym, sym_trades)

        # Universe performance
        universe_perf = self.performance_engine.calculate_universe_performance(
            {sym: trades_for_engine for sym in symbols}
        )

        # Fase 5: Buy-and-Hold baseline
        bh_baselines: Dict[str, BuyAndHoldBaseline] = {}
        for sym in symbols:
            bh_baselines[sym] = self._compute_buy_and_hold(sym, symbol_outcomes.get(sym, []))

        # Fase 6: Testes estatísticos
        stat_tests: Dict[str, StatisticalTestResult] = {}
        stat_tests["global"] = self._run_statistical_tests(filtered_outcomes, "global")
        for sym in symbols:
            stat_tests[sym] = self._run_statistical_tests(symbol_outcomes.get(sym, []), sym)

        wall_end = time.perf_counter()

        return EnhancedBenchmarkReport(
            version="2.0",
            results=tuple(all_run_results),
            average_execution_time=(
                sum(r.execution_time for r in all_run_results) / len(all_run_results)
                if all_run_results else 0.0
            ),
            performance_metrics=metrics,
            asset_performances=asset_performances,
            universe_performance=universe_perf,
            buy_and_hold_baselines=bh_baselines,
            statistical_tests=stat_tests,
            warm_up_trades_excluded=warm_excluded,
            cool_down_trades_excluded=cool_excluded,
            total_wall_time=wall_end - wall_start,
            parallel_workers=self.max_workers,
        )

    # ------------------------------------------------------------------
    # Quick Benchmark (compatibilidade com versão anterior)
    # ------------------------------------------------------------------
    def run_quick_benchmark(self, symbols: List[str]) -> BenchmarkReport:
        """
        Modo rápido compatível com a API v1.
        Retorna BenchmarkReport (sem métricas enriquecidas).
        """
        run_results = []
        decisions = []
        outcomes = []
        scores = []

        process = psutil.Process(os.getpid())

        for symbol in symbols:
            tracemalloc.clear_traces()
            start_time = time.perf_counter()

            result = self.pipeline.analyze(symbol)

            end_time = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()

            memory = float(peak)
            if memory == 0:
                memory = float(process.memory_info().rss)

            run_results.append(BenchmarkRunResult(
                timestamp=DeterministicClock.utcnow().isoformat(),
                symbol=symbol,
                decision_result=result.decision,
                execution_time=end_time - start_time,
                memory_usage=memory,
            ))

            decisions.append(result.decision.decision)
            scores.append(result.decision.score)
            # Outcome REAL de mercado (não circular — B3). NUNCA deriva do
            # próprio score do modelo. Sem replay -> neutro 0.0 com aviso.
            if self.use_historical_replay:
                outcomes.append(self._get_real_outcome(symbol, result.decision.decision))
            else:
                logger.warning(
                    "Real outcomes disabled (use_historical_replay=False); "
                    "outcome=0.0 (neutral, non-circular) for %s", symbol
                )
                outcomes.append(0.0)

        metrics = MetricCalculator.calculate(decisions, outcomes, scores)

        return BenchmarkReport(
            version="1.0",
            results=tuple(run_results),
            average_execution_time=(
                sum(r.execution_time for r in run_results) / len(run_results)
                if run_results else 0.0
            ),
            performance_metrics=metrics,
        )
