from dataclasses import dataclass
from typing import Tuple, Optional, Mapping
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class EvidenceRankingResult:
    ranked_evidences: Tuple[Evidence, ...]
    contribution_percentage: Mapping[str, float]
    strongest_evidence: Evidence
    weakest_evidence: Evidence
    total_weight: float
    bullish_weight: float
    bearish_weight: float
    neutral_weight: float
    bullish_score: float
    bearish_score: float
    neutral_score: float
    top_bullish_evidence: Optional[Evidence] = None
    top_bearish_evidence: Optional[Evidence] = None
    top_neutral_evidence: Optional[Evidence] = None
