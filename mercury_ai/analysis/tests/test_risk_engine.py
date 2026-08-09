"""
Testes para RiskEngine — Bloco 4.

Cobre:
  - VaR/CVaR paramétrico e histórico
  - Kelly Criterion (full, half, quarter)
  - Matriz de correlação de Pearson
  - Stress testing com cenários extremos
  - Compatibilidade retroativa (assess sem novos parâmetros)
  - Casos de borda (retornos vazios, ativo único, volatilidade zero)
"""

import math
import pytest
from unittest.mock import MagicMock

from mercury_ai.analysis.risk_engine import RiskEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_structure import MarketStructure
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.risk_assessment import RiskAssessment


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def engine():
    """Retorna uma instância limpa do RiskEngine."""
    return RiskEngine()


@pytest.fixture
def mock_context():
    """MarketContext mínimo para testes, usando dataclasses reais."""
    market_data = MarketData(
        symbol="EURUSD",
        timeframe="H1",
        close=1.1000,
        ema9=1.0990,
        ema21=1.0980,
        ema50=1.0950,
        rsi=55.0,
        atr=0.0015,
        adx=25.0,
        macd=0.0002,
        macd_signal=0.0001,
        bollinger_upper=1.1050,
        bollinger_lower=1.0950,
        volume=10000.0,
    )
    structure = MarketStructure(trend="BULLISH")
    smart_money = SmartMoneyAnalysis(structure=structure)
    # Usamos MagicMock apenas para os campos que o RiskEngine não acessa diretamente
    ctx = MagicMock(spec=MarketContext)
    ctx.market = market_data
    ctx.smart_money = smart_money
    return ctx


@pytest.fixture
def mock_evidence_bundle():
    """MarketEvidenceBundle mínimo para testes, usando Evidence reais."""
    vol_evidence = Evidence(
        engine_name="VolatilityEngine",
        evidence_name="volatility_check",
        direction="NEUTRAL",
        strength=3.0,
        confidence=80.0,
        description="ATR-based volatility assessment",
        weight=0.3,
    )
    trend_evidence = Evidence(
        engine_name="Trend",
        evidence_name="trend_direction",
        direction="BULLISH",
        strength=7.0,
        confidence=85.0,
        description="EMA alignment bullish",
        weight=0.4,
    )
    momentum_evidence = Evidence(
        engine_name="MomentumEngine",
        evidence_name="momentum_check",
        direction="BULLISH",
        strength=6.0,
        confidence=75.0,
        description="RSI and MACD momentum",
        weight=0.3,
    )
    return MarketEvidenceBundle(
        evidences=(vol_evidence, trend_evidence, momentum_evidence),
        timestamp="2025-01-01T00:00:00",
        asset="EURUSD",
        timeframe="H1",
    )


@pytest.fixture
def sample_returns_normal():
    """Retornos sintéticos com distribuição aproximadamente normal."""
    return [
        0.001, -0.002, 0.003, -0.001, 0.000,
        -0.004, 0.002, 0.001, -0.003, 0.002,
        0.001, -0.001, 0.000, 0.002, -0.002,
        0.003, -0.001, 0.001, -0.002, 0.000,
        0.002, -0.003, 0.001, 0.000, -0.001,
        0.002, -0.001, 0.001, -0.002, 0.003,
    ]


@pytest.fixture
def sample_returns_positive():
    """Retornos majoritariamente positivos (mercado bullish)."""
    return [0.002, 0.003, 0.001, 0.004, 0.002,
            0.003, 0.001, 0.002, 0.004, 0.003,
            0.002, 0.001, 0.003, 0.002, 0.004]


@pytest.fixture
def sample_returns_negative():
    """Retornos majoritariamente negativos (mercado bearish)."""
    return [-0.002, -0.003, -0.001, -0.004, -0.002,
            -0.003, -0.001, -0.002, -0.004, -0.003,
            -0.002, -0.001, -0.003, -0.002, -0.004]


# ---------------------------------------------------------------------------
# Testes: VaR & CVaR
# ---------------------------------------------------------------------------

