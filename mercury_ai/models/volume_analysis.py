from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class VolumeAnalysis:
    engine_name: str = "VolumeEngine"
    relative_volume: float = 0.0
    is_volume_spike: bool = False
    is_absorption: bool = False
    is_distribution: bool = False
    is_accumulation: bool = False
    is_climax: bool = False
    volume_trend: str = "NEUTRAL" # INCREASING, DECREASING, NEUTRAL
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Evidence, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
