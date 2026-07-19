from dataclasses import dataclass, field
from typing import List
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.market_state import MarketState

@dataclass(frozen=True)
class MarketThesis:
    market_bias: str
    confluence_score: float
    confidence: ConfidenceResult
    risk: RiskAssessment
    market_state: MarketState
    confirmations: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    institutional_alignment: bool = False
    opportunity_grade: str = "C"
