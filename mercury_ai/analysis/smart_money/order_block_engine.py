import pandas as pd
from typing import Optional, Dict


class OrderBlockEngine:
    """
    Identifica Order Blocks institucionais.
    """

    def analyze(
        self,
        df: pd.DataFrame
    ) -> Optional[Dict]:

        if df is None or len(df) < 20:
            return None


        df = df.copy()

        df = df.reset_index(drop=True)



        # Remove colunas duplicadas
        df = df.loc[:, ~df.columns.duplicated()]



        # Garantir dados numéricos

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

            return None



        volume = df["Volume"]


        vol_avg = (
            volume
            .rolling(20)
            .mean()
            .iloc[-1]
        )


        current_volume = (
            volume
            .iloc[-1]
        )



        if pd.isna(vol_avg):

            return None



        candle = df.iloc[-1]



        if current_volume > vol_avg * 1.5:

            return {

                "type": "BULLISH_OB",

                "price": float(
                    candle["Low"]
                ),

                "volume_strength": float(
                    current_volume / vol_avg
                )

            }



        return None