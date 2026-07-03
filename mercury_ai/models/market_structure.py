from dataclasses import dataclass, field


@dataclass
class MarketStructure:

    trend: str = "RANGE"

    higher_high: bool = False
    higher_low: bool = False

    lower_high: bool = False
    lower_low: bool = False

    swing_highs: int = 0
    swing_lows: int = 0

    confidence: int = 0

    explanation: list[str] = field(default_factory=list)