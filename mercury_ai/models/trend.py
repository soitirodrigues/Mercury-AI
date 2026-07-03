from dataclasses import dataclass


@dataclass
class TrendAnalysis:

    trend: str
    confidence: int
    explanation: list[str]