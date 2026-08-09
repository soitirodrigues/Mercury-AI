from dataclasses import dataclass, field
from typing import Tuple, Optional

@dataclass(frozen=True)
class TradePermission:
    status: Optional[str] = None
    confidence: Optional[float] = None
    reasons: Tuple[str, ...] = field(default_factory=tuple)
