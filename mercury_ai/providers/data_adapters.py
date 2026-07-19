import pandas as pd
import yfinance as yf

from mercury_ai.providers.data_interfaces import IDataProvider


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


    def check_health(self):

        return True



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
            [
                "BTC-USD",
                "AAPL",
                "GC=F",
                "EURUSD=X"
            ],
            1000,
            1
        )


    def get_data(
        self,
        symbol,
        interval="5m"
    ):

        print(
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
            ["AAPL","BTC-USD"],
            500,
            2
        )



class TwelveDataAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "TwelveData",
            ["1m","5m","1h"],
            ["Forex","Stocks"],
            ["EURUSD","AAPL"],
            800,
            3
        )



class AlphaVantageAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "AlphaVantage",
            ["5m","1h","1d"],
            ["Stocks"],
            ["AAPL"],
            500,
            4
        )



class BinanceAdapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "Binance",
            ["1m","5m","1h"],
            ["Crypto"],
            ["BTC-USD"],
            1200,
            1
        )



class MetaTrader5Adapter(BaseAdapter):

    def __init__(self):

        super().__init__(
            "MetaTrader5",
            ["1m","5m","1h","1d"],
            ["Forex","Commodities"],
            ["EURUSD","GC=F"],
            9999,
            5
        )