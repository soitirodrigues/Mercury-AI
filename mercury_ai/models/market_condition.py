from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class MarketCondition:
    trend: Optional[str] = None
    trend_strength: Optional[float] = None
    market_state: Optional[str] = None
    explanation: Optional[str] = None
