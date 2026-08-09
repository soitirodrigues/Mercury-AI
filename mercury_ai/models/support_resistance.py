from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SupportResistanceAnalysis:

    support: float
    resistance: float
    distance_support: float
    distance_resistance: float
    explanation: Tuple[str, ...]