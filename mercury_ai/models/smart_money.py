from dataclasses import dataclass, field

from mercury_ai.models.market_structure import MarketStructure


@dataclass(frozen=True)
class SmartMoneyAnalysis:

    structure: MarketStructure

    score: int = 0
    confidence: int = 0
    institutional_score: float = 0.0
    explanation: list[str] = field(default_factory=list)