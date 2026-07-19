from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class ProbabilityResult:
    buy_probability: float
    sell_probability: float
    neutral_probability: float
    expected_risk: float
    opportunity_grade: str
    institutional_confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