class TestVaRCVaR:
    """Testes para _compute_var_cvar."""

    def test_var_cvar_with_normal_returns(self, engine, sample_returns_normal):
        var_95, var_99, cvar_95 = engine._compute_var_cvar(sample_returns_normal)
        # Todos devem ser >= 0
        assert var_95 >= 0.0
        assert var_99 >= 0.0
        assert cvar_95 >= 0.0
        # VaR 99% deve ser >= VaR 95% (mais conservador)
        assert var_99 >= var_95
        # CVaR deve ser >= VaR 95% (média das perdas na cauda)
        assert cvar_95 >= var_95

    def test_var_cvar_with_positive_returns(self, engine, sample_returns_positive):
        var_95, var_99, cvar_95 = engine._compute_var_cvar(sample_returns_positive)
        # Com retornos positivos, VaR pode ser 0 (sem perdas significativas)
        assert var_95 >= 0.0
        assert var_99 >= 0.0
        assert cvar_95 >= 0.0

    def test_var_cvar_with_negative_returns(self, engine, sample_returns_negative):
        var_95, var_99, cvar_95 = engine._compute_var_cvar(sample_returns_negative)
        # Com retornos negativos, VaR deve ser > 0
        assert var_95 > 0.0
        assert var_99 > 0.0
        assert cvar_95 > 0.0
        assert var_99 >= var_95

    def test_var_cvar_empty_returns(self, engine):
        var_95, var_99, cvar_95 = engine._compute_var_cvar([])
        assert var_95 == 0.0
        assert var_99 == 0.0
        assert cvar_95 == 0.0

    def test_var_cvar_insufficient_returns(self, engine):
        """Menos de 5 retornos deve retornar zeros."""
        var_95, var_99, cvar_95 = engine._compute_var_cvar([0.01, 0.02, -0.01])
        assert var_95 == 0.0
        assert var_99 == 0.0
        assert cvar_95 == 0.0

    def test_var_cvar_zero_variance(self, engine):
        """Retornos constantes (std=0) devem retornar zeros."""
        constant = [0.01] * 20
        var_95, var_99, cvar_95 = engine._compute_var_cvar(constant)
        assert var_95 == 0.0
        assert var_99 == 0.0
        assert cvar_95 == 0.0

    def test_var_cvar_single_outlier(self, engine):
        """Um outlier negativo grande deve aumentar CVaR significativamente."""
        returns = [0.001] * 29 + [-0.10]  # 30 retornos, 1 crash
        var_95, var_99, cvar_95 = engine._compute_var_cvar(returns)
        assert var_95 > 0.0
        assert cvar_95 > var_95  # CVaR captura a cauda gorda


# ---------------------------------------------------------------------------
# Testes: Kelly Criterion
# ---------------------------------------------------------------------------

class TestKellyCriterion:
    """Testa _compute_kelly."""

    def test_kelly_default_params(self, engine):
        k_full, k_half, k_quarter = engine._compute_kelly()
        # Com defaults (55% win, 1.5 payoff)
        assert k_full >= 0.0
        assert k_half == k_full / 2.0
        assert k_quarter == k_full / 4.0

    def test_kelly_high_win_rate(self, engine):
        """Win rate alta + payoff alto = Kelly alto."""
        k_full, k_half, k_quarter = engine._compute_kelly(
            win_rate=0.70, payoff_ratio=2.0
        )
        assert k_full > 0.20  # Deve ser alto
        assert k_half == k_full / 2.0
        assert k_quarter == k_full / 4.0

    def test_kelly_low_win_rate(self, engine):
        """Win rate baixa = Kelly 0 (não apostar)."""
        k_full, k_half, k_quarter = engine._compute_kelly(
            win_rate=0.30, payoff_ratio=1.5
        )
        assert k_full == 0.0
        assert k_half == 0.0
        assert k_quarter == 0.0

    def test_kelly_breakeven(self, engine):
        """Win rate exatamente no breakeven."""
        # p*b = 1-p => p = 1/(1+b) = 1/2.5 = 0.4
        k_full, _, _ = engine._compute_kelly(win_rate=0.40, payoff_ratio=1.5)
        assert k_full == pytest.approx(0.0, abs=1e-15)  # Kelly ≈ 0 no breakeven

    def test_kelly_capped_at_max(self, engine):
        """Kelly não deve exceder KELLY_MAX_FRACTION (0.25)."""
        k_full, _, _ = engine._compute_kelly(win_rate=0.99, payoff_ratio=10.0)
        assert k_full <= 0.25

    def test_kelly_zero_payoff(self, engine):
        """Payoff zero deve resultar em Kelly zero."""
        k_full, k_half, k_quarter = engine._compute_kelly(
            win_rate=0.60, payoff_ratio=0.0
        )
        assert k_full == 0.0

    def test_kelly_win_rate_clamped(self, engine):
        """Win rate > 1.0 deve ser clampada para 1.0."""
        k_full, _, _ = engine._compute_kelly(win_rate=1.5, payoff_ratio=2.0)
        # win_rate=1.0, payoff=2.0 => kelly = (1*2 - 0)/2 = 1.0, capped at 0.25
        assert k_full == 0.25

    def test_kelly_negative_win_rate_clamped(self, engine):
        """Win rate < 0 deve ser clampada para 0."""
        k_full, _, _ = engine._compute_kelly(win_rate=-0.5, payoff_ratio=2.0)
        assert k_full == 0.0


