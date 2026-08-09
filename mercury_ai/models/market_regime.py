from dataclasses import dataclass
from typing import Tuple
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_regime_enum import MarketRegimeEnum

@dataclass(frozen=True)
class MarketRegime:
    regime: MarketRegimeEnum
    confidence: float
    supporting_evidences: Tuple[Evidence, ...]
