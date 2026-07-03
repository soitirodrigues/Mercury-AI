from mercury_ai.models.confluence import ConfluenceResult
from mercury_ai.models.market_context import MarketContext


class ConfluenceEngine:

    def analyze(self, context: MarketContext):

        score = 0
        evidences = []

        # Tendência
        if context.trend.trend == "STRONG_UP":
            score += 40
            evidences.append("Tendência forte de alta")

        elif context.trend.trend == "UP":
            score += 25
            evidences.append("Tendência de alta")

        elif context.trend.trend == "STRONG_DOWN":
            score -= 40
            evidences.append("Tendência forte de baixa")

        elif context.trend.trend == "DOWN":
            score -= 25
            evidences.append("Tendência de baixa")

        # Price Action
        if context.price_action.trend_structure == "BULLISH":
            score += 25
            evidences.append("Estrutura de alta")

        elif context.price_action.trend_structure == "BEARISH":
            score -= 25
            evidences.append("Estrutura de baixa")

        # Decisão
        if score >= 40:
            decision = "BUY"

        elif score <= -40:
            decision = "SELL"

        else:
            decision = "WAIT"

        confidence = min(abs(score), 100)

        return ConfluenceResult(
            score=score,
            confidence=confidence,
            decision=decision,
            evidences=evidences
        )