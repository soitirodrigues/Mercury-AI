import pandas as pd
from typing import List, Tuple

from mercury_ai.models.evidence import Evidence
from mercury_ai.models.swing_analysis import Swing, SwingSequenceResult


class SwingEngine:
    """
    Motor institucional de estrutura de mercado Mercury AI.
    Compatível com padrão OHLCV:
    open, high, low, close, volume
    """

    def __init__(
        self,
        pivot_window: int = 5,
        atr_period: int = 14,
        atr_multiplier: float = 0.5
    ):

        self.pivot_window = pivot_window
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier



    def calculate_atr(self, df):

        high = df["high"]
        low = df["low"]
        close = df["close"]


        prev_close = close.shift(1)


        tr = pd.concat(
            [
                high - low,
                (high - prev_close).abs(),
                (low - prev_close).abs()
            ],
            axis=1
        ).max(axis=1)


        return (
            tr
            .ewm(
                alpha=1/self.atr_period,
                adjust=False
            )
            .mean()
        )



    def detect_swings(
        self,
        df: pd.DataFrame
    ) -> Tuple[List[Swing], List[Evidence]]:


        highs = df["high"]
        lows = df["low"]

        volume = (
            df["volume"]
            if "volume" in df.columns
            else pd.Series(
                0,
                index=df.index
            )
        )


        atr = self.calculate_atr(df)


        confirmed_highs = []
        confirmed_lows = []

        evidences = []



        for i in range(
            self.pivot_window,
            len(df)-self.pivot_window
        ):



            # ======================
            # SWING HIGH
            # ======================

            if (
                all(
                    highs.iloc[i] >
                    highs.iloc[i-self.pivot_window:i]
                )
                and
                all(
                    highs.iloc[i] >
                    highs.iloc[i+1:i+self.pivot_window+1]
                )
            ):


                price = float(
                    highs.iloc[i]
                )


                if (
                    not confirmed_highs
                    or
                    abs(
                        confirmed_highs[-1].price
                        -
                        price
                    )
                    >
                    atr.iloc[i] *
                    self.atr_multiplier
                ):


                    classification = (
                        "HH"
                        if (
                            not confirmed_highs
                            or
                            price >
                            confirmed_highs[-1].price
                        )
                        else
                        "LH"
                    )


                    swing = Swing(
                        "HIGH",
                        classification,
                        price,
                        str(df.index[i]),
                        i,
                        float(atr.iloc[i]),
                        100.0,
                        float(volume.iloc[i]),
                        True,
                        0.0
                    )


                    confirmed_highs.append(
                        swing
                    )


                    evidences.append(
                        Evidence(
                            "SwingEngine",
                            f"New {classification}",
                            "BULLISH"
                            if classification=="HH"
                            else "BEARISH",
                            70.0,
                            90.0,
                            f"Swing High {classification}",
                            20.0
                        )
                    )




            # ======================
            # SWING LOW
            # ======================


            if (
                all(
                    lows.iloc[i] <
                    lows.iloc[i-self.pivot_window:i]
                )
                and
                all(
                    lows.iloc[i] <
                    lows.iloc[i+1:i+self.pivot_window+1]
                )
            ):


                price = float(
                    lows.iloc[i]
                )


                if (
                    not confirmed_lows
                    or
                    abs(
                        confirmed_lows[-1].price
                        -
                        price
                    )
                    >
                    atr.iloc[i] *
                    self.atr_multiplier
                ):


                    classification = (
                        "HL"
                        if (
                            not confirmed_lows
                            or
                            price >
                            confirmed_lows[-1].price
                        )
                        else
                        "LL"
                    )


                    swing = Swing(
                        "LOW",
                        classification,
                        price,
                        str(df.index[i]),
                        i,
                        float(atr.iloc[i]),
                        100.0,
                        float(volume.iloc[i]),
                        True,
                        0.0
                    )


                    confirmed_lows.append(
                        swing
                    )


                    evidences.append(
                        Evidence(
                            "SwingEngine",
                            f"New {classification}",
                            "BULLISH"
                            if classification=="HL"
                            else "BEARISH",
                            70.0,
                            90.0,
                            f"Swing Low {classification}",
                            20.0
                        )
                    )



        return (
            confirmed_highs + confirmed_lows,
            evidences
        )



    def analyze_sequence(
        self,
        swings
    ):

        if len(swings) < 3:
            return SwingSequenceResult()


        sorted_swings = sorted(
            swings,
            key=lambda x:x.index
        )


        sequence = [
            s.classification
            for s in sorted_swings[-5:]
        ]


        trend="NEUTRAL"
        transition=False


        if all(
            x in ["HH","HL"]
            for x in sequence[-4:]
        ):

            trend="BULLISH"



        elif all(
            x in ["LL","LH"]
            for x in sequence[-4:]
        ):

            trend="BEARISH"


        else:

            transition=True



        return SwingSequenceResult(
            current_swing=sorted_swings[-1],
            previous_swing=sorted_swings[-2],
            sequence=sequence,
            sequence_length=len(sequence),
            trend_direction=trend,
            trend_transition=transition,
            sequence_quality=85.0,
            sequence_confidence=90.0
        )