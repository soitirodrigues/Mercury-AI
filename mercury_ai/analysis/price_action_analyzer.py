from mercury_ai.models.price_action import PriceActionAnalysis


class PriceActionAnalyzer:

    def analyze(self, df):
        if len(df) < 2:
            return PriceActionAnalysis(
                trend_structure="UNKNOWN",
                last_event="UNKNOWN",
                confidence=0,
                explanation=["Dados insuficientes"]
            )

        highs = df["High"]
        lows = df["Low"]

        explanation = []

        # Estrutura extremamente simples (v1)
        if highs.iloc[-1] > highs.iloc[-2] and lows.iloc[-1] > lows.iloc[-2]:

            structure = "BULLISH"

            explanation.append(
                "Máximas e mínimas ascendentes."
            )

        elif highs.iloc[-1] < highs.iloc[-2] and lows.iloc[-1] < lows.iloc[-2]:

            structure = "BEARISH"

            explanation.append(
                "Máximas e mínimas descendentes."
            )

        else:

            structure = "RANGE"

            explanation.append(
                "Mercado sem estrutura clara."
            )

        return PriceActionAnalysis(

            trend_structure=structure,

            last_event=structure,

            confidence=0, # Neutral value as it's not a confidence engine

            explanation=explanation
        )