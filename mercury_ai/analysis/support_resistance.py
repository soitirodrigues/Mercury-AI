import pandas as pd


class SupportResistanceAnalyzer:
    """
    Detecta suportes e resistências simples
    utilizando máximas e mínimas recentes.
    """

    def analyze(self, df: pd.DataFrame):

        support = df["Low"].tail(30).min()

        resistance = df["High"].tail(30).max()

        current_price = df["Close"].iloc[-1]

        distance_support = round(current_price - support, 2)

        distance_resistance = round(resistance - current_price, 2)

        near_support = distance_support <= (
            current_price * 0.003
        )

        near_resistance = distance_resistance <= (
            current_price * 0.003
        )

        return {
            "support": support,
            "resistance": resistance,
            "distance_support": distance_support,
            "distance_resistance": distance_resistance,
            "near_support": near_support,
            "near_resistance": near_resistance
        }