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


def _make_controlled_ohlcv(closes, start="2024-01-03 10:00") -> pd.DataFrame:
    """Cria DataFrame OHLCV com closes EXATOS para testes de janela temporal.

    Cada close é posicional: a última vela do df é a "vela de decisão" (T0)
    quando este df é passado como decision_df.
    """
    dates = pd.date_range(start, periods=len(closes), freq="5min")
    closes = [float(c) for c in closes]
    return pd.DataFrame(
        {
            "Open": closes,
            "High": [c * 1.001 for c in closes],
            "Low": [c * 0.999 for c in closes],
            "Close": closes,
            "Volume": [1000.0] * len(closes),
        },
        index=dates,
    )


class TestB4C3OutcomeContract:
    """Regressão B4-C3: contrato temporal FORWARD do _get_real_outcome.

    Contrato (correção B4-C3, elimina o overlap de 1 candle confirmado no B4-C2):
      DECISION_CANDLE = última vela do df analisado pelo pipeline (T0)
      OUTCOME_CANDLE  = 1ª vela com timestamp ESTRITAMENTE após T0 (T1)
      OUTCOME_RETURN  = (close[T1] - close[T0]) / close[T0]   (SELL inverte)

    A vela de decisão (T0) NUNCA é usada como vela de outcome. Se nenhuma vela
    estritamente após T0 estiver disponível, o outcome é NEUTRO (0.0).
    """

    SYMBOL = "SYM-USD"
    # T-2=100, T-1=102, T0=105 (decisão); T1=110, T2=120 (futuro)
    DECISION_DF = _make_controlled_ohlcv([100.0, 102.0, 105.0])
    FRESH_DF = _make_controlled_ohlcv([100.0, 102.0, 105.0, 110.0, 120.0])

    def _call_outcome(self, decision, decision_df, fresh_df):
        """Executa _get_real_outcome com o fetch 'fresco' controlado.

        O patch interno sobrescreve o autouse fixture: YahooFinanceProvider()
        retorna um provider cujo get_data devolve fresh_df (controlado).
        """
        with patch(
            "mercury_ai.analysis.benchmark_framework.YahooFinanceProvider"
        ) as m:
            provider = MagicMock()
            provider.get_data.return_value = fresh_df
            provider.is_available.return_value = True
            provider.supports_symbol.return_value = True
            provider.supports_market.return_value = True
            provider.supports_timeframe.return_value = True
            m.return_value = provider
            framework = MercuryBenchmarkFramework(use_historical_replay=True)
            return framework._get_real_outcome(
                self.SYMBOL, decision, decision_df=decision_df
            )

    def test_forward_outcome_is_first_candle_after_decision(self):
        """Outcome usa T1 (1ª vela estritamente após T0), nunca T0 ou T2."""
        outcome = self._call_outcome("BUY", self.DECISION_DF, self.FRESH_DF)
        expected = (110.0 - 105.0) / 105.0
        assert outcome == pytest.approx(expected, rel=1e-9)

    def test_no_future_candle_is_neutral(self):
        """Sem vela futura (fresh termina em T0): outcome NEUTRO 0.0.

        Regressão direta do overlap B4-C2: antes, iloc[-1] (T0, a própria vela
        de decisão) era usado como endpoint do outcome.
        """
        outcome = self._call_outcome("BUY", self.DECISION_DF, self.DECISION_DF)
        assert outcome == 0.0

    def test_decision_candle_never_is_outcome_endpoint(self):
        """A vela de decisão (T0) não é usada como endpoint do outcome.

        Antes da correção (B4-C2): outcome = (close[-1]-close[-2])/close[-2]
        com close[-1]=T0 → a própria vela de decisão era o endpoint (overlap),
        e com futuro presente ancorava em T1 e media T1→T2.
        Depois: outcome = (close[T1]-close[T0])/close[T0], ancorado em T0.
        """
        outcome = self._call_outcome("BUY", self.DECISION_DF, self.FRESH_DF)
        # endpoint = T1 (close 110); NÃO é o retorno T1→T2 (overlap pré-fix)
        assert outcome == pytest.approx((110.0 - 105.0) / 105.0, rel=1e-9)
        assert outcome != pytest.approx((120.0 - 110.0) / 110.0, rel=1e-9)

    def test_far_future_candle_does_not_interfere(self):
        """T3/T4 (futuro longínquo) não alteram o outcome do horizonte N=1."""
        far_future = _make_controlled_ohlcv([100.0, 102.0, 105.0, 110.0, 120.0, 500.0, 600.0])
        outcome = self._call_outcome("BUY", self.DECISION_DF, far_future)
        assert outcome == pytest.approx((110.0 - 105.0) / 105.0, rel=1e-9)

    def test_sensitivity_only_t0_changes_outcome(self):
        """T0 é a referência: alterar apenas T0 muda o outcome."""
        decision_df_t0_changed = _make_controlled_ohlcv([100.0, 102.0, 115.0])
        fresh_t0_changed = _make_controlled_ohlcv([100.0, 102.0, 115.0, 110.0, 120.0])
        base = self._call_outcome("BUY", self.DECISION_DF, self.FRESH_DF)
        changed = self._call_outcome("BUY", decision_df_t0_changed, fresh_t0_changed)
        assert changed != base
        assert changed == pytest.approx((110.0 - 115.0) / 115.0, rel=1e-9)

    def test_sensitivity_only_t1_changes_outcome(self):
        """T1 é a vela de outcome: alterar apenas T1 muda o outcome."""
        fresh_t1_changed = _make_controlled_ohlcv([100.0, 102.0, 105.0, 120.0, 120.0])
        outcome = self._call_outcome("BUY", self.DECISION_DF, fresh_t1_changed)
        assert outcome == pytest.approx((120.0 - 105.0) / 105.0, rel=1e-9)

    def test_sensitivity_only_t2_does_not_change_outcome(self):
        """T2 está fora do horizonte N=1: alterar apenas T2 NÃO muda o outcome."""
        fresh_t2_changed = _make_controlled_ohlcv([100.0, 102.0, 105.0, 110.0, 999.0])
        base = self._call_outcome("BUY", self.DECISION_DF, self.FRESH_DF)
        changed = self._call_outcome("BUY", self.DECISION_DF, fresh_t2_changed)
        assert changed == base

    def test_horizon_extremes(self):
        """Extremos N=1: usa T1, nunca T2 (mesmo com valores extremos)."""
        extreme = _make_controlled_ohlcv([100.0, 102.0, 100.0, 200.0, 1000.0])
        decision_df = _make_controlled_ohlcv([100.0, 102.0, 100.0])
        outcome = self._call_outcome("BUY", decision_df, extreme)
        assert outcome == pytest.approx((200.0 - 100.0) / 100.0, rel=1e-9)  # +1.0, não +9.0
        # Invertido: T1=1000, T2=200 → usa T1 (horizonte respeitado)
        inverted = _make_controlled_ohlcv([100.0, 102.0, 100.0, 1000.0, 200.0])
        outcome_inv = self._call_outcome("BUY", decision_df, inverted)
        assert outcome_inv == pytest.approx((1000.0 - 100.0) / 100.0, rel=1e-9)  # +9.0

    def test_sell_negates_forward_return(self):
        """SELL inverte o sinal do retorno forward."""
        buy = self._call_outcome("BUY", self.DECISION_DF, self.FRESH_DF)
        sell = self._call_outcome("SELL", self.DECISION_DF, self.FRESH_DF)
        assert sell == pytest.approx(-buy, rel=1e-9)
        assert sell == pytest.approx(-(110.0 - 105.0) / 105.0, rel=1e-9)

    def test_neutral_without_decision_df(self):
        """Sem decision_df (None ou vazio): outcome NEUTRO 0.0 (não adivinha T0)."""
        assert self._call_outcome("BUY", None, self.FRESH_DF) == 0.0
        empty_df = _make_controlled_ohlcv([])
        assert self._call_outcome("BUY", empty_df, self.FRESH_DF) == 0.0

    def test_exception_returns_neutral_and_logs(self, caplog):
        """Exceção no fetch fresco → NEUTRO 0.0 COM warning logado (não mascara)."""
        import logging
        with patch(
            "mercury_ai.analysis.benchmark_framework.YahooFinanceProvider"
        ) as m:
            provider = MagicMock()
            provider.get_data.side_effect = ConnectionError("boom")
            provider.is_available.return_value = True
            provider.supports_symbol.return_value = True
            m.return_value = provider
            framework = MercuryBenchmarkFramework(use_historical_replay=True)
            with caplog.at_level(
                logging.WARNING, logger="mercury_ai.analysis.benchmark_framework"
            ):
                outcome = framework._get_real_outcome(
                    self.SYMBOL, "BUY", decision_df=self.DECISION_DF
                )
        assert outcome == 0.0
        assert any("Could not get real outcome" in r.message for r in caplog.records)