# ---------------------------------------------------------------------------
# Testes: Correlation Matrix
# ---------------------------------------------------------------------------

class TestCorrelationMatrix:
    """Testa _compute_correlation_matrix."""

    def test_correlation_two_assets_perfect_positive(self, engine):
        """Dois ativos com retornos idênticos = correlação 1.0."""
        returns = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.00, 0.02, -0.02]
        asset_map = {"BTC": returns, "ETH": returns}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is not None
        assert len(matrix) == 2
        assert len(matrix[0]) == 2
        # Diagonal = 1.0
        assert matrix[0][0] == 1.0
        assert matrix[1][1] == 1.0
        # Correlação perfeita
        assert matrix[0][1] == pytest.approx(1.0, abs=1e-9)
        assert matrix[1][0] == pytest.approx(1.0, abs=1e-9)

    def test_correlation_two_assets_perfect_negative(self, engine):
        """Dois ativos com retornos opostos = correlação -1.0."""
        returns_a = [0.01, -0.02, 0.03, -0.01, 0.02]
        returns_b = [-0.01, 0.02, -0.03, 0.01, -0.02]
        asset_map = {"A": returns_a, "B": returns_b}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is not None
        assert matrix[0][1] == pytest.approx(-1.0, rel=1e-9)

    def test_correlation_three_assets(self, engine):
        """Matriz 3x3 deve ser simétrica com diagonal 1.0."""
        r1 = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.00, 0.02, -0.02]
        r2 = [0.02, -0.01, 0.04, -0.02, 0.01, 0.02, -0.02, 0.01, 0.03, -0.01]
        r3 = [-0.01, 0.02, -0.03, 0.01, -0.02, -0.01, 0.01, 0.00, -0.02, 0.02]
        asset_map = {"X": r1, "Y": r2, "Z": r3}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is not None
        assert len(matrix) == 3
        assert all(len(row) == 3 for row in matrix)
        # Diagonal = 1.0
        for i in range(3):
            assert matrix[i][i] == 1.0
        # Simetria
        for i in range(3):
            for j in range(3):
                assert matrix[i][j] == pytest.approx(matrix[j][i], rel=1e-9)
        # Valores no intervalo [-1, 1] (com tolerância para floating point)
        for i in range(3):
            for j in range(3):
                assert -1.0 - 1e-12 <= matrix[i][j] <= 1.0 + 1e-12

    def test_correlation_single_asset(self, engine):
        """Apenas 1 ativo deve retornar None."""
        asset_map = {"BTC": [0.01, -0.02, 0.03, -0.01, 0.02]}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is None

    def test_correlation_empty_map(self, engine):
        """Mapa vazio deve retornar None."""
        matrix = engine._compute_correlation_matrix({})
        assert matrix is None

    def test_correlation_insufficient_data(self, engine):
        """Menos de 5 pontos deve retornar None."""
        asset_map = {"A": [0.01, 0.02], "B": [0.01, 0.02]}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is None

    def test_correlation_unequal_lengths(self, engine):
        """Comprimentos diferentes: usa o menor (min_len)."""
        r1 = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.00, 0.02, -0.02]
        r2 = [0.02, -0.01, 0.04, -0.02, 0.01]  # apenas 5
        asset_map = {"A": r1, "B": r2}
        matrix = engine._compute_correlation_matrix(asset_map)
        assert matrix is not None
        # Deve funcionar com min_len=5
        assert len(matrix) == 2


