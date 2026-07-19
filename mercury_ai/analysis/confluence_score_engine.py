from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.confluence_score import ConfluenceScore
from mercury_ai.models.market_state_enum import MarketStateEnum
from mercury_ai.analysis.evidence_query import EvidenceQuery
from mercury_ai.config.institutional_weights import INSTITUTIONAL_WEIGHTS
from mercury_ai.analysis.confluence_helpers import has_conflict, clamp_score


class ConfluenceScoreEngine:
    """
    Motor central para cálculos determinísticos de confluência, score, e alinhamento.

    Utiliza os pesos institucionais canônicos definidos em
    mercury_ai.config.institutional_weights (single source of truth).
    """

    def calculate(self, context: MarketContext) -> ConfluenceScore:
        bullish = 0.0
        bearish = 0.0
        conflicts = 0

        W = INSTITUTIONAL_WEIGHTS  # alias local para legibilidade

        # Trend contribuição
        is_uptrend = EvidenceQuery.is_uptrend(context.trend)
        is_downtrend = EvidenceQuery.is_downtrend(context.trend)

        if is_uptrend:
            bullish += W["trend"]
        elif is_downtrend:
            bearish += W["trend"]

        # Smart Money contribuição
        if context.smart_money.structure.trend == "BULLISH":
            bullish += W["smart_money"]
        elif context.smart_money.structure.trend == "BEARISH":
            bearish += W["smart_money"]

        # Market Structure contribuição (Price Action)
        if context.price_action.trend_structure == "BULLISH":
            bullish += W["market_structure"]
        elif context.price_action.trend_structure == "BEARISH":
            bearish += W["market_structure"]

        # Liquidity contribuição
        if context.liquidity.liquidity_sweep:
            if context.smart_money.structure.trend == "BULLISH":
                bullish += W["liquidity"]
            elif context.smart_money.structure.trend == "BEARISH":
                bearish += W["liquidity"]

        # Support/Resistance contribuição (proximidade)
        if context.support_resistance.distance_support < context.support_resistance.distance_resistance:
            bullish += W["support_resistance"]
        elif context.support_resistance.distance_resistance < context.support_resistance.distance_support:
            bearish += W["support_resistance"]

        # Volatility contribuição (ATR relativo ao preço)
        atr_pct = context.market.atr / context.market.close if context.market.close > 0 else 0.0
        if atr_pct < 0.02:
            if is_uptrend:
                bullish += W["volatility"]
            elif is_downtrend:
                bearish += W["volatility"]

        # Market Condition contribuição
        if context.market_state.state == MarketStateEnum.TRENDING:
            if is_uptrend:
                bullish += W["market_condition"]
            elif is_downtrend:
                bearish += W["market_condition"]

        # Candlestick contribuição (último evento de price action)
        if "BULLISH" in context.price_action.last_event.upper():
            bullish += W["candlestick"]
        elif "BEARISH" in context.price_action.last_event.upper():
            bearish += W["candlestick"]

        # Detecção de conflitos
        if has_conflict(bullish, bearish):
            conflicts = 1

        # Cálculos determinísticos
        total_weight = sum(W.values())
        confluence_score = (max(bullish, bearish) / total_weight) * 100
        conflict_penalty = (conflicts * 20.0)
        clarity_score = clamp_score(confluence_score - conflict_penalty, floor=0.0, ceiling=100.0)

        return ConfluenceScore(
            confluence_score=confluence_score,
            clarity_score=clarity_score,
            bullish_score=bullish,
            bearish_score=bearish,
            conflict_penalty=conflict_penalty
        )
