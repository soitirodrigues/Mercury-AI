from mercury_ai.models.market_state import MarketState


class ContextEngine:
    """
    Responsável por entender o contexto atual do mercado.
    Não gera sinais.
    Apenas descreve o estado do mercado.
    """

    def analyze(self, market: dict) -> MarketState:

        trend = market.get("trend", "SIDEWAYS")

        volatility = market.get("volatility", "NORMAL")

        session = market.get("session", "UNKNOWN")

        high_liquidity = market.get("high_liquidity", False)

        support = market.get("support")

        resistance = market.get("resistance")

        timeframe = market.get("timeframe", "M5")

        asset = market.get("symbol", "UNKNOWN")

        return MarketState(
            asset=asset,
            trend=trend,
            volatility=volatility,
            session=session,
            high_liquidity=high_liquidity,
            support=support,
            resistance=resistance,
            timeframe=timeframe
        )