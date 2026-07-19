from dataclasses import dataclass

@dataclass
class InstitutionalContext:

    market_state: str

    session: str

    volatility: float

    liquidity: float

    institutional_bias: str

    confidence: float

    explanation: str


class InstitutionalContextBuilder:

    """
    Constrói o contexto institucional completo do mercado.
    """

    def build(
        self,
        market_state,
        session_analysis,
        volatility,
        liquidity,
        trend,
        smart_money,
    ) -> InstitutionalContext:

        bias = self._calculate_bias(
            trend,
            smart_money,
        )

        confidence = self._calculate_confidence(
            volatility,
            liquidity,
            session_analysis,
        )

        explanation = self._build_text(
            market_state,
            session_analysis,
            bias,
        )

        return InstitutionalContext(

            market_state=market_state.state.value,

            session=session_analysis.session,

            volatility=volatility.score,

            liquidity=liquidity.score,

            institutional_bias=bias,

            confidence=confidence,

            explanation=explanation,

        )

    def _calculate_bias(
        self,
        trend,
        smart_money,
    ):

        bullish = 0

        bearish = 0

        if trend.direction == "BULLISH":
            bullish += 1

        elif trend.direction == "BEARISH":
            bearish += 1

        if smart_money.direction == "BULLISH":
            bullish += 1

        elif smart_money.direction == "BEARISH":
            bearish += 1

        if bullish > bearish:
            return "BULLISH"

        if bearish > bullish:
            return "BEARISH"

        return "NEUTRAL"

    def _calculate_confidence(
        self,
        volatility,
        liquidity,
        session,
    ):

        score = 50

        score += liquidity.score * 0.20

        score += volatility.score * 0.20

        score += session.quality * 0.20

        return min(score,100)

    def _build_text(
        self,
        state,
        session,
        bias,
    ):

        return (
            f"State: {state.state.value} | "
            f"Session: {session.session} | "
            f"Bias: {bias}"
        )