from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class FairValueGapAnalysis:
    engine_name: str = "FairValueGapEngine"
    is_bullish_fvg: bool = False
    is_bearish_fvg: bool = False
    is_filled: bool = False
    is_open: bool = False
    fvg_quality: float = 0.0
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Evidence, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
