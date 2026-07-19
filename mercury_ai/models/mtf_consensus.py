from dataclasses import dataclass

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
