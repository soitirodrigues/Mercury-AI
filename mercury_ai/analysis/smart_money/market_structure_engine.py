import pandas as pd

from mercury_ai.models.market_structure import MarketStructure


class MarketStructureEngine:

    def analyze(self, df: pd.DataFrame) -> MarketStructure:

        if df.empty:
            return MarketStructure(
                trend="RANGE",
                higher_high=False,
                higher_low=False,
                lower_high=False,
                lower_low=False,
                swing_highs=0,
                swing_lows=0,
                confidence=0,
                explanation=["DataFrame vazio"]
            )

        highs = df["high"].tolist()
        lows = df["low"].tolist()

        swing_highs = 0
        swing_lows = 0

        higher_high = False
        higher_low = False

        lower_high = False
        lower_low = False

        explanation = []

        # -----------------------------
        # Contagem simples de swings
        # -----------------------------

        for i in range(1, len(highs) - 1):

            if highs[i] > highs[i - 1] and highs[i] > highs[i + 1]:
                swing_highs += 1

            if lows[i] < lows[i - 1] and lows[i] < lows[i + 1]:
                swing_lows += 1

        # -----------------------------
        # Estrutura recente
        # -----------------------------

        if len(highs) >= 2:

            if highs[-1] > highs[-2]:
                higher_high = True
                explanation.append("Último topo é mais alto")

            elif highs[-1] < highs[-2]:
                lower_high = True
                explanation.append("Último topo é mais baixo")

        if len(lows) >= 2:

            if lows[-1] > lows[-2]:
                higher_low = True
                explanation.append("Último fundo é mais alto")

            elif lows[-1] < lows[-2]:
                lower_low = True
                explanation.append("Último fundo é mais baixo")

        # -----------------------------
        # Tendência
        # -----------------------------

        trend = "RANGE"
        confidence = 40

        if higher_high and higher_low:

            trend = "BULLISH"
            confidence = 85
            explanation.append("Sequência HH + HL")

        elif lower_high and lower_low:

            trend = "BEARISH"
            confidence = 85
            explanation.append("Sequência LH + LL")

        return MarketStructure(
            trend=trend,
            higher_high=higher_high,
            higher_low=higher_low,
            lower_high=lower_high,
            lower_low=lower_low,
            swing_highs=swing_highs,
            swing_lows=swing_lows,
            confidence=confidence,
            explanation=explanation
        )