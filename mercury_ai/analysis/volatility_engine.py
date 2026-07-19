import pandas as pd
from typing import List

from mercury_ai.models.volatility_analysis import VolatilityAnalysis
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.evidence import Evidence


ATR_LOW_RATIO = 0.8
ATR_HIGH_RATIO = 1.2
ATR_EXPLOSIVE_RATIO = 1.5


class VolatilityEngine:
    """
    Analisa volatilidade usando ATR.
    """


    def analyze(
        self,
        df: pd.DataFrame,
        market: MarketData
    ) -> VolatilityAnalysis:


        if df is None or len(df) < 20:

            return VolatilityAnalysis(
                "LOW",
                0.0,
                False,
                False,
                ()
            )



        df = df.copy()

        df = df.reset_index(drop=True)



        # Remove colunas duplicadas

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]



        # Normalização numérica

        for col in [
            "Open",
            "High",
            "Low",
            "Close",
            "Volume"
        ]:

            if col in df.columns:

                df[col] = pd.to_numeric(
                    df[col],
                    errors="coerce"
                )



        required = [
            "High",
            "Low",
            "Close"
        ]


        for col in required:

            if col not in df.columns:

                return VolatilityAnalysis(
                    "LOW",
                    0.0,
                    False,
                    False,
                    ()
                )



        if "ATR" not in df.columns:


            from ta.volatility import AverageTrueRange


            atr = AverageTrueRange(

                high=df["High"],

                low=df["Low"],

                close=df["Close"],

                window=14

            )


            df["ATR"] = atr.average_true_range()



        atr_series = df["ATR"]



        current_atr = float(
            atr_series.iloc[-1]
        )


        avg_atr = float(
            atr_series.tail(20).mean()
        )



        if avg_atr <= 0 or pd.isna(avg_atr):

            ratio = 1.0

        else:

            ratio = current_atr / avg_atr



        evidences: List[Evidence] = []



        if ratio < ATR_LOW_RATIO:

            state = "LOW"


        elif ratio < ATR_HIGH_RATIO:

            state = "NORMAL"


        elif ratio < ATR_EXPLOSIVE_RATIO:

            state = "HIGH"


        else:

            state = "EXPLOSIVE"



        evidences.append(

            Evidence(

                "VolatilityEngine",

                "ATR",

                "NEUTRAL",

                70.0,

                85.0,

                f"ATR Ratio {ratio:.2f}",

                20.0

            )

        )



        expanding = False

        contracting = False



        if len(atr_series) >= 3:


            expanding = (
                atr_series.iloc[-3]
                <
                atr_series.iloc[-2]
                <
                atr_series.iloc[-1]
            )


            contracting = (
                atr_series.iloc[-3]
                >
                atr_series.iloc[-2]
                >
                atr_series.iloc[-1]
            )



        score = min(
            max(
                ratio * 50,
                0
            ),
            100
        )



        return VolatilityAnalysis(

            state=state,

            score=float(score),

            expanding=bool(expanding),

            contracting=bool(contracting),

            evidences=tuple(evidences)

        )