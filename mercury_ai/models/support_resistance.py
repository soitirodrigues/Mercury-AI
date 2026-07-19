from dataclasses import dataclass


@dataclass(frozen=True)
class SupportResistanceAnalysis:

    support: float
    resistance: float
    distance_support: float
    distance_resistance: float
    explanation: list[str]