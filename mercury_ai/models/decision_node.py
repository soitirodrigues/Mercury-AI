from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DecisionNode:
    engine: str
    evidence: str
    weight: float
    score: float
    influence: str
    result: str
