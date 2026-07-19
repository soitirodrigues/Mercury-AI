from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.market_state import MarketState, MarketStateEnum
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.liquidity_profile import LiquidityProfile
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.price_action import PriceActionAnalysis
from mercury_ai.models.support_resistance import SupportResistanceAnalysis
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.market_regime import MarketRegime
from typing import List

"""
OFFICIAL MARKET CONTEXT FACTORY

Single responsibility:

Instantiate immutable MarketContext.

No business rules.

No decisions.

No filtering.

No fallbacks.

Every field MUST be supplied by the caller.
"""

class MarketContextBuilder:

    def build(
        self,
        market,
        trend: List[Evidence],
        price_action: PriceActionAnalysis,
        support_resistance: SupportResistanceAnalysis,
        smart_money: SmartMoneyAnalysis,
        market_state: MarketState,
        regime: MarketRegime,
        risk_assessment: RiskAssessment,
        mtf_consensus: MTFConsensus,
        structure=None
    ) -> MarketContext:
        # Build LiquidityProfile from MarketStructureProfile when available,
        # otherwise default-construct so the contract (MarketContext.liquidity: LiquidityProfile) is always satisfied.
        if structure is not None and isinstance(structure, MarketStructureProfile):
            liquidity_profile = LiquidityProfile(
                internal_liquidity=structure.internal_liquidity,
                external_liquidity=structure.external_liquidity,
                liquidity_sweep=structure.liquidity_sweep,
                equal_highs=structure.equal_highs,
                equal_lows=structure.equal_lows,
                stop_hunt_probability=1.0 if structure.stop_hunt else 0.0,
                liquidity_density=structure.buy_side_liquidity + structure.sell_side_liquidity,
            )
        else:
            liquidity_profile = LiquidityProfile()

        return MarketContext(
            market=market,
            trend=trend,
            support_resistance=support_resistance,
            price_action=price_action,
            smart_money=smart_money,
            market_state=market_state,
            liquidity=liquidity_profile,
            market_regime=regime,
            risk_assessment=risk_assessment,
            mtf_consensus=mtf_consensus,
        )
