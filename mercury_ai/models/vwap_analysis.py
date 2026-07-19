from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class VWAPAnalysis:
    engine_name: str = "VWAPEngine"
    vwap: float = 0.0
    distance_to_vwap: float = 0.0
    is_accepted: bool = False
    is_rejected: bool = False
    is_mean_reversion: bool = False
    institutional_bias: str = "NEUTRAL" # BULLISH, BEARISH, NEUTRAL
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Evidence, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
