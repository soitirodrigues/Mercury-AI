from typing import List

import pandas as pd

from mercury_ai.core.exceptions import MarketClosedException
from mercury_ai.data.data_normalizer import DataNormalizer



class MarketDataService:


    def __init__(
        self,
        provider=None,
        providers: List = None,
        provider_manager=None
    ):

        self.provider_manager = (
            provider_manager
            or provider
        )

        self.providers = providers or []



    # =====================================================
    # NORMALIZAÇÃO CENTRAL
    # =====================================================

    def _normalize_dataframe(
        self,
        df: pd.DataFrame
    ) -> pd.DataFrame:

        if df is None:
            return df

        if df.empty:
            return df


        try:

            return DataNormalizer.normalize(df)


        except Exception as e:

            print(
                f"Normalizador Mercury falhou: {e}"
            )


            # fallback de segurança

            rename = {}

            for col in df.columns:

                name = str(col).lower()


                if name == "open":
                    rename[col] = "Open"

                elif name == "high":
                    rename[col] = "High"

                elif name == "low":
                    rename[col] = "Low"

                elif name == "close":
                    rename[col] = "Close"

                elif name == "volume":
                    rename[col] = "Volume"



            df = df.rename(
                columns=rename
            )


            if "Open" not in df.columns and "Close" in df.columns:
                df["Open"] = df["Close"]


            if "High" not in df.columns and "Close" in df.columns:
                df["High"] = df["Close"]


            if "Low" not in df.columns and "Close" in df.columns:
                df["Low"] = df["Close"]


            if "Volume" not in df.columns:
                df["Volume"] = 0.0


            return df




    # =====================================================
    # BUSCA PRINCIPAL DE DADOS
    # =====================================================


    def get_data(
        self,
        symbol: str,
        interval: str = "5m",
        period: str = "5d"
    ) -> pd.DataFrame:



        # -------------------------------------------------
        # Mercury Data Provider V1
        # -------------------------------------------------

        if self.provider_manager:


            try:


                provider = (
                    self.provider_manager
                    .best_provider(symbol)
                )


                if provider:


                    df = provider.get_data(
                        symbol,
                        interval
                    )


                    return self._normalize_dataframe(
                        df
                    )


            except Exception as e:


                print(
                    f"Mercury Provider falhou: {e}"
                )



        # -------------------------------------------------
        # Providers antigos
        # -------------------------------------------------


        for provider in self.providers:


            try:


                if hasattr(
                    provider,
                    "is_available"
                ):


                    if not provider.is_available():
                        continue



                if hasattr(
                    provider,
                    "supports_symbol"
                ):


                    if not provider.supports_symbol(symbol):
                        continue



                df = provider.get_data(
                    symbol,
                    interval,
                    period
                )


                return self._normalize_dataframe(
                    df
                )



            except MarketClosedException:

                raise



            except Exception as e:


                print(
                    f"Provider {provider} falhou: {e}"
                )


                continue



        raise Exception(
            f"No provider available for {symbol}"
        )