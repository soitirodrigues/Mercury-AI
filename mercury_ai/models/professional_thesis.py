from dataclasses import dataclass, field
from typing import Tuple, Dict, Any

@dataclass(frozen=True)
class ProfessionalThesis:
    market_bias: str
    opportunity_grade: str
    confidence: int
    institutional_alignment: bool
    confirmations: Tuple[str, ...] = field(default_factory=tuple)
    conflicts: Tuple[str, ...] = field(default_factory=tuple)
    risk_factors: Tuple[str, ...] = field(default_factory=tuple)
    summary: str = ""
    full_report: str = ""
    decision_tree: Dict[str, Any] = field(default_factory=dict)
