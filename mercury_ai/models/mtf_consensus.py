from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class MTFConsensus:
    global_bias: str
    local_bias: str
    conflict_detected: bool
    alignment_score: float
    conflict_score: float = 0.0
    trend_alignment: float = 0.0
    liquidity_alignment: float = 0.0
    structure_alignment: float = 0.0
    volatility_alignment: float = 0.0
    dominant_trend: str = "NEUTRAL"
    institutional_consensus_strength: float = 0.0
    summary: str = ""
    # Observabilidade: status por timeframe (processed/rejected/absent/invalid/error).
    # NÃO altera fórmulas de consenso — apenas registra explicitamente a presença
    # ou ausência de cada timeframe na análise.
    timeframe_status: Dict[str, str] = field(default_factory=dict)
    timeframe_errors: Dict[str, str] = field(default_factory=dict)
