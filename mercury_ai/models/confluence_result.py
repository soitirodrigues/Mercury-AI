from dataclasses import dataclass
from typing import Tuple, Any
from mercury_ai.models.analysis_result import AnalysisDirection

@dataclass(frozen=True)
class ConfluenceResult:
    buy_score: float
    sell_score: float
    neutral_score: float
    agreement_percentage: float
    conflicting_signals: bool
    independent_confirmations: int
    weighted_score: float
    confidence: float
    dominant_direction: AnalysisDirection
    evidences: Tuple[Any, ...]
    warnings: Tuple[str, ...]
