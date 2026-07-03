from dataclasses import dataclass


@dataclass
class MarketData:
    symbol: str
    timeframe: str

    close: float

    ema9: float
    ema21: float
    ema50: float

    rsi: float

    atr: float
    adx: float

    macd: float
    macd_signal: float

    bollinger_upper: float
    bollinger_lower: float

    volume: float