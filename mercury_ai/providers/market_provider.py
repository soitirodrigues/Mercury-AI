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
    MetaTrader5Adapter,
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

    # ---------------------------------------------------------

    def register_provider(self, provider: IDataProvider):

        self._providers[provider.name] = provider

    # ---------------------------------------------------------

    def _healthy_providers(self):

        return [
            provider
            for provider in self._providers.values()
            if provider.check_health()
        ]

    # ---------------------------------------------------------

    def _get_best_provider(self, symbol: str) -> IDataProvider:

        candidates = [

            provider

            for provider in self._healthy_providers()

            if symbol in provider.supported_assets

        ]

        if not candidates:

            candidates = self._healthy_providers()

        if not candidates:

            raise RuntimeError("No healthy providers available.")

        return min(candidates, key=lambda p: p.priority)

    # ---------------------------------------------------------
    # PUBLIC API
    # ---------------------------------------------------------

    def best_provider(self, symbol: str):

        return self._get_best_provider(symbol)

    # ---------------------------------------------------------
    def is_available(self) -> bool:
        """Verifica se há pelo menos um provider saudável."""
        try:
            return any(
                provider.check_health()
                for provider in self._providers.values()
            )
        except (ConnectionError, TimeoutError, RuntimeError, ValueError):
            return False

    # ---------------------------------------------------------

    def get_data(
        self,
        symbol: str,
        interval: str = "5m",
        period: str = "5d",
    ):
        """Obtém dados diretamente do melhor provider (sem cache/retry)."""
        provider = self._get_best_provider(symbol)
        return provider.get_data(symbol, interval)

    # ---------------------------------------------------------    def trigger_failover(self, reason: str = "") -> bool:

        logger.warning(f"Failover requested: {reason}")

        healthy = self._healthy_providers()

        if len(healthy) <= 1:

            logger.error("No fallback provider available.")

            return False

        logger.info("Fallback provider available.")

        return True

    # ---------------------------------------------------------

    def connect(self) -> bool:

        return len(self._healthy_providers()) > 0

    # ---------------------------------------------------------

    def health(self):

        return {

            provider.name: provider.check_health()

            for provider in self._providers.values()

        }

    # ---------------------------------------------------------

    @lru_cache(maxsize=128)

    def get_candles(

        self,

        symbol: str,

        interval: str = "5m",

        retries: int = 3,

        timeout: float = 5.0,

    ) -> pd.DataFrame:

        last_error = None

        for attempt in range(retries):

            provider = self._get_best_provider(symbol)

            try:

                logger.info(

                    f"{provider.name} -> {symbol} ({attempt+1}/{retries})"

                )

                start = time.time()

                candles = provider.get_data(symbol, interval)

                elapsed = time.time() - start

                if elapsed > timeout:

                    raise TimeoutError(

                        f"{provider.name} timeout ({elapsed:.2f}s)"

                    )

                return candles

            except Exception as e:

                last_error = e

                logger.warning(e)

                time.sleep(0.5)

        raise RuntimeError(last_error)

    # ---------------------------------------------------------

    def get_history(

        self,

        symbol: str,

        timeframe: str = "5m",

    ):

        return self.get_candles(symbol, timeframe)

    # ---------------------------------------------------------

    def get_last_price(self, symbol: str):

        provider = self._get_best_provider(symbol)

        return getattr(

            provider,

            "get_last_price",

            lambda _: 0.0,

        )(symbol)

    # ---------------------------------------------------------

    def market_status(self, symbol: str):

        provider = self._get_best_provider(symbol)

        return getattr(

            provider,

            "market_status",

            lambda _: "OPEN",

        )(symbol)