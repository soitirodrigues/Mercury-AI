from dataclasses import dataclass
from typing import List

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.price_action import PriceActionAnalysis
from mercury_ai.models.support_resistance import SupportResistanceAnalysis
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.market_state import MarketState
from mercury_ai.models.liquidity_profile import LiquidityProfile
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.risk_assessment import RiskAssessment


@dataclass(frozen=True)
class MarketContext:

    market: MarketData

    trend: List[Evidence]

    price_action: PriceActionAnalysis

    support_resistance: SupportResistanceAnalysis

    smart_money: SmartMoneyAnalysis

    liquidity: LiquidityProfile

    market_state: MarketState

    market_regime: MarketRegime

    mtf_consensus: MTFConsensus

    risk_assessment: RiskAssessment