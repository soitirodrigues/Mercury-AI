from enum import Enum

class MarketStateEnum(Enum):
        # ----------------------------
    # Estado Operacional
    # ----------------------------

    OPEN = "OPEN"
    PRE_OPEN = "PRE_OPEN"
    PRE_CLOSE = "PRE_CLOSE"
    CLOSED = "CLOSED"
    HOLIDAY = "HOLIDAY"
    MAINTENANCE = "MAINTENANCE"

    # ----------------------------
    # Estado Estrutural
    # ----------------------------

    TRENDING = "TRENDING"
    RANGING = "RANGING"

    HIGH_VOLATILITY = "HIGH_VOLATILITY"
    LOW_VOLATILITY = "LOW_VOLATILITY"

    HIGH_LIQUIDITY = "HIGH_LIQUIDITY"
    LOW_LIQUIDITY = "LOW_LIQUIDITY"

    BREAKOUT = "BREAKOUT"
    PULLBACK = "PULLBACK"
    ACCUMULATION = "ACCUMULATION"
    DISTRIBUTION = "DISTRIBUTION"

    UNKNOWN = "UNKNOWN"
