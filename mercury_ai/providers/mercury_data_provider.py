from typing import Dict
import pandas as pd
import time
import logging
from functools import lru_cache


from mercury_ai.providers.data_interfaces import IDataProvider

from mercury_ai.providers.data_adapters import (
    YahooAdapter,
    PolygonAdapter,
    TwelveDataAdapter,
    AlphaVantageAdapter,
    BinanceAdapter,
    MetaTrader5Adapter
)


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger("MercuryDataProvider")


class MercuryDataProvider:


    def __init__(self):

        self._providers: Dict[str, IDataProvider] = {}

        self.register_provider(YahooAdapter())
        self.register_provider(PolygonAdapter())
        self.register_provider(TwelveDataAdapter())
        self.register_provider(AlphaVantageAdapter())
        self.register_provider(BinanceAdapter())
        self.register_provider(MetaTrader5Adapter())


    def register_provider(
        self,
        provider: IDataProvider
    ):

        self._providers[
            provider.name
        ] = provider



    # ==================================================
    # COMPATIBILIDADE MARKET DATA SERVICE
    # ==================================================

    def best_provider(
        self,
        symbol: str
    ):

        return self._get_best_provider(symbol)



    def is_available(self) -> bool:

        try:

            return any(
                provider.check_health()
                for provider in self._providers.values()
            )

        except Exception:

            return False



    # ==================================================
    # ESCOLHA INTELIGENTE DO PROVIDER
    # ==================================================

    def _get_best_provider(
        self,
        symbol: str
    ):


        candidates = [

            provider

            for provider in self._providers.values()

            if (
                symbol in provider.supported_assets
                and provider.check_health()
            )

        ]


        if not candidates:

            candidates = [

                provider

                for provider in self._providers.values()

                if provider.check_health()

            ]


        if not candidates:

            raise Exception(
                "Nenhum provider disponível"
            )


        return min(
            candidates,
            key=lambda p: p.priority
        )



    # ==================================================
    # CONEXÃO
    # ==================================================

    def connect(self):

        return all(

            provider.check_health()

            for provider in self._providers.values()

        )



    def health(self):

        return {

            name:
            provider.check_health()

            for name, provider
            in self._providers.items()

        }



    # ==================================================
    # BUSCA PRINCIPAL DE DADOS
    # ==================================================

    @lru_cache(maxsize=128)
    def get_candles(
        self,
        symbol: str,
        interval="5m",
        retries=3,
        timeout=5.0
    ) -> pd.DataFrame:


        last_error = None


        for attempt in range(retries):

            try:


                provider = self._get_best_provider(symbol)


                logger.info(
                    f"{symbol} usando {provider.name}"
                )


                start = time.time()


                data = provider.get_data(
                    symbol,
                    interval
                )


                elapsed = time.time() - start


                if elapsed > timeout:

                    raise TimeoutError(
                        "Tempo excedido"
                    )


                return data


            except Exception as e:


                last_error = e


                logger.warning(
                    f"Tentativa {attempt+1} falhou: {e}"
                )


                time.sleep(0.5)



        raise Exception(
            f"Falha ao buscar {symbol}: {last_error}"
        )



    # ==================================================
    # ALIASES UTILIZADOS PELO SISTEMA
    # ==================================================

    def get_history(
        self,
        symbol,
        timeframe="5m"
    ):

        return self.get_candles(
            symbol,
            timeframe
        )



    def get_data(
        self,
        symbol,
        interval="5m",
        period="5d"
    ):


        provider = self._get_best_provider(
            symbol
        )


        return provider.get_data(
            symbol,
            interval
        )



    def get_last_price(
        self,
        symbol
    ):


        provider = self._get_best_provider(
            symbol
        )


        return getattr(
            provider,
            "get_last_price",
            lambda s: 0.0
        )(symbol)



    def market_status(
        self,
        symbol
    ):


        provider = self._get_best_provider(
            symbol
        )


        return getattr(
            provider,
            "market_status",
            lambda s: "OPEN"
        )(symbol)