# ---------------------------------------------------------------------------
# Testes: Pearson Correlation (estático)
# ---------------------------------------------------------------------------

class TestPearsonCorrelation:
    """Testa _pearson_correlation."""

    def test_perfect_positive(self, engine):
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [2.0, 4.0, 6.0, 8.0, 10.0]
        corr = engine._pearson_correlation(x, y)
        assert corr == pytest.approx(1.0, rel=1e-9)

    def test_perfect_negative(self, engine):
        x = [1.0, 2.0, 3.0, 4.0, 5.0]
        y = [5.0, 4.0, 3.0, 2.0, 1.0]
        corr = engine._pearson_correlation(x, y)
        assert corr == pytest.approx(-1.0, rel=1e-9)

    def test_no_correlation(self, engine):
        """Dois vetores ortogonais devem ter correlação ~0."""
        x = [1.0, 0.0, -1.0, 0.0, 1.0]
        y = [0.0, 1.0, 0.0, -1.0, 0.0]
        corr = engine._pearson_correlation(x, y)
        assert abs(corr) < 0.01

    def test_constant_vector(self, engine):
        """Vetor constante deve retornar 0 (std=0)."""
        x = [5.0, 5.0, 5.0, 5.0, 5.0]
        y = [1.0, 2.0, 3.0, 4.0, 5.0]
        corr = engine._pearson_correlation(x, y)
        assert corr == 0.0

    def test_single_element(self, engine):
        """Apenas 1 elemento deve retornar 0."""
        corr = engine._pearson_correlation([1.0], [2.0])
        assert corr == 0.0


# ---------------------------------------------------------------------------
# Testes: Stress Testing
# ---------------------------------------------------------------------------

class TestStressTesting:
    """Testa _compute_stress_test."""

    def test_stress_normal_volatility(self, engine):
        """Volatilidade normal (1%) deve retornar perda proporcional."""
        loss = engine._compute_stress_test(0.01)
        # Pior cenário = black_swan (-0.50), vol_multiplier = 0.01/0.01 = 1.0
        # loss = abs(-0.50) * 1.0 = 0.50
        assert loss == pytest.approx(0.50, rel=1e-9)

    def test_stress_high_volatility(self, engine):
        """Volatilidade alta (3%) deve agravar o cenário."""
        loss = engine._compute_stress_test(0.03)
        # vol_multiplier = 0.03/0.01 = 3.0
        # loss = 0.50 * 3.0 = 1.50, capped at 0.80
        assert loss == 0.80

    def test_stress_low_volatility(self, engine):
        """Volatilidade baixa (0.5%) deve reduzir o cenário."""
        loss = engine._compute_stress_test(0.005)
        # vol_multiplier = 0.005/0.01 = 0.5
        # loss = 0.50 * 0.5 = 0.25
        assert loss == pytest.approx(0.25, rel=1e-9)

    def test_stress_zero_volatility(self, engine):
        """Volatilidade zero deve usar fallback 0.01."""
        loss = engine._compute_stress_test(0.0)
        assert loss == pytest.approx(0.50, rel=1e-9)

    def test_stress_negative_volatility(self, engine):
        """Volatilidade negativa deve usar fallback 0.01."""
        loss = engine._compute_stress_test(-0.05)
        assert loss == pytest.approx(0.50, rel=1e-9)

    def test_stress_capped_at_80_percent(self, engine):
        """Perda nunca deve exceder 80%."""
        loss = engine._compute_stress_test(0.10)  # 10% vol diária
        assert loss <= 0.80


# ---------------------------------------------------------------------------
# Testes: assess() — Integração
# ---------------------------------------------------------------------------

