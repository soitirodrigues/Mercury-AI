from dataclasses import dataclass, field
from typing import List


@dataclass
class Recommendation:
    """
    Resultado produzido pelo Mercury Brain.
    """

    decision: str

    confidence: float

    score: float

    strategy: str

    evidences: List[str] = field(default_factory=list)

    explanation: str = ""