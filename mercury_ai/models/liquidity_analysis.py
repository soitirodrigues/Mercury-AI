from dataclasses import dataclass, field
from typing import Tuple, Dict, Any
from mercury_ai.models.evidence import Evidence

@dataclass(frozen=True)
class LiquidityAnalysis:
    engine_name: str = "LiquidityEngine"
    has_equal_highs: bool = False
    has_equal_lows: bool = False
    has_liquidity_sweep: bool = False
    has_stop_hunt: bool = False
    has_liquidity_void: bool = False
    is_premium: bool = False
    is_discount: bool = False
    confidence: float = 0.0
    quality: float = 0.0
    evidences: Tuple[Evidence, ...] = field(default_factory=tuple)
    metadata: Dict[str, Any] = field(default_factory=dict)
