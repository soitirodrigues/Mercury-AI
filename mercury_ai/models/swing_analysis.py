from dataclasses import dataclass, field
from typing import Tuple, Optional

@dataclass(frozen=True)
class Swing:
    type: str  # 'HIGH' or 'LOW'
    classification: str  # 'HH', 'HL', 'LH', 'LL'
    price: float
    timestamp: str
    index: int
    atr: float
    strength: float
    volume: float
    confirmed: bool = True
    distance_from_previous: float = 0.0

@dataclass(frozen=True)
class SwingSequenceResult:
    current_swing: Optional[Swing] = None
    previous_swing: Optional[Swing] = None
    sequence: Tuple[str, ...] = field(default_factory=tuple)
    sequence_length: int = 0
    sequence_quality: float = 0.0
    sequence_confidence: float = 0.0
    trend_direction: str = "NEUTRAL"
    trend_transition: bool = False
