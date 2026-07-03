from dataclasses import dataclass


@dataclass
class PriceActionAnalysis:

    trend_structure: str
    last_event: str
    confidence: int
    explanation: list[str]