from dataclasses import dataclass, field
from typing import Optional, Tuple

@dataclass(frozen=True)
class CandlestickAnalysis:
    pattern: Optional[str] = None
    body_strength: Optional[float] = None
    upper_wick: Optional[float] = None
    lower_wick: Optional[float] = None
    rejection: Optional[bool] = None
    engulfing: Optional[bool] = None
    continuation: Optional[bool] = None
    explanation: Optional[str] = None
    context: Optional[str] = None
    context_score: Optional[float] = None
    evidences: Tuple[str, ...] = field(default_factory=tuple)

