import yfinance as yf
import ta


class MarketProvider:

    def get_price(self, symbol):

        ticker = yf.Ticker(symbol)

        df = ticker.history(period="3mo")

        if df.empty:
            return None

        df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()

        bb = ta.volatility.BollingerBands(df["Close"])

        df["BB_HIGH"] = bb.bollinger_hband()
        df["BB_LOW"] = bb.bollinger_lband()

        ema20 = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()
        ema50 = ta.trend.EMAIndicator(df["Close"], window=50).ema_indicator()

        last = df.iloc[-1]

        trend = "UP" if ema20.iloc[-1] > ema50.iloc[-1] else "DOWN"

        if last["Close"] <= last["BB_LOW"]:
            bollinger = "LOWER"

        elif last["Close"] >= last["BB_HIGH"]:
            bollinger = "UPPER"

        else:
            bollinger = "MIDDLE"

        return {

            "symbol": symbol,

            "open": float(last["Open"]),
            "high": float(last["High"]),
            "low": float(last["Low"]),
            "close": float(last["Close"]),
            "volume": int(last["Volume"]),

            "trend": trend,

            "rsi": float(last["RSI"]),

            "bollinger": bollinger
        }