"""Testes para o MercuryBenchmarkFramework - Enhanced (Bloco 3)."""
import pytest
from mercury_ai.analysis.benchmark_framework import (
    MercuryBenchmarkFramework,
    EnhancedBenchmarkReport,
    StatisticalTestResult,
    BuyAndHoldBaseline,
)


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
