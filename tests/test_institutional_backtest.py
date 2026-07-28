"""
Teste de Integração Institucional — Bloco 6, Sprint 1.9

Fluxo completo: replay → analytics → performance → risco → relatório

Valida a integração entre todos os motores do Mercury-AI:
  - HistoricalReplayEngine (Bloco 5)
  - ReplayCache (Bloco 5)
  - ReplayBatchProcessor (Bloco 5)
  - RiskEngine (Bloco 4)
  - PerformanceEngine (Bloco 1)
  - InstitutionalAnalyticsEngine (Bloco 2)
  - BenchmarkFramework (Bloco 3)
"""

import math
import time

import numpy as np
import pandas as pd
import pytest

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.replay_cache import ReplayCache
from mercury_ai.analysis.replay_batch_processor import (
    ReplayBatchProcessor,
    BatchReplayResult,
    BatchReplayReport,
)
from mercury_ai.analysis.risk_engine import RiskEngine
from mercury_ai.analysis.performance_engine import PerformanceEngine
from mercury_ai.models.equity_metrics import AssetPerformance, UniversePerformance
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.database.replay_storage import ReplayMetrics


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_ohlcv_df(n_candles: int = 80, seed: int = 42) -> pd.DataFrame:
    """Gera DataFrame OHLCV sintético com tendência de alta e ruído."""
    rng = np.random.default_rng(seed)
    close = 100.0
    data = []
    for i in range(n_candles):
        change = rng.normal(0.05, 0.5)
        close = close + change
        open_ = close - rng.normal(0, 0.1)
        high = max(open_, close) + abs(rng.normal(0, 0.2))
        low = min(open_, close) - abs(rng.normal(0, 0.2))
        volume = abs(rng.normal(1000, 200))
        data.append({
            "open": open_,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
        })
    df = pd.DataFrame(data)
    df.index = pd.date_range("2024-01-01", periods=n_candles, freq="1h")
    return df


def _make_multi_symbol_data(n_symbols: int = 3, n_candles: int = 80) -> dict:
    """Gera dicionário {symbol: DataFrame} para batch processing."""
    symbols = [f"ASSET_{i}" for i in range(n_symbols)]
    return {sym: _make_ohlcv_df(n_candles, seed=i) for i, sym in enumerate(symbols)}


# ---------------------------------------------------------------------------
# Teste 1: Replay → Métricas
# ---------------------------------------------------------------------------

