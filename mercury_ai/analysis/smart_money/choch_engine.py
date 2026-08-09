from dataclasses import dataclass
from typing import Tuple

from mercury_ai.models.market_structure import MarketStructure


@dataclass(frozen=True)
class CHOCHResult:

    detected: bool
    direction: str
    confidence: int
    explanation: Tuple[str, ...]


class CHOCHEngine:

    def analyze(self, market_structure: MarketStructure) -> CHOCHResult:

        detected = False
        direction = "NONE"
        confidence = 0
        explanation = []

        # -----------------------------
        # CHOCH Bearish — reversão para BAIXA
        # Market structure: lower_high AND lower_low
        # O preço falha em fazer HH e quebra o último LL
        # -----------------------------

        if (
            market_structure.lower_high
            and market_structure.lower_low
        ):

            detected = True
            direction = "BEARISH"

            confidence = 80

            explanation.append(
                "CHOCH Bearish detectado."
            )

        # -----------------------------
        # CHOCH Bullish — reversão para ALTA
        # Market structure: higher_high AND higher_low
        # O preço falha em fazer LL e quebra o último HH
        # -----------------------------

        elif (
            market_structure.higher_high
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
            explanation=tuple(explanation)
        )