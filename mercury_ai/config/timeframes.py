SCALPING = [
    "M1",
    "M5"
]

INTRADAY = [
    "M15",
    "M30",
    "H1"
]

SWING = [
    "H4",
    "D1",
    "W1",
    "MN"
]

SUPPORTED_TIMEFRAMES = {
    "SCALPING": SCALPING,
    "INTRADAY": INTRADAY,
    "SWING": SWING,
}

YFINANCE_INTERVALS = {
    "M1": "1m",
    "M5": "5m",
    "M15": "15m",
    "M30": "30m",
    "H1": "1h",
    "H4": "4h",
    "D1": "1d",
    "W1": "1wk",
    "MN": "1mo"
}

# Default Institutional Timeframe
DEFAULT_TIMEFRAME = SCALPING[1]  # "M5"
