from dataclasses import dataclass, field
from typing import Tuple, Optional
from mercury_ai.models.decision_trace import DecisionTrace
from mercury_ai.models.version_metadata import VersionMetadata
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.evidence_ranking import EvidenceRankingResult

@dataclass(frozen=True)
class DecisionResult:
    decision: str
    grade: str
    confidence: float
    clarity: float
    risk_score: float
    score: float
    quality: float
    expected_strength: float
    buy_probability: float
    sell_probability: float
    wait_probability: float
    expected_risk: float
    expected_reward: float
    expected_drawdown: float
    audit_id: str
    version_metadata: VersionMetadata
    explanation: TradingExplanation
    mtf_consensus: Optional[MTFConsensus] = None
    market_regime: Optional[MarketRegime] = None
    trade_allowed: bool = True
    trade_block_reasons: Tuple[str, ...] = field(default_factory=tuple)
    trade_quality_score: float = 0.0
    trade_quality_level: str = "N/A"
    trace: Optional[DecisionTrace] = None
    warnings: Tuple[str, ...] = field(default_factory=tuple)
    weaknesses: Tuple[str, ...] = field(default_factory=tuple)
    blockers: Tuple[str, ...] = field(default_factory=tuple)
    summary: str = ""
    technical_reason: str = ""
    institutional_alignment: bool = False
    evidence_ranking: Optional[EvidenceRankingResult] = None