class TestAssessIntegration:
    """Testa o método assess() completo."""

    def test_assess_basic(self, engine, mock_context, mock_evidence_bundle):
        """Chamada básica sem parâmetros novos (compatibilidade retroativa)."""
        result = engine.assess(mock_context, mock_evidence_bundle)
        assert isinstance(result, RiskAssessment)
        # Campos originais preenchidos
        assert result.suggested_stop > 0
        assert result.suggested_take_profit > 0
        assert result.risk_reward_ratio > 0
        assert result.expected_drawdown >= 0
        assert result.expected_volatility >= 0
        assert result.trade_quality >= 0
        assert result.institutional_risk_score >= 0
        # Campos Bloco 4 — VaR/CVaR zerados sem historical_returns
        assert result.var_95 == 0.0
        assert result.var_99 == 0.0
        assert result.cvar_95 == 0.0
        # Kelly calculado com defaults (win_rate=0.55, payoff=1.5) → 0.25
        assert result.kelly_fraction == pytest.approx(0.25)
        assert result.kelly_half == pytest.approx(0.125)
        assert result.kelly_quarter == pytest.approx(0.0625)
        assert result.correlation_matrix is None
        assert result.stress_test_loss >= 0.0

    def test_assess_with_historical_returns(
        self, engine, mock_context, mock_evidence_bundle, sample_returns_normal
    ):
        """Com retornos históricos, VaR/CVaR devem ser calculados."""
        result = engine.assess(
            mock_context,
            mock_evidence_bundle,
            historical_returns=sample_returns_normal,
        )
        assert result.var_95 > 0.0
        assert result.var_99 > 0.0
        assert result.cvar_95 > 0.0

    def test_assess_with_kelly_params(
        self, engine, mock_context, mock_evidence_bundle
    ):
        """Com win_rate e payoff, Kelly deve ser calculado."""
        result = engine.assess(
            mock_context,
            mock_evidence_bundle,
            win_rate=0.60,
            payoff_ratio=2.0,
        )
        assert result.kelly_fraction > 0.0
        assert result.kelly_half == result.kelly_fraction / 2.0
        assert result.kelly_quarter == result.kelly_fraction / 4.0

    def test_assess_with_correlation(
        self, engine, mock_context, mock_evidence_bundle
    ):
        """Com asset_returns_map, correlação deve ser calculada."""
        r1 = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.00, 0.02, -0.02]
        r2 = [0.02, -0.01, 0.04, -0.02, 0.01, 0.02, -0.02, 0.01, 0.03, -0.01]
        result = engine.assess(
            mock_context,
            mock_evidence_bundle,
            asset_returns_map={"BTC": r1, "ETH": r2},
        )
        assert result.correlation_matrix is not None
        assert len(result.correlation_matrix) == 2

    def test_assess_full(
        self, engine, mock_context, mock_evidence_bundle, sample_returns_normal
    ):
        """Todos os parâmetros novos fornecidos simultaneamente."""
        r1 = [0.01, -0.02, 0.03, -0.01, 0.02, 0.01, -0.01, 0.00, 0.02, -0.02]
        r2 = [0.02, -0.01, 0.04, -0.02, 0.01, 0.02, -0.02, 0.01, 0.03, -0.01]
        result = engine.assess(
            mock_context,
            mock_evidence_bundle,
            historical_returns=sample_returns_normal,
            win_rate=0.55,
            payoff_ratio=1.8,
            asset_returns_map={"BTC": r1, "ETH": r2},
        )
        assert result.var_95 > 0.0
        assert result.var_99 > 0.0
        assert result.cvar_95 > 0.0
        assert result.kelly_fraction > 0.0
        assert result.correlation_matrix is not None
        assert result.stress_test_loss > 0.0

    def test_assess_bearish_trend(self, engine, mock_context, mock_evidence_bundle):
        """Tendência BEARISH deve inverter invalidação."""
        bearish_structure = MarketStructure(trend="BEARISH")
        bearish_smart_money = SmartMoneyAnalysis(structure=bearish_structure)
        bearish_context = MagicMock(spec=MarketContext)
        bearish_context.market = mock_context.market
        bearish_context.smart_money = bearish_smart_money
        result = engine.assess(bearish_context, mock_evidence_bundle)
        # Invalidação deve ser acima do preço (1% acima)
        assert result.invalidation_point > bearish_context.market.close

    def test_assess_risk_assessment_is_frozen(self, engine, mock_context, mock_evidence_bundle):
        """RiskAssessment deve ser imutável (frozen dataclass)."""
        result = engine.assess(mock_context, mock_evidence_bundle)
        with pytest.raises(Exception):
            result.var_95 = 0.99  # type: ignore


