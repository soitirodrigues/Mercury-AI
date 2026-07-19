from typing import List

from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_regime_enum import MarketRegimeEnum
from mercury_ai.models.trade_filter_result import TradeFilterResult


class InstitutionalTradeFilterEngine:
    """
    Motor institucional de filtragem de trades.

    Avalia se um trade deve ser permitido com base em penalidades
    acumuladas por fatores de risco institucional.

    Retorna um TradeFilterResult imutável em vez da tupla ambígua
    (bool, list[str], float, str) usada anteriormente.
    """

    def evaluate(
        self,
        context: MarketContext,
        evidence_bundle: MarketEvidenceBundle,
    ) -> TradeFilterResult:
        """
        Avalia se um trade deve ser permitido.

        Em vez de bloquear imediatamente qualquer condição,
        cada fator adiciona uma penalidade.

        Apenas quando a penalidade total ultrapassa o limite,
        o trade será bloqueado.
        """

        reasons: List[str] = []
        penalty: float = 0.0

        ########################################################
        # MARKET REGIME
        ########################################################

        if (
            context.market_regime is not None
            and context.market_regime.regime == MarketRegimeEnum.COMPRESSION
        ):
            reasons.append("Compression Regime")
            penalty += 20.0

        elif (
            context.market_regime is not None
            and context.market_regime.regime == MarketRegimeEnum.DISTRIBUTION
        ):
            reasons.append("Distribution Regime")
            penalty += 8.0

        elif (
            context.market_regime is not None
            and context.market_regime.regime == MarketRegimeEnum.EXPANSION
        ):
            reasons.append("High Volatility Regime")
            penalty += 10.0

        elif (
            context.market_regime is not None
            and context.market_regime.regime == MarketRegimeEnum.CONSOLIDATION
        ):
            reasons.append("Low Liquidity Regime")
            penalty += 12.0

        ########################################################
        # CONFLUENCE
        ########################################################

        evidence_count = len(evidence_bundle.evidences)

        if evidence_count < 3:
            reasons.append("Insufficient Confluence")
            penalty += 35.0

        elif evidence_count == 3:
            penalty += 10.0

        ########################################################
        # ATR
        ########################################################

        atr = context.market.atr

        if atr <= 0:
            reasons.append("ATR unavailable")
            penalty += 30.0

        elif atr < 0.0001:
            reasons.append("Low ATR")
            penalty += 25.0

        ########################################################
        # QUALITY SCORE
        ########################################################

        quality_score = max(0.0, 100.0 - penalty)

        ########################################################
        # QUALITY LEVEL
        ########################################################

        if quality_score >= 90:
            quality_level = "A+"

        elif quality_score >= 80:
            quality_level = "A"

        elif quality_score >= 70:
            quality_level = "B"

        elif quality_score >= 60:
            quality_level = "C"

        else:
            quality_level = "D"

        ########################################################
        # DECISÃO
        ########################################################

        # Bloqueia somente quando o ambiente institucional
        # realmente é desfavorável.

        allowed = penalty >= 50.0
        allowed = not allowed

        return TradeFilterResult(
            allowed=allowed,
            reasons=tuple(reasons),
            quality_score=quality_score,
            quality_level=quality_level,
        )