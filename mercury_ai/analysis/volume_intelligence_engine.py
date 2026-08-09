from typing import List, Tuple

import pandas as pd

from mercury_ai.models.evidence import Evidence
from mercury_ai.models.volume_profile import VolumeProfile
from mercury_ai.config.institutional_weights import INSTITUTIONAL_WEIGHTS


class VolumeIntelligenceEngine:
    """
    Motor institucional para análise de volume.
    """


    def evaluate(
        self,
        df: pd.DataFrame
    ) -> Tuple[VolumeProfile, List[Evidence]]:


        if df is None or len(df) < 20:
            return VolumeProfile(), []



        df = df.copy()

        df = df.reset_index(drop=True)



        # Remove colunas duplicadas
        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]



        # Garantir formato numérico

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



        if "Volume" not in df.columns:

            return VolumeProfile(), []



        volume = df["Volume"]


        closes = df["Close"]

        highs = df["High"]

        lows = df["Low"]



        price_spread = (
            highs - lows
        ).abs()



        avg_volume = (
            volume
            .rolling(20)
            .mean()
            .iloc[-1]
        )


        current_volume = (
            volume
            .iloc[-1]
        )


        avg_spread = (
            price_spread
            .rolling(20)
            .mean()
            .iloc[-1]
        )


        current_spread = (
            price_spread
            .iloc[-1]
        )



        # Proteção pandas

        if pd.isna(avg_volume):

            return VolumeProfile(), []



        if avg_volume <= 0:

            return VolumeProfile(), []



        relative_volume = (
            current_volume / avg_volume
        )



        spike = relative_volume > 2.0

        dry = relative_volume < 0.5

        climactic = relative_volume > 2.5

        absorption = (
            relative_volume > 1.5
            and current_spread < avg_spread
        )



        divergence = (
            closes.diff().iloc[-1]
            *
            volume.diff().iloc[-1]
        ) < 0



        no_demand = (
            relative_volume < 0.7
            and closes.iloc[-1] > closes.iloc[-2]
        )


        no_supply = (
            relative_volume < 0.7
            and closes.iloc[-1] < closes.iloc[-2]
        )



        evidences = []



        if spike:

            evidences.append(
                Evidence(
                    engine_name="VolumeEngine",
                    evidence_name="Volume Spike",
                    direction="NEUTRAL",
                    strength=60.0,
                    confidence=70.0,
                    description="Volume acima da média",
                    weight=INSTITUTIONAL_WEIGHTS["smart_money"],
                )
            )



        if absorption:

            evidences.append(
                Evidence(
                    engine_name="VolumeEngine",
                    evidence_name="Absorption",
                    direction="NEUTRAL",
                    strength=80.0,
                    confidence=80.0,
                    description="Absorção institucional detectada",
                    weight=INSTITUTIONAL_WEIGHTS["smart_money"],
                )
            )



        profile = VolumeProfile(

            relative_volume=float(relative_volume),

            volume_spike=spike,

            dry_volume=dry,

            absorption=absorption,

            volume_divergence=divergence,

            buying_climax=(
                climactic
                and closes.iloc[-1] > closes.iloc[-2]
            ),

            selling_climax=(
                climactic
                and closes.iloc[-1] < closes.iloc[-2]
            ),

            institutional_participation=min(
                relative_volume * 20,
                100
            ),

            confidence_score=75.0
        )


        return profile, evidences