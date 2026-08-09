from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class DecisionInput:
    market_bias: str
    confluence_score: float
    confidence: float
    risk_score: float
    market_state: str
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    blockers: Tuple[str, ...] = field(default_factory=tuple)
    opportunity_grade: str = "C"
    institutional_alignment: bool = False