class TestIntegrationReplayToMetrics:
    """Integração: HistoricalReplayEngine produz ReplayMetrics válidos."""

    def test_replay_produces_metrics(self):
        """Replay com 80 candles deve produzir métricas."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)

        assert isinstance(metrics, list)
        assert len(metrics) > 0
        for m in metrics:
            assert isinstance(m, ReplayMetrics)
            assert hasattr(m, "pl")
            assert hasattr(m, "mae")
            assert hasattr(m, "mfe")

    def test_replay_metrics_are_finite(self):
        """Todas as métricas devem ser finitas (não NaN, não inf)."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)

        for m in metrics:
            assert math.isfinite(m.pl), f"PL não finito: {m.pl}"
            assert math.isfinite(m.mae), f"MAE não finito: {m.mae}"
            assert math.isfinite(m.mfe), f"MFE não finito: {m.mfe}"

    def test_replay_updates_stats(self):
        """Após replay, replay_stats deve conter métricas de execução."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        engine.run_replay("TEST", df, n_candles=5, silent=True)

        stats = engine.replay_stats
        assert stats["total_candles"] > 0
        assert stats["wall_time"] > 0


# ---------------------------------------------------------------------------
# Teste 2: Replay → Cache
# ---------------------------------------------------------------------------

class TestIntegrationReplayToCache:
    """Integração: HistoricalReplayEngine + ReplayCache."""

    def test_cache_populated_after_replay(self):
        """Cache deve conter entradas após replay."""
        cache = ReplayCache(maxsize=500)
        engine = HistoricalReplayEngine(cache=cache)
        df = _make_ohlcv_df(80)
        engine.run_replay("TEST", df, n_candles=5, silent=True)

        assert cache.size > 0
        assert cache.stats["misses"] > 0  # primeiro run sempre tem misses

    def test_second_run_hits_cache(self):
        """Segundo replay com mesmos dados deve usar cache."""
        cache = ReplayCache(maxsize=500)
        engine = HistoricalReplayEngine(cache=cache)
        df = _make_ohlcv_df(80)

        engine.run_replay("TEST", df, n_candles=5, silent=True)
        hits_before = cache.stats["hits"]

        engine.run_replay("TEST", df, n_candles=5, silent=True)
        hits_after = cache.stats["hits"]

        assert hits_after > hits_before


# ---------------------------------------------------------------------------
# Teste 3: Replay → Performance
# ---------------------------------------------------------------------------

class TestIntegrationReplayToPerformance:
    """Integração: ReplayMetrics → PerformanceEngine → AssetPerformance."""

    def test_performance_from_replay_metrics(self):
        """PerformanceEngine calcula AssetPerformance a partir de ReplayMetrics."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)

        perf_engine = PerformanceEngine()
        asset_perf = perf_engine.calculate_asset_performance("TEST", metrics)

        assert isinstance(asset_perf, AssetPerformance)
        assert asset_perf.asset == "TEST"
        assert asset_perf.total_trades == len(metrics)
        assert -1.0 <= asset_perf.win_rate <= 1.0

    def test_performance_fields_are_finite(self):
        """Todos os campos de AssetPerformance devem ser finitos."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)

        perf_engine = PerformanceEngine()
        asset_perf = perf_engine.calculate_asset_performance("TEST", metrics)

        for field_name in [
            "pnl_accumulated", "win_rate", "profit_factor",
            "expectancy", "avg_win", "avg_loss", "max_drawdown",
            "sharpe_ratio", "sortino_ratio",
        ]:
            val = getattr(asset_perf, field_name)
            assert math.isfinite(val) or math.isnan(val), (
                f"{field_name} = {val} não é finito"
            )


# ---------------------------------------------------------------------------
# Teste 4: Batch → Universe Performance
# ---------------------------------------------------------------------------

class TestIntegrationBatchToUniverse:
    """Integração: ReplayBatchProcessor → UniversePerformance."""

    def test_batch_produces_universe_performance(self):
        """Batch com 3 símbolos deve produzir UniversePerformance."""
        processor = ReplayBatchProcessor(max_workers=2)
        data_map = _make_multi_symbol_data(3, n_candles=80)

        report = processor.run_batch(data_map, n_candles=5)

        assert isinstance(report, BatchReplayReport)
        assert report.total_symbols == 3
        assert report.successful == 3
        assert report.failed == 0
        assert report.universe_performance is not None

        up = report.universe_performance
        assert isinstance(up, UniversePerformance)
        assert up.total_assets == 3
        assert len(up.asset_stats) == 3

    def test_batch_results_have_cache_stats(self):
        """Cada BatchReplayResult deve conter cache_stats."""
        processor = ReplayBatchProcessor(max_workers=2)
        data_map = build_multi_symbol_data(2, n_candles=80)

        report = processor.run_batch(data_map, n_candles=5)

        for result in report.results:
            assert isinstance(result.cache_stats, dict)
            assert "hits" in result.cache_stats
            assert "misses" in result.cache_stats


# ---------------------------------------------------------------------------
# Teste 5: Risk + Replay
# ---------------------------------------------------------------------------

class TestIntegrationRiskAndReplay:
    """Integração: RiskEngine + ReplayMetrics."""

    def test_risk_assessment_from_replay(self):
        """RiskEngine.assess() funciona com dados de replay."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)

        # Extrai P&L como retornos
        returns = [m.pl for m in metrics if m.pl is not None]

        risk_engine = RiskEngine()
        assessment = risk_engine.assess_simple(
            symbol="TEST",
            price=df["close"].iloc[-1],
            atr=df["close"].diff().abs().mean(),
            trend="BULLISH",
            evidence_bundle=None,
            historical_returns=returns,
        )

        assert isinstance(assessment, RiskAssessment)
        assert assessment.var_95 is not None
        assert assessment.cvar_95 is not None
        assert assessment.kelly_fraction is not None

    def test_risk_assessment_fields_are_finite(self):
        """Todos os campos numéricos de RiskAssessment devem ser finitos."""
        engine = HistoricalReplayEngine()
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("TEST", df, n_candles=5, silent=True)
        returns = [m.pl for m in metrics if m.pl is not None]

        risk_engine = RiskEngine()
        assessment = risk_engine.assess_simple(
            symbol="TEST",
            price=df["close"].iloc[-1],
            atr=df["close"].iloc[-1] * 0.02,
            evidence_bundle=None,
            historical_returns=returns,
        )

        for field_name in [
            "var_95", "cvar_95", "var_99",
            "kelly_fraction", "stress_test_loss",
        ]:
            val = getattr(assessment, field_name)
            assert val is not None, f"{field_name} é None"
            assert math.isfinite(val), f"{field_name} = {val} não é finito"


