from dataclasses import dataclass, field
from typing import Tuple, Dict, Any

@dataclass(frozen=True)
class PriceActionAnalysis:
    engine_name: str = "PriceActionEngine"
    is_strong_candle: bool = False
    is_weak_candle: bool = False
    is_engulfing: bool = False
    is_pin_bar: bool = False
    is_inside_bar: bool = False
    is_outside_bar: bool = False
    is_false_breakout: bool = False
    is_pullback: bool = False
    is_rejection: bool = False
    is_continuation: bool = False
    is_exhaustion: bool = False
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Any, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
