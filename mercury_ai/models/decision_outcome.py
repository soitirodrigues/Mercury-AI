from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class DecisionOutcome:
    audit_id: str
    outcome: float # PnL or binary success/fail
    timestamp: str
    meta: Dict[str, Any]