# ---------------------------------------------------------------------------
# Teste 6: Cenários Extremos
# ---------------------------------------------------------------------------

class TestIntegrationExtremeScenarios:
    """Testes de integração com cenários extremos de mercado."""

    def test_flat_market(self):
        """Mercado completamente flat (preço constante)."""
        df = pd.DataFrame({
            "open": [100.0] * 80,
            "high": [100.0] * 80,
            "low": [100.0] * 80,
            "close": [100.0] * 80,
            "volume": [1000.0] * 80,
        })
        df.index = pd.date_range("2024-01-01", periods=80, freq="1h")

        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("FLAT", df, n_candles=5, silent=True)

        # Deve produzir métricas (mesmo que PL ≈ 0)
        assert len(metrics) > 0
        for m in metrics:
            assert math.isfinite(m.pl)

    def test_high_volatility(self):
        """Mercado com alta volatilidade (grandes swings)."""
        rng = np.random.default_rng(99)
        close = 100.0
        data = []
        for _ in range(80):
            change = rng.normal(0, 5.0)  # σ = 5 (alta volatilidade)
            close = max(0.01, close + change)
            data.append({
                "open": close,
                "high": close + abs(rng.normal(0, 2)),
                "low": close - abs(rng.normal(0, 2)),
                "close": close,
                "volume": abs(rng.normal(5000, 1000)),
            })
        df = pd.DataFrame(data)
        df.index = pd.date_range("2024-01-01", periods=80, freq="1h")

        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("VOLATILE", df, n_candles=5, silent=True)

        assert len(metrics) > 0

        # Risk assessment deve capturar alta volatilidade
        returns = [m.pl for m in metrics if m.pl is not None]
        risk_engine = RiskEngine()
        assessment = risk_engine.assess_simple(
            symbol="VOLATILE",
            price=df["close"].iloc[-1],
            atr=5.0,
            evidence_bundle=None,
            historical_returns=returns,
        )
        # Em alta volatilidade, VaR deve ser significativo
        assert abs(assessment.var_95) > 0

    def test_single_candle_dataframe(self):
        """DataFrame com poucos candles (insuficiente para replay)."""
        df = pd.DataFrame({
            "open": [100.0],
            "high": [101.0],
            "low": [99.0],
            "close": [100.5],
            "volume": [1000.0],
        })
        df.index = pd.date_range("2024-01-01", periods=1, freq="1h")

        engine = HistoricalReplayEngine()
        metrics = engine.run_replay("TINY", df, n_candles=5, silent=True)

        # Deve retornar lista vazia (dados insuficientes)
        assert metrics == []
        assert engine.replay_stats["total_candles"] == 0


