from dataclasses import dataclass
from typing import Tuple

from mercury_ai.models.market_structure import MarketStructure


@dataclass(frozen=True)
class BOSResult:
    detected: bool
    direction: str
    confidence: int
    explanation: Tuple[str, ...]


class BOSEngine:

    def analyze(self, market_structure: MarketStructure) -> BOSResult:

        explanation = []

        detected = False
        direction = "NONE"
        confidence = 0

        if (
            market_structure.higher_high
            and market_structure.higher_low
        ):

            detected = True
            direction = "BULLISH"
            confidence = market_structure.confidence

            explanation.append(
                "Rompimento de estrutura de alta confirmado."
            )

        elif (
            market_structure.lower_high
            and market_structure.lower_low
        ):

            detected = True
            direction = "BEARISH"
            confidence = market_structure.confidence

            explanation.append(
                "Rompimento de estrutura de baixa confirmado."
            )

        else:

            explanation.append(
                "Nenhum rompimento estrutural confirmado."
            )

        return BOSResult(
            detected=detected,
            direction=direction,
            confidence=confidence,
            explanation=tuple(explanation),
        )