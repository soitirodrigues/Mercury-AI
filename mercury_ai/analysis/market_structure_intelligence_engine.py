from typing import List, Tuple
import pandas as pd

from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.analysis.swing_engine import SwingEngine


class MarketStructureIntelligenceEngine:
    """
    Motor institucional avançado para análise de estrutura de mercado baseado em SwingEngine.
    """

    def __init__(self):
        self.swing_engine = SwingEngine()

    def evaluate(
        self,
        df: pd.DataFrame,
        avg_volume: pd.Series = None,
        avg_body: pd.Series = None
    ) -> Tuple[MarketStructureProfile, List[Evidence]]:

        if df.empty:
            return MarketStructureProfile(), []

        swings, evidences = self.swing_engine.detect_swings(df)

        sequence_result = self.swing_engine.analyze_sequence(swings)

        bos = False
        choch = False
        mss = False

        break_price = 0.0
        break_strength = 0.0
        break_timestamp = ""

        impulses = []
        corrections = []

        for i in range(2, len(swings)):

            dist = abs(
                swings[i].price -
                swings[i - 1].price
            )

            if i % 2 == 0:
                impulses.append(dist)
            else:
                corrections.append(dist)

        avg_impulse = (
            sum(impulses) / len(impulses)
            if impulses else 1.0
        )

        avg_correction = (
            sum(corrections) / len(corrections)
            if corrections else 1.0
        )

        last_candle = df.iloc[-1]

        body = abs(
            last_candle["close"] -
            last_candle["open"]
        )

        if avg_volume is not None:
            avg_vol = avg_volume.iloc[-1]
        else:
            avg_vol = (
                df["volume"]
                .rolling(20)
                .mean()
                .iloc[-1]
            )

        if avg_body is not None:
            avg_bdy = avg_body.iloc[-1]
        else:
            avg_bdy = (
                (
                    df["close"] -
                    df["open"]
                )
                .abs()
                .rolling(20)
                .mean()
                .iloc[-1]
            )

        displacement = (
            body > (avg_bdy * 2.0)
            and
            last_candle["volume"] > avg_vol
        )

        direction = "NEUTRAL"

        if displacement:

            if last_candle["close"] > last_candle["open"]:
                direction = "BULLISH"
            else:
                direction = "BEARISH"

            evidences.append(
                Evidence(
                    "StructureEngine",
                    f"{direction} Displacement",
                    direction,
                    85.0,
                    90.0,
                    f"Displacement {direction} detectado",
                    40.0
                )
            )

        equilibrium = 0.0
        premium = 0.0
        discount = 0.0
        ote = 0.0

        if (
            sequence_result.current_swing
            and
            sequence_result.previous_swing
        ):

            high = max(
                sequence_result.current_swing.price,
                sequence_result.previous_swing.price
            )

            low = min(
                sequence_result.current_swing.price,
                sequence_result.previous_swing.price
            )

            rng = high - low

            equilibrium = low + (rng * 0.5)
            premium = low + (rng * 0.5)
            discount = low + (rng * 0.5)
            ote = low + (rng * 0.705)

            evidences.append(
                Evidence(
                    "StructureEngine",
                    "OTE",
                    "NEUTRAL",
                    80.0,
                    95.0,
                    "Nível OTE calculado",
                    30.0
                )
            )

        hh = sum(
            1 for s in swings
            if s.classification == "HH"
        )

        hl = sum(
            1 for s in swings
            if s.classification == "HL"
        )

        lh = sum(
            1 for s in swings
            if s.classification == "LH"
        )

        ll = sum(
            1 for s in swings
            if s.classification == "LL"
        )

        profile = MarketStructureProfile(
            classification=sequence_result.trend_direction,
            trend_strength=sequence_result.sequence_confidence,
            hh_count=hh,
            hl_count=hl,
            lh_count=lh,
            ll_count=ll,
            confidence_score=sequence_result.sequence_confidence,
            current_swing=sequence_result.current_swing,
            previous_swing=sequence_result.previous_swing,
            current_sequence=sequence_result.sequence,
            bos=bos,
            choch=choch,
            mss=mss,
            break_strength=break_strength,
            break_price=break_price,
            break_timestamp=break_timestamp,
            impulse_strength=float(avg_impulse),
            correction_strength=float(avg_correction),
            displacement=displacement,
            displacement_strength=(
                float(body / avg_bdy)
                if avg_bdy > 0
                else 0.0
            ),
            displacement_direction=direction,
            premium_zone=float(premium),
            discount_zone=float(discount),
            equilibrium=float(equilibrium),
            ote=float(ote)
        )

        return profile, evidences