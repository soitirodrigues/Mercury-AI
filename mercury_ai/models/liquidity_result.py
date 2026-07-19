from dataclasses import dataclass
from typing import Tuple, Any

@dataclass(frozen=True)
class LiquidityResult:
    evidences: Tuple[Any, ...]
    score: float
    confidence: float
    strength: float
    metadata: dict
