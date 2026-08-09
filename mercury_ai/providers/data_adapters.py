import pandas as pd
import yfinance as yf
import logging

from mercury_ai.providers.data_interfaces import IDataProvider
from mercury_ai.config.universe import ALL_SYMBOLS, FOREX_SYMBOLS, CRYPTO_SYMBOLS


class BaseAdapter:

    def __init__(
        self,
        name,
        timeframes,
        markets,
        assets,
        limit,
        priority
    ):

        self.name = name
        self.supported_timeframes = timeframes
        self.supported_markets = markets
        self.supported_assets = assets
        self.request_limit = limit
        self.priority = priority
        # Apenas adapters com implementação real de get_data são "implemented".
        # Stubs (herdeiros que não sobrescrevem get_data) são indisponíveis.
        self.is_implemented = False


    def check_health(self):

        # Saúde honesta: um adapter sem implementação real (stub) NÃO está
        # disponível, mesmo que registrado no catálogo de providers.
        return self.is_implemented



    def get_data(
        self,
        symbol,
        interval="5m"
    ):

        return pd.DataFrame()



class YahooAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Yahoo",
            [
                "1m",
                "5m",
                "15m",
                "1h"
            ],
            [
                "Forex",
                "Stocks",
                "Commodities",
                "Crypto"
            ],
            ALL_SYMBOLS,
            1000,
            1
        )

        # Único adapter com implementação real de get_data no V1.
        self.is_implemented = True


    def get_data(
        self,
        symbol,
        interval="5m"
    ):

        logging.debug(
            f"Yahoo buscando {symbol}"
        )


        df = yf.download(
            symbol,
            period="5d",
            interval=interval,
            progress=False
        )


        if df.empty:
            return pd.DataFrame()


        if isinstance(df.columns, pd.MultiIndex):

            df.columns = df.columns.get_level_values(0)


        df = df.rename(
            columns={
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Volume": "volume"
            }
        )


        return df



class PolygonAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Polygon",
            ["1m","5m","1h"],
            ["Stocks","Crypto"],
            CRYPTO_SYMBOLS,
            500,
            2
        )



class TwelveDataAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "TwelveData",
            ["1m","5m","1h"],
            ["Forex","Stocks"],
            FOREX_SYMBOLS,
            800,
            3
        )



class AlphaVantageAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "AlphaVantage",
            ["5m","1h","1d"],
            ["Stocks"],
            ALL_SYMBOLS,
            500,
            4
        )



class BinanceAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Binance",
            ["1m","5m","1h"],
            ["Crypto"],
            CRYPTO_SYMBOLS,
            1200,
            1
        )



class MetaTrader5Adapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "MetaTrader5",
            ["1m","5m","1h","1d"],
            ["Forex","Commodities"],
            FOREX_SYMBOLS,
            9999,
            5
        )