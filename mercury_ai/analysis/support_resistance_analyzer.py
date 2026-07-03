from dataclasses import dataclass

import pandas as pd


@dataclass
class SupportResistanceAnalysis:
    support: float
    resistance: float
    distance_support: float
    distance_resistance: float
    explanation: list[str]


class SupportResistanceAnalyzer:

    def analyze(self, df: pd.DataFrame):

        support = df["Low"].tail(20).min()
        resistance = df["High"].tail(20).max()

        close = df["Close"].iloc[-1]

        return SupportResistanceAnalysis(

            support=float(support),

            resistance=float(resistance),

            distance_support=round(close - support, 2),

            distance_resistance=round(resistance - close, 2),

            explanation=[
                "Suporte calculado pelos últimos 20 candles",
                "Resistência calculada pelos últimos 20 candles"
            ]
        )