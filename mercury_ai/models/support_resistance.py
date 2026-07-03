from dataclasses import dataclass


@dataclass
class SupportResistanceAnalysis:

    support: float
    resistance: float
    distance_support: float
    distance_resistance: float
    explanation: list[str]