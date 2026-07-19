from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class DecisionInput:
    market_bias: str
    confluence_score: float
    confidence: float
    risk_score: float
    market_state: str
    warnings: List[str] = field(default_factory=list)
    blockers: List[str] = field(default_factory=list)
    opportunity_grade: str = "C"
    institutional_alignment: bool = False
