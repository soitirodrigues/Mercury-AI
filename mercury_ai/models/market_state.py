from dataclasses import dataclass
from mercury_ai.models.market_state_enum import MarketStateEnum

@dataclass(frozen=True)
class MarketState:
    state: MarketStateEnum
    explanation: str
