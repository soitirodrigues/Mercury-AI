import pandas as pd
from ta.trend import EMAIndicator, MACD, ADXIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange, BollingerBands


class IndicatorEngine:
    """
    Calcula os principais indicadores técnicos da Mercury AI.
    """

    def calculate(self, df: pd.DataFrame) -> dict:

        close = df["Close"]
        high = df["High"]
        low = df["Low"]

        ema9 = EMAIndicator(close, window=9).ema_indicator().iloc[-1]
        ema21 = EMAIndicator(close, window=21).ema_indicator().iloc[-1]
        ema50 = EMAIndicator(close, window=50).ema_indicator().iloc[-1]

        rsi = RSIIndicator(close, window=14).rsi().iloc[-1]

        atr = AverageTrueRange(
            high,
            low,
            close,
            window=14
        ).average_true_range().iloc[-1]

        adx = ADXIndicator(
            high,
            low,
            close,
            window=14
        ).adx().iloc[-1]

        macd = MACD(close)

        bb = BollingerBands(close)

        return {

            "close": float(close.iloc[-1]),

            "ema9": float(ema9),
            "ema21": float(ema21),
            "ema50": float(ema50),

            "rsi": float(rsi),

            "atr": float(atr),

            "adx": float(adx),

            "macd": float(macd.macd().iloc[-1]),

            "macd_signal": float(macd.macd_signal().iloc[-1]),

            "bollinger_upper": float(bb.bollinger_hband().iloc[-1]),

            "bollinger_lower": float(bb.bollinger_lband().iloc[-1]),

            "volume": float(df["Volume"].iloc[-1])
        }