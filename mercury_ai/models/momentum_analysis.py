from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class MomentumAnalysis:
    engine_name: str = "MomentumEngine"
    rsi: float = 0.0
    macd: float = 0.0
    macd_signal: float = 0.0
    roc: float = 0.0
    strength: float = 0.0
    is_divergence: bool = False
    is_exhaustion: bool = False
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Evidence, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
