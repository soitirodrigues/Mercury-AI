from mercury_ai.models.smart_money import SmartMoneyAnalysis

from mercury_ai.analysis.smart_money.market_structure_engine import (
    MarketStructureEngine,
)


class SmartMoneyEngine:

    def __init__(self):

        self.structure_engine = MarketStructureEngine()

    def analyze(self, df):

        structure = self.structure_engine.analyze(df)

        explanation = []

        score = 0

        if structure.trend == "BULLISH":

            score += 40
            explanation.append("Estrutura Bullish")

        elif structure.trend == "BEARISH":

            score -= 40
            explanation.append("Estrutura Bearish")

        confidence = abs(score)

        return SmartMoneyAnalysis(
            structure=structure,
            score=score,
            confidence=confidence,
            explanation=explanation
        )