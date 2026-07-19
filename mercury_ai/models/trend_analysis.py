from dataclasses import dataclass, field
from typing import Tuple, Dict, Any

@dataclass(frozen=True)
class TrendAnalysis:
    engine_name: str = "TrendEngine"
    is_hh_hl: bool = False
    is_lh_ll: bool = False
    ema20: float = 0.0
    ema50: float = 0.0
    ema200: float = 0.0
    adx: float = 0.0
    trend_strength: float = 0.0
    trend_quality: float = 0.0
    trend_confidence: float = 0.0
    is_consolidation: bool = False
    is_expansion: bool = False
    evidences: Tuple[Any, ...] = field(default_factory=tuple)
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
