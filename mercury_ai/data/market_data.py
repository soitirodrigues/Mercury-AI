import pandas as pd
import yfinance as yf


class MarketDataService:
    """
    Responsável por baixar e padronizar os candles.
    """

    def get_data(
        self,
        symbol: str,
        interval: str = "5m",
        period: str = "5d"
    ) -> pd.DataFrame:

        df = yf.download(
            tickers=symbol,
            interval=interval,
            period=period,
            progress=False,
            auto_adjust=True,
        )

        if df.empty:
            raise ValueError(f"Nenhum dado encontrado para {symbol}")

        # Remove MultiIndex, se existir
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df[["Open", "High", "Low", "Close", "Volume"]]

        df.dropna(inplace=True)

        return df.reset_index()