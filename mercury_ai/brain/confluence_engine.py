from mercury_ai.models.recommendation import Recommendation


class ConfluenceEngine:
    """
    Responsável por calcular o Mercury Score
    com base nas evidências encontradas.
    """

    def analyze(self, market: dict) -> Recommendation:

        score = 0

        evidences = []

        # Tendência
        if market.get("trend") == "UP":
            score += 20
            evidences.append("Tendência de alta confirmada")

        elif market.get("trend") == "DOWN":
            score += 20
            evidences.append("Tendência de baixa confirmada")

        # RSI

        rsi = market.get("rsi", 50)

        if rsi < 30:
            score += 10
            evidences.append("RSI em sobrevenda")

        elif rsi > 70:
            score += 10
            evidences.append("RSI em sobrecompra")

        # Bollinger

        bollinger = market.get("bollinger")

        if bollinger == "LOW":
            score += 10
            evidences.append("Preço na banda inferior de Bollinger")

        elif bollinger == "HIGH":
            score += 10
            evidences.append("Preço na banda superior de Bollinger")

        # Liquidez

        if market.get("high_liquidity"):
            score += 5
            evidences.append("Alta liquidez")

        # Contexto

        if market.get("session") in ["LONDON", "NEW_YORK"]:
            score += 10
            evidences.append("Sessão forte")

        confidence = min(score, 100)

        if score >= 70:
            decision = "BUY" if market.get("trend") == "UP" else "SELL"
        else:
            decision = "WAIT"

        explanation = (
            f"Foram encontradas {len(evidences)} evidências "
            f"que resultaram em um Mercury Score de {score}."
        )

        return Recommendation(
            decision=decision,
            confidence=confidence,
            score=score,
            strategy="Confluence",
            evidences=evidences,
            explanation=explanation
        )