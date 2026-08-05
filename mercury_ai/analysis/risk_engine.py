"""
Risk Engine — Bloco 4 Enhanced.

Novas capacidades:
  - VaR paramétrico (95%, 99%)
  - CVaR / Expected Shortfall (95%)
  - Kelly Criterion (full, half, quarter)
  - Matriz de correlação entre ativos
  - Stress testing com cenários extremos
"""

import math
from typing import Dict, List, Optional, Tuple

from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine
from mercury_ai.config.risk import (
    VAR_CONFIDENCE_95,
    VAR_CONFIDENCE_99,
    KELLY_DEFAULT_WIN_RATE,
    KELLY_DEFAULT_PAYOFF,
    KELLY_MAX_FRACTION,
    STRESS_SCENARIOS,
)


class RiskEngine:
    """
    Motor central e único para análise de risco institucional.

    Bloco 4: Adiciona VaR, CVaR, Kelly Criterion, correlação e stress testing.
    """

    def __init__(self):
        self.quality = EvidenceQualityEngine()

    # ------------------------------------------------------------------
    # API principal
    # ------------------------------------------------------------------
    def assess(
        self,
        context: MarketContext,
        evidence_bundle: MarketEvidenceBundle,
        historical_returns: Optional[List[float]] = None,
        win_rate: Optional[float] = None,
        payoff_ratio: Optional[float] = None,
        asset_returns_map: Optional[Dict[str, List[float]]] = None,
    ) -> RiskAssessment:
        """
        Avaliação completa de risco.

        Args:
            context: Contexto de mercado atual
            evidence_bundle: Bundle de evidências
            historical_returns: Lista de retornos históricos para VaR/CVaR
            win_rate: Win rate histórica para Kelly (0.0-1.0)
            payoff_ratio: Payoff ratio histórico para Kelly
            asset_returns_map: Mapa símbolo->retornos para correlação
        """
        # 1. Métricas determinísticas (originais)
        atr = context.market.atr
        price = context.market.close

        invalidation = (
            price * 0.99
            if context.smart_money.structure.trend == "BULLISH"
            else price * 1.01
        )

        stop = invalidation
        reward_dist = (price - stop) * 2.0
        tp = price + reward_dist
        rr = reward_dist / abs(price - stop) if abs(price - stop) > 0 else 0.0

        drawdown = next(
            (e.strength for e in evidence_bundle.evidences if e.engine_name == "VolatilityEngine"),
            5.0,
        )
        volatility = atr / price * 100 if price > 0 else 0.0

        quality_res = self.quality.evaluate(list(evidence_bundle.evidences))
        quality_score = (
            sum(e.quality_score for e in quality_res) / len(quality_res)
            if quality_res
            else 50.0
        )

        quality_component = quality_score * 0.6
        rr_component = min(rr * 10, 40)
        risk_score = 100 - (quality_component + rr_component)

        # 2. Bloco 4: VaR & CVaR
        var_95, var_99, cvar_95 = self._compute_var_cvar(historical_returns or [])

        # 3. Bloco 4: Kelly Criterion
        kelly_full, kelly_half, kelly_quarter = self._compute_kelly(
            win_rate=win_rate,
            payoff_ratio=payoff_ratio,
        )

        # 4. Bloco 4: Correlation Matrix
        corr_matrix = self._compute_correlation_matrix(asset_returns_map or {})

        # 5. Bloco 4: Stress Testing
        stress_loss = self._compute_stress_test(volatility / 100.0 if volatility > 0 else 0.01)
        return RiskAssessment(
            # Originais
            suggested_stop=float(stop),
            suggested_take_profit=float(tp),
            risk_reward_ratio=float(rr),
            expected_drawdown=float(drawdown),
            expected_volatility=float(volatility),
            trade_quality=float(quality_score),
            max_exposure=0.02,
            invalidation_point=float(invalidation),
            institutional_risk_score=float(risk_score),
            # Bloco 4
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            kelly_fraction=kelly_full,
            kelly_half=kelly_half,
            kelly_quarter=kelly_quarter,
            correlation_matrix=corr_matrix,
            stress_test_loss=stress_loss,
        )

    # ------------------------------------------------------------------
    # API simplificada para integração com pipelines de backtest
    # ------------------------------------------------------------------
    def assess_simple(
        self,
        symbol: str = "UNKNOWN",
        price: float = 0.0,
        atr: float = 0.0,
        trend: str = "NEUTRAL",
        evidence_bundle=None,
        historical_returns: Optional[List[float]] = None,
    ) -> RiskAssessment:
        """
        Avaliação de risco com parâmetros planos (para pipelines de backtest).

        Constrói internamente MarketContext e MarketEvidenceBundle mínimos
        e delega para o método assess principal.
        """
        from mercury_ai.models.market_data import MarketData
        from mercury_ai.models.market_structure import MarketStructure
        from mercury_ai.models.smart_money import SmartMoneyAnalysis
        from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
        from mercury_ai.models.evidence import Evidence

        market_data = MarketData(
            symbol=symbol,
            timeframe="H1",
            close=price,
            ema9=price,
            ema21=price,
            ema50=price,
            rsi=50.0,
            atr=atr,
            adx=25.0,
            macd=0.0,
            macd_signal=0.0,
            bollinger_upper=price * 1.02,
            bollinger_lower=price * 0.98,
            volume=10000.0,
        )

        structure = MarketStructure(trend=trend)
        smart_money = SmartMoneyAnalysis(structure=structure)

        # Construímos um MarketContext real com valores padrão para campos
        # que o RiskEngine.assess() não acessa diretamente
        from mercury_ai.models.price_action import PriceActionAnalysis
        from mercury_ai.models.support_resistance import SupportResistanceAnalysis
        from mercury_ai.models.liquidity_profile import LiquidityProfile
        from mercury_ai.models.market_state import MarketState
        from mercury_ai.models.market_state_enum import MarketStateEnum
        from mercury_ai.models.market_regime import MarketRegime
        from mercury_ai.models.market_regime_enum import MarketRegimeEnum
        from mercury_ai.models.mtf_consensus import MTFConsensus
        from mercury_ai.models.risk_assessment import RiskAssessment

        ctx = MarketContext(
            market=market_data,
            trend=[],
            price_action=PriceActionAnalysis(
                trend_structure="NEUTRAL",
                last_event="NONE",
                confidence=50,
                explanation=[],
            ),
            support_resistance=SupportResistanceAnalysis(
                support=price * 0.99,
                resistance=price * 1.01,
                distance_support=price * 0.01,
                distance_resistance=price * 0.01,
                explanation=[],
            ),
            smart_money=smart_money,
            liquidity=LiquidityProfile(),
            market_state=MarketState(
                state=MarketStateEnum.RANGING,
                explanation="Default state for simple assessment",
            ),
            market_regime=MarketRegime(
                regime=MarketRegimeEnum.UNKNOWN,
                confidence=50.0,
                supporting_evidences=[],
            ),
            mtf_consensus=MTFConsensus(
                global_bias="NEUTRAL",
                local_bias="NEUTRAL",
                conflict_detected=False,
                alignment_score=50.0,
            ),
            risk_assessment=RiskAssessment(
                suggested_stop=price * 0.99,
                suggested_take_profit=price * 1.02,
                risk_reward_ratio=2.0,
                expected_drawdown=5.0,
                expected_volatility=atr / price * 100 if price > 0 else 0.0,
                trade_quality=50.0,
                max_exposure=0.02,
                invalidation_point=price * 0.99,
                institutional_risk_score=50.0,
                var_95=0.0,
                var_99=0.0,
                cvar_95=0.0,
                kelly_fraction=0.0,
                kelly_half=0.0,
                kelly_quarter=0.0,
                correlation_matrix={},
                stress_test_loss=0.0,
            ),
        )

        if evidence_bundle is None:
            vol_evidence = Evidence(
                engine_name="VolatilityEngine",
                evidence_name="volatility_check",
                direction="NEUTRAL",
                strength=3.0,
                confidence=80.0,
                description="ATR-based volatility assessment",
                weight=0.3,
            )
            evidence_bundle = MarketEvidenceBundle(
                evidences=(vol_evidence,),
                timestamp="2025-01-01T00:00:00",
                asset=symbol,
                timeframe="H1",
            )

        return self.assess(ctx, evidence_bundle, historical_returns=historical_returns)

    # ------------------------------------------------------------------
    # Bloco 4.1: Value at Risk (VaR) & Conditional VaR (CVaR)
    # ------------------------------------------------------------------
    def _compute_var_cvar(
        self, returns: List[float]
    ) -> Tuple[float, float, float]:
        """
        Calcula VaR paramétrico (95%, 99%) e CVaR histórico (95%).

        Args:
            returns: Lista de retornos percentuais (ex: [0.01, -0.02, ...])

        Returns:
            (var_95, var_99, cvar_95) — todos como fração (ex: 0.02 = 2% de perda)
        """
        if len(returns) < 5:
            return 0.0, 0.0, 0.0

        n = len(returns)
        mean = sum(returns) / n
        variance = sum((r - mean) ** 2 for r in returns) / (n - 1) if n > 1 else 0.0
        std = math.sqrt(variance) if variance > 0 else 0.0

        if std == 0.0:
            return 0.0, 0.0, 0.0

        # VaR paramétrico (assume distribuição normal)
        var_95 = -(mean - VAR_CONFIDENCE_95 * std)
        var_99 = -(mean - VAR_CONFIDENCE_99 * std)

        # CVaR histórico: média dos retornos abaixo do VaR 95%
        var_threshold = mean - VAR_CONFIDENCE_95 * std
        tail_losses = [r for r in returns if r <= var_threshold]
        if tail_losses:
            cvar_95 = -(sum(tail_losses) / len(tail_losses))
        else:
            cvar_95 = var_95  # fallback: usa VaR paramétrico

        # Garantir que valores negativos (ganho) não sejam retornados como "risco"
        return max(0.0, float(var_95)), max(0.0, float(var_99)), max(0.0, float(cvar_95))

    # ------------------------------------------------------------------
    # Bloco 4.2: Kelly Criterion
    # ------------------------------------------------------------------
    def _compute_kelly(
        self,
        win_rate: Optional[float] = None,
        payoff_ratio: Optional[float] = None,
    ) -> Tuple[float, float, float]:
        """
        Calcula a fração ótima de Kelly para position sizing.

        Fórmula: f* = (p * b - (1-p)) / b
        onde p = win_rate, b = payoff_ratio

        Args:
            win_rate: Probabilidade de ganho (0.0-1.0)
            payoff_ratio: Razão ganho/perda média

        Returns:
            (kelly_full, kelly_half, kelly_quarter)
        """
        p = win_rate if win_rate is not None else KELLY_DEFAULT_WIN_RATE
        b = payoff_ratio if payoff_ratio is not None else KELLY_DEFAULT_PAYOFF

        # Validar inputs
        p = max(0.0, min(1.0, p))
        b = max(0.01, b)

        # Kelly formula: f* = (p*b - (1-p)) / b
        if b > 0:
            kelly = (p * b - (1.0 - p)) / b
        else:
            kelly = 0.0

        # Cap no máximo permitido
        kelly = max(0.0, min(KELLY_MAX_FRACTION, kelly))

        return (
            float(kelly),
            float(kelly / 2.0),
            float(kelly / 4.0),
        )

    # ------------------------------------------------------------------
    # Bloco 4.3: Correlation Matrix
    # ------------------------------------------------------------------
    def _compute_correlation_matrix(
        self, asset_returns_map: Dict[str, List[float]]
    ) -> Optional[Tuple[Tuple[float, ...], ...]]:
        """
        Calcula matriz de correlação de Pearson entre ativos.

        Args:
            asset_returns_map: {symbol: [returns]}

        Returns:
            Matriz de correlação como tuple de tuples, ou None se < 2 ativos
        """
        symbols = list(asset_returns_map.keys())
        if len(symbols) < 2:
            return None

        # Validar que todos têm o mesmo comprimento
        min_len = min(len(r) for r in asset_returns_map.values())
        if min_len < 5:
            return None

        n = len(symbols)
        matrix: List[List[float]] = [[1.0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                r_i = asset_returns_map[symbols[i]][:min_len]
                r_j = asset_returns_map[symbols[j]][:min_len]
                corr = self._pearson_correlation(r_i, r_j)
                matrix[i][j] = corr
                matrix[j][i] = corr

        # Converter para tuple imutável
        return tuple(tuple(row) for row in matrix)

    @staticmethod
    def _pearson_correlation(x: List[float], y: List[float]) -> float:
        """Coeficiente de correlação de Pearson."""
        n = len(x)
        if n < 2:
            return 0.0

        mean_x = sum(x) / n
        mean_y = sum(y) / n

        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

        if std_x == 0.0 or std_y == 0.0:
            return 0.0

        return float(cov / (std_x * std_y))

    # ------------------------------------------------------------------
    # Bloco 4.4: Stress Testing
    # ------------------------------------------------------------------
    def _compute_stress_test(self, daily_volatility: float) -> float:
        """
        Executa stress testing com cenários extremos predefinidos.

        Retorna a perda estimada no pior cenário, ponderada pela
        volatilidade atual do ativo.

        Args:
            daily_volatility: Volatilidade diária como fração (ex: 0.01 = 1%)

        Returns:
            Perda estimada no pior cenário como fração positiva
        """
        if daily_volatility <= 0:
            daily_volatility = 0.01

        # Pior cenário entre os definidos
        worst_scenario = min(STRESS_SCENARIOS.values())  # mais negativo

        # Ajusta o cenário pela volatilidade atual:
        # Se vol atual > vol implícita no cenário, agrava o cenário
        base_vol = 0.01  # 1% diário = volatilidade "normal"
        vol_multiplier = daily_volatility / base_vol

        stress_loss = abs(worst_scenario) * vol_multiplier

        # Cap em 80% (perda máxima concebível)
        return float(min(stress_loss, 0.80))
