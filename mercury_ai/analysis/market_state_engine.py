from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_state import MarketState
from mercury_ai.models.market_state_enum import MarketStateEnum
from mercury_ai.models.session_analysis import SessionAnalysis


class MarketStateEngine:
    """
    Motor responsável por identificar o estado estrutural
    e operacional do mercado.
    """

    def analyze(
        self,
        market: MarketData,
        session: SessionAnalysis
    ) -> MarketState:

        atr = market.atr or 0.0
        adx = market.adx or 0.0
        ema9 = market.ema9 or 1.0

        explanation = []

        # ----------------------------------
        # Volatilidade
        # ----------------------------------

        if atr >= ema9 * 0.020:

            state = MarketStateEnum.HIGH_VOLATILITY
            explanation.append("ATR elevado")

        elif atr <= ema9 * 0.005:

            state = MarketStateEnum.LOW_VOLATILITY
            explanation.append("ATR reduzido")

        # ----------------------------------
        # Estrutura
        # ----------------------------------

        elif adx >= 30:

            state = MarketStateEnum.TRENDING
            explanation.append("Mercado em tendência")

        elif adx <= 20:

            state = MarketStateEnum.RANGING
            explanation.append("Mercado lateral")

        else:

            state = MarketStateEnum.UNKNOWN
            explanation.append("Estado indefinido")

        # ----------------------------------
        # Sessão Institucional
        # ----------------------------------

        if session:

            explanation.append(
                f"Sessão: {session.session}"
            )

            if session.overlap:

                explanation.append(
                    "Overlap institucional"
                )

            if session.liquidity_score >= 90:

                explanation.append(
                    "Alta liquidez"
                )

        return MarketState(
            state=state,
            explanation=" | ".join(explanation)
        )