# ---------------------------------------------------------------------------
# Testes: Casos de Borda
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """Casos de borda e robustez."""

    def test_assess_zero_atr(self, engine, mock_context, mock_evidence_bundle):
        """ATR zero não deve causar divisão por zero."""
        zero_atr_market = MarketData(
            symbol="EURUSD", timeframe="H1", close=1.1000,
            ema9=1.0990, ema21=1.0980, ema50=1.0950,
            rsi=55.0, atr=0.0, adx=25.0,
            macd=0.0002, macd_signal=0.0001,
            bollinger_upper=1.1050, bollinger_lower=1.0950,
            volume=10000.0,
        )
        zero_atr_context = MagicMock(spec=MarketContext)
        zero_atr_context.market = zero_atr_market
        zero_atr_context.smart_money = mock_context.smart_money
        result = engine.assess(zero_atr_context, mock_evidence_bundle)
        # ATR=0 → volatilidade = 0 (atr/price*100 = 0)
        assert result.expected_volatility == 0.0
        # RR não é afetado pelo ATR (usa 1% do preço como stop)
        assert result.risk_reward_ratio > 0

    def test_assess_zero_price(self, engine, mock_context, mock_evidence_bundle):
        """Preço zero não deve crashar."""
        zero_price_market = MarketData(
            symbol="EURUSD", timeframe="H1", close=0.0,
            ema9=1.0990, ema21=1.0980, ema50=1.0950,
            rsi=55.0, atr=0.0015, adx=25.0,
            macd=0.0002, macd_signal=0.0001,
            bollinger_upper=1.1050, bollinger_lower=1.0950,
            volume=10000.0,
        )
        zero_price_context = MagicMock(spec=MarketContext)
        zero_price_context.market = zero_price_market
        zero_price_context.smart_money = mock_context.smart_money
        result = engine.assess(zero_price_context, mock_evidence_bundle)
        assert result.expected_volatility == 0.0

    def test_assess_no_volatility_evidence(self, engine, mock_context):
        """Bundle sem evidência de volatilidade deve usar fallback."""
        trend_evidence = Evidence(
            engine_name="Trend",
            evidence_name="trend_only",
            direction="BULLISH",
            strength=5.0,
            confidence=80.0,
            description="Only trend evidence, no volatility",
            weight=1.0,
        )
        bundle = MarketEvidenceBundle(
            evidences=(trend_evidence,),
            timestamp="2025-01-01T00:00:00",
            asset="EURUSD",
            timeframe="H1",
        )
        result = engine.assess(mock_context, bundle)
        assert result.expected_drawdown == 5.0  # fallback

    def test_assess_empty_evidence_bundle(self, engine, mock_context):
        """Bundle vazio não deve crashar."""
        bundle = MagicMock(spec=MarketEvidenceBundle)
        bundle.evidences = []
        result = engine.assess(mock_context, bundle)
        assert isinstance(result, RiskAssessment)
        assert result.trade_quality == 50.0  # fallback

    def test_kelly_extreme_values(self, engine):
        """Valores extremos de win_rate e payoff."""
        # win_rate = 0, payoff = 0.01
        k_full, _, _ = engine._compute_kelly(win_rate=0.0, payoff_ratio=0.01)
        assert k_full == 0.0

        # win_rate = 1.0, payoff = 100
        k_full, _, _ = engine._compute_kelly(win_rate=1.0, payoff_ratio=100.0)
        assert k_full == 0.25  # capped

    def test_pearson_identical_vectors(self, engine):
        """Vetores idênticos devem ter correlação 1.0."""
        x = [0.01, -0.02, 0.03, -0.01, 0.02]
        corr = engine._pearson_correlation(x, x)
        assert corr == pytest.approx(1.0, rel=1e-9)