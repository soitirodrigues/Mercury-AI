from dataclasses import dataclass, field
from typing import Tuple
from enum import Enum
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.config import settings

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.market_condition import MarketCondition
from mercury_ai.models.market_state import MarketState
from mercury_ai.models.candlestick_analysis import CandlestickAnalysis
from mercury_ai.models.volatility_analysis import VolatilityAnalysis
from mercury_ai.models.session_analysis import SessionAnalysis
from mercury_ai.models.support_resistance import SupportResistanceAnalysis
from mercury_ai.models.liquidity_result import LiquidityResult
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.volume_analysis import VolumeAnalysis
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.models.decision_result import DecisionResult

# AnalysisDirection moved to direction.py to avoid circular imports

@dataclass(frozen=True)
class AnalysisResult:
    market: MarketData
    context: MarketContext
    trend: Tuple[Evidence, ...]
    mtf_evidences: Tuple[Evidence, ...]
    smart_money: SmartMoneyAnalysis
    market_regime: MarketRegime
    confluence: ConfluenceResult
    market_condition: MarketCondition
    market_state: MarketState
    candlestick_analysis: CandlestickAnalysis
    volatility_analysis: VolatilityAnalysis
    session_analysis: SessionAnalysis
    support_resistance: SupportResistanceAnalysis
    liquidity_analysis: LiquidityResult
    risk_assessment: RiskAssessment
    evidence_ranking: EvidenceRankingResult
    volume_analysis: VolumeAnalysis
    structure_analysis: MarketStructureProfile
    decision: DecisionResult
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())
    version: str = field(default_factory=lambda: settings.VERSION)
