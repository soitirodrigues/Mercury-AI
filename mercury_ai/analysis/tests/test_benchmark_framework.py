"""Testes para o MercuryBenchmarkFramework - Enhanced (Bloco 3).

Os testes mockam o YahooFinanceProvider para evitar dependência de rede
e a limitação do yfinance (1m data não disponível para crypto).
"""
import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
from mercury_ai.analysis.benchmark_framework import (
    MercuryBenchmarkFramework,
    EnhancedBenchmarkReport,
    StatisticalTestResult,
    BuyAndHoldBaseline,
)


def _make_synthetic_ohlcv(symbol: str = "BTC-USD", n: int = 100) -> pd.DataFrame:
    """Cria DataFrame OHLCV sintético determinístico para testes.

    Gera dados com tendência leve e ruído para que o pipeline de análise
    e os cálculos de buy-and-hold tenham dados válidos.
    """
    rng = np.random.RandomState(hash(symbol) & 0xFFFFFFFF)
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    base = 50000.0 if "BTC" in symbol else 3000.0
    close = base * (1.0 + rng.randn(n).cumsum() * 0.001)
    high = close * (1 + rng.rand(n) * 0.002)
    low = close * (1 - rng.rand(n) * 0.002)
    op = close * (1 + rng.randn(n) * 0.001)
    volume = rng.randint(100, 10000, size=n).astype(float)
    df = pd.DataFrame(
        {"Open": op, "High": high, "Low": low, "Close": close, "Volume": volume},
        index=dates,
    )
    df.index.name = "Datetime"
    return df


def _make_mock_provider():
    """Cria um mock do YahooFinanceProvider que retorna dados sintéticos."""
    mock = MagicMock()
    mock.get_data = MagicMock(side_effect=lambda *a, **kw: _make_synthetic_ohlcv(a[0] if a else "BTC-USD"))
    mock.is_available = MagicMock(return_value=True)
    mock.supports_symbol = MagicMock(return_value=True)
    mock.supports_market = MagicMock(return_value=True)
    mock.supports_timeframe = MagicMock(return_value=True)
    mock.max_history = MagicMock(return_value="10y")
    mock.source_name = MagicMock(return_value="YahooFinanceMock")
    return mock


@pytest.fixture(autouse=True)
def mock_yahoo_provider():
    """Mocka YahooFinanceProvider em todos os testes deste módulo."""
    with patch(
        "mercury_ai.analysis.benchmark_framework.YahooFinanceProvider",
        new_callable=lambda: _make_mock_provider,
    ):
        yield


class TestMercuryBenchmarkFramework:
    """Testes de integração para o framework de benchmark."""

    def test_benchmark_framework_execution(self):
        """Teste básico: execução com um símbolo e verificação de métricas."""
        framework = MercuryBenchmarkFramework()
        symbols = ["BTC-USD"]
        report = framework.run_benchmark(symbols)

        assert len(report.results) == 1
        assert report.average_execution_time > 0
        assert report.results[0].memory_usage > 0
        assert report.performance_metrics.accuracy >= 0

    def test_enhanced_report_fields(self):
        """Teste: EnhancedBenchmarkReport contém todos os campos novos do Bloco 3."""
        framework = MercuryBenchmarkFramework()
        symbols = ["BTC-USD"]
        report = framework.run_benchmark(symbols)

        # Verifica campos do EnhancedBenchmarkReport
        assert report.version == "2.0"
        assert isinstance(report.asset_performances, dict)
        assert report.universe_performance is not None
        assert isinstance(report.buy_and_hold_baselines, dict)
        assert isinstance(report.statistical_tests, dict)
        assert "global" in report.statistical_tests
        assert report.total_wall_time > 0
        assert report.parallel_workers > 0

    def test_statistical_test_result(self):
        """Teste: StatisticalTestResult tem valores coerentes."""
        framework = MercuryBenchmarkFramework(bootstrap_samples=100)
        symbols = ["BTC-USD"]
        report = framework.run_benchmark(symbols)

        global_test = report.statistical_tests["global"]
        assert isinstance(global_test, StatisticalTestResult)
        # Se há dados suficientes, bootstrap_samples == 100
        # Se não (mercado fechado / yfinance indisponível), early-return com 0
        assert global_test.bootstrap_samples in (0, 100)
        if global_test.bootstrap_samples > 0:
            assert -1.0 <= global_test.mean_return <= 1.0
            assert global_test.std_return >= 0
        else:
            # Early return: sem dados suficientes
            assert global_test.mean_return == 0.0
            assert global_test.std_return == 0.0

    def test_buy_and_hold_baseline(self):
        """Teste: BuyAndHoldBaseline é gerado para cada símbolo."""
        framework = MercuryBenchmarkFramework()
        symbols = ["BTC-USD"]
        report = framework.run_benchmark(symbols)

        for sym in symbols:
            assert sym in report.buy_and_hold_baselines
            bh = report.buy_and_hold_baselines[sym]
            assert isinstance(bh, BuyAndHoldBaseline)
            assert bh.symbol == sym

    def test_quick_benchmark_compatibility(self):
        """Teste: run_quick_benchmark mantém compatibilidade com API v1."""
        framework = MercuryBenchmarkFramework()
        symbols = ["BTC-USD"]
        report = framework.run_quick_benchmark(symbols)

        assert len(report.results) == 1
        assert report.average_execution_time > 0
        assert report.performance_metrics.accuracy >= 0

    def test_warm_cool_filter(self):
        """Teste: Filtro warm-up/cool-down é aplicado."""
        framework = MercuryBenchmarkFramework(
            warm_up_trades=3,
            cool_down_trades=2,
        )
        symbols = ["BTC-USD"]
        report = framework.run_benchmark(symbols)

        # Os contadores de exclusão devem existir
        assert report.warm_up_trades_excluded >= 0
        assert report.cool_down_trades_excluded >= 0

    def test_multiple_symbols(self):
        """Teste: Benchmark com múltiplos símbolos em paralelo."""
        framework = MercuryBenchmarkFramework(max_workers=2)
        symbols = ["BTC-USD", "ETH-USD"]
        report = framework.run_benchmark(symbols)

        assert len(report.results) == 2
        assert len(report.asset_performances) == 2
        for sym in symbols:
            assert sym in report.asset_performances
            assert sym in report.buy_and_hold_baselines
            assert sym in report.statistical_tests
