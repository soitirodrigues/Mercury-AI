from dataclasses import dataclass, field
from typing import Dict, Any
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME
from mercury_ai.utils.deterministic_clock import DeterministicClock

@dataclass(frozen=True)
class Evidence:
    engine_name: str
    evidence_name: str
    direction: str  # BULLISH / BEARISH / NEUTRAL
    strength: float # 0-100
    confidence: float # 0-100
    description: str
    weight: float
    contribution_score: float = 0.0
    quality_score: float = 100.0
    context_score: float = 100.0
    timeframe: str = DEFAULT_TIMEFRAME
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
