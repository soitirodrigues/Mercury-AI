from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class MarketStructure:

    trend: str = "RANGE"

    higher_high: bool = False
    higher_low: bool = False

    lower_high: bool = False
    lower_low: bool = False

    swing_highs: int = 0
    swing_lows: int = 0

    confidence: int = 0

    explanation: Tuple[str, ...] = field(default_factory=tuple)