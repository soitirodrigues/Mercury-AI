from dataclasses import dataclass, field
from typing import Tuple, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from mercury_ai.models.decision_result import DecisionResult

@dataclass(frozen=True)
class TradingExplanation:
    exec_summary: str
    decision_rationale: str
    market_context: str
    trend_context: str
    liquidity_context: str
    structure_context: str
    momentum_context: str
    volume_context: str
    smart_money_context: str
    confluence_context: str
    risk_assessment: str
    confidence_rationale: str
    strong_evidences: Tuple[str, ...] = ()
    weak_evidences: Tuple[str, ...] = ()
    missing_confirmations: Tuple[str, ...] = ()
    detected_risks: Tuple[str, ...] = ()
    bullish_factors: Tuple[str, ...] = ()
    bearish_factors: Tuple[str, ...] = ()
    neutral_factors: Tuple[str, ...] = ()
    conflicts: Tuple[str, ...] = ()
    logical_sequence: Tuple[str, ...] = ()
    risk_analysis: str = ""
    institutional_context: str = ""
    suggested_entry: Any = None
    suggested_stop: Any = None
    suggested_targets: Tuple[Any, ...] = ()
    confidence_explanation: str = ""
    machine_readable: Dict[str, Any] = field(default_factory=dict)
    engine_weights: Dict[str, float] = field(default_factory=dict)
    warnings: Tuple[str, ...] = ()
