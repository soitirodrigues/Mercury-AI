from dataclasses import dataclass
from typing import Mapping, Any

@dataclass(frozen=True)
class DecisionOutcome:
    audit_id: str
    outcome: float # PnL or binary success/fail
    timestamp: str
    meta: Mapping[str, Any]
