from dataclasses import dataclass
from typing import Tuple, Dict, Any
from mercury_ai.models.decision_snapshot import DecisionSnapshot

@dataclass(frozen=True)
class TradeMemory:
    timestamp: str
    context_snapshot: Dict[str, Any]
    evidences: Tuple[str, ...]
    decision: str
    result: str # BUY_CORRETO, etc.
    mae: float
    mfe: float
    drawdown: float
    profit: float
    time_to_close: float
    session: str
    regime: str
