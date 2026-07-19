from dataclasses import dataclass
from typing import Tuple
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class MarketEvidenceBundle:
    """
    Immutable internal transport model for aggregated market evidence.
    """
    evidences: Tuple[Evidence, ...]
    timestamp: str
    asset: str
    timeframe: str
