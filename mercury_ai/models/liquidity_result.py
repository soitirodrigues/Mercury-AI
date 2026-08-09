from dataclasses import dataclass, field
from typing import Tuple, Any, Dict

@dataclass(frozen=True)
class LiquidityResult:
    evidences: Tuple[Any, ...]
    score: float
    confidence: float
    strength: float
    metadata: Dict[str, Any] = field(default_factory=dict)
