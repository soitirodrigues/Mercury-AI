from dataclasses import dataclass

from mercury_ai.models.market_structure import MarketStructure


@dataclass
class CHOCHResult:

    detected: bool
    direction: str
    confidence: int
    explanation: list[str]


class CHOCHEngine:

    def analyze(self, market_structure: MarketStructure) -> CHOCHResult:

        detected = False
        direction = "NONE"
        confidence = 0
        explanation = []

        # -----------------------------
        # Possível reversão para BAIXA
        # -----------------------------

        if (
            market_structure.higher_high
            and market_structure.lower_low
        ):

            detected = True
            direction = "BEARISH"

            confidence = 80

            explanation.append(
                "CHOCH Bearish detectado."
            )

        # -----------------------------
        # Possível reversão para ALTA
        # -----------------------------

        elif (
            market_structure.lower_high
            and market_structure.higher_low
        ):

            detected = True
            direction = "BULLISH"

            confidence = 80

            explanation.append(
                "CHOCH Bullish detectado."
            )

        else:

            explanation.append(
                "Nenhum CHOCH identificado."
            )

        return CHOCHResult(
            detected=detected,
            direction=direction,
            confidence=confidence,
            explanation=explanation
        )