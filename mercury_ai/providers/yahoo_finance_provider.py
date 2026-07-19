import yfinance as yf
import pandas as pd
from mercury_ai.providers.base_provider import MarketDataProvider
from mercury_ai.core.exceptions import MarketClosedException

class YahooFinanceProvider:
    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty or len(df) < 20:
            raise MarketClosedException(f"Market closed or insufficient data for {symbol}")
            
        required_columns = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in df.columns for col in required_columns):
             raise MarketClosedException(f"Missing required columns for {symbol}")
             
        return df

    def is_available(self) -> bool:
        return True # Simplistic health check

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def supports_market(self, market: str) -> bool:
        return True

    def supports_timeframe(self, timeframe: str) -> bool:
        return True

    def max_history(self) -> str:
        return "10y"

    def source_name(self) -> str:
        return "YahooFinance"
