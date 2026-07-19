from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass(frozen=True)
class ProfessionalThesis:
    market_bias: str
    opportunity_grade: str
    confidence: int
    institutional_alignment: bool
    confirmations: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    risk_factors: List[str] = field(default_factory=list)
    summary: str = ""
    full_report: str = ""
    decision_tree: Dict[str, Any] = field(default_factory=dict)
