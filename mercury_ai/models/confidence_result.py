from dataclasses import dataclass

@dataclass(frozen=True)
class ConfidenceResult:
    confidence_score: float
    confidence_grade: str # A, B, C, D
    is_high: bool
