from dataclasses import dataclass
from typing import Optional, Tuple
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class VolatilityAnalysis:
    state: Optional[str] = None
    score: Optional[float] = None
    expanding: Optional[bool] = None
    contracting: Optional[bool] = None
    evidences: Tuple[Evidence, ...] = ()