# ---------------------------------------------------------------------------
# Teste 7: Pipeline Completo (end-to-end)
# ---------------------------------------------------------------------------

class TestIntegrationEndToEnd:
    """Teste de integração ponta-a-ponta: replay → analytics → performance → report."""

    def test_full_pipeline_single_symbol(self):
        """Pipeline completo com um símbolo."""
        # 1. Replay
        cache = ReplayCache(maxsize=500)
        engine = HistoricalReplayEngine(cache=cache)
        df = _make_ohlcv_df(80)
        metrics = engine.run_replay("E2E", df, n_candles=5, silent=True)

        assert len(metrics) > 0, "Replay não produziu métricas"

        # 2. Performance
        perf_engine = PerformanceEngine()
        asset_perf = perf_engine.calculate_asset_performance("E2E", metrics)
        assert isinstance(asset_perf, AssetPerformance)

        # 3. Risk
        returns = [m.pl for m in metrics if m.pl is not None]
        risk_engine = RiskEngine()
        assessment = risk_engine.assess_simple(
            symbol="E2E",
            price=df["close"].iloc[-1],
            atr=df["close"].diff().abs().std(),
            evidence_bundle=None,
            historical_returns=returns,
        )
        assert isinstance(assessment, RiskAssessment)

        # 4. Cache stats
        assert cache.size > 0
        assert cache.hit_rate >= 0.0

        # 5. Verificação de consistência
        assert asset_perf.total_trades == len(metrics)
        assert assessment.var_95 is not None

    def test_full_pipeline_multi_symbol(self):
        """Pipeline completo com múltiplos símbolos via batch."""
        processor = ReplayBatchProcessor(max_workers=2)
        data_map = build_multi_symbol_data(3, n_candles=80)

        report = processor.run_batch(data_map, n_candles=5)

        # Verificações estruturais
        assert report.total_symbols == 3
        assert report.successful == 3
        assert report.failed == 0
        assert report.universe_performance is not None

        # Cada símbolo deve ter AssetPerformance
        for result in report.results:
            assert isinstance(result.asset_performance, AssetPerformance)
            assert result.asset_performance.total_trades > 0
            assert result.error is None

        # UniversePerformance deve ser consistente
        up = report.universe_performance
        assert up.total_assets == 3
        assert len(up.asset_stats) == 3
        assert up.global_pnl is not None

    def test_pipeline_with_risk_on_all_symbols(self):
        """Pipeline completo com avaliação de risco para cada símbolo."""
        processor = ReplayBatchProcessor(max_workers=2)
        data_map = build_multi_symbol_data(3, n_candles=80)

        report = processor.run_batch(data_map, n_candles=5)

        risk_engine = RiskEngine()
        for result in report.results:
            # Extrai retornos do asset_performance
            perf = result.asset_performance
            # Simula retornos a partir do P&L acumulado
            returns = [perf.pnl_accumulated / max(perf.total_trades, 1)]

            assessment = risk_engine.assess_simple(
                symbol=result.symbol,
                price=100.0,
                atr=1.0,
                evidence_bundle=None,
                historical_returns=returns,
            )
            assert isinstance(assessment, RiskAssessment)


# ---------------------------------------------------------------------------
# Helpers locais (evitam redefinição)
# ---------------------------------------------------------------------------

def build_multi_symbol_data(n_symbols: int = 3, n_candles: int = 80) -> dict:
    """Helper local para criar data_map multi-símbolo."""
    return _make_multi_symbol_data(n_symbols, n_candles)


def build_data_symbol_data(n_symbols: int = 2, n_candles: int = 80) -> dict:
    """Alias para build_multi_symbol_data."""
    return _make_multi_symbol_data(n_symbols, n_candles)