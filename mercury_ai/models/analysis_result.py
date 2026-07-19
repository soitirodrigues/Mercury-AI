from dataclasses import dataclass, field
from typing import Any, List
from enum import Enum
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.config import settings

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.smart_money import SmartMoneyAnalysis

class AnalysisDirection(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NEUTRAL = "NEUTRAL"

@dataclass(frozen=True)
class AnalysisResult:
    market: MarketData
    context: MarketContext
    trend: List[Evidence]
    mtf_evidences: List[Evidence]
    smart_money: SmartMoneyAnalysis
    market_regime: Any
    confluence: Any
    market_condition: Any
    market_state: Any
    candlestick_analysis: Any
    volatility_analysis: Any
    session_analysis: Any
    support_resistance: Any
    liquidity_analysis: Any
    risk_assessment: Any
    evidence_ranking: Any
    volume_analysis: Any
    structure_analysis: Any
    decision: Any
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())
    version: str = field(default_factory=lambda: settings.VERSION)
