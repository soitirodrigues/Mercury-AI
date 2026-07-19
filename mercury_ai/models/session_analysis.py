from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SessionAnalysis:
    session: Optional[str] = None
    overlap: Optional[bool] = None
    quality: Optional[float] = None
    liquidity_score: Optional[float] = None
    explanation: Optional[str] = None
