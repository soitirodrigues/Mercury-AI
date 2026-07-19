from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.market_state import MarketState, MarketStateEnum
from mercury_ai.models.mtf_consensus import MTFConsensus

"""
OFFICIAL MARKET CONTEXT FACTORY

Single responsibility:

Instantiate immutable MarketContext.

No business rules.

No decisions.

No filtering.
"""

class MarketContextBuilder:

    def __init__(self, trend, sr, price_action, liquidity, smart_money, fvg, ob, regime):
        self.trend = trend
        self.support_resistance = sr
        self.price_action = price_action
        self.liquidity = liquidity
        self.smart_money = smart_money
        self.fvg = fvg
        self.ob = ob
        self.regime_engine = regime

    def build(self, dataframe, market, smart_money=None, market_state=None, liquidity=None, regime=None, risk_assessment=None, mtf_consensus=None) -> MarketContext:
        return MarketContext(
            market=market,
            trend=self.trend.analyze(market),
            support_resistance=self.support_resistance.analyze(dataframe),
            price_action=self.price_action.analyze(dataframe),
            smart_money=smart_money if smart_money is not None else self.smart_money.analyze(dataframe, [], None),
            market_state=market_state if market_state is not None else MarketState(state=MarketStateEnum.UNKNOWN, confidence=0.0),
            liquidity=liquidity if liquidity is not None else self.liquidity.analyze(dataframe, [], None),
            market_regime=regime if regime is not None else self.regime_engine.analyze(market, smart_money, None, None),
            risk_assessment=risk_assessment if risk_assessment is not None else RiskAssessment(
                suggested_stop=0.0, suggested_take_profit=0.0, risk_reward_ratio=0.0,
                expected_drawdown=0.0, expected_volatility=0.0, trade_quality=0.0,
                max_exposure=0.0, invalidation_point=0.0, institutional_risk_score=0.0
            ),
            mtf_consensus=mtf_consensus if mtf_consensus is not None else MTFConsensus(
                global_bias="NEUTRAL", local_bias="NEUTRAL", conflict_detected=False, 
                alignment_score=0.0, dominant_trend="NEUTRAL", institutional_consensus_strength=0.0, summary="No MTF data"
            )
        )
