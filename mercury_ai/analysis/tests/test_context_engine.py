from unittest.mock import Mock, MagicMock
from mercury_ai.analysis.context_engine import ContextEngine
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.price_action import PriceActionAnalysis
from mercury_ai.models.support_resistance import SupportResistanceAnalysis
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.market_state import MarketState
from mercury_ai.models.market_state_enum import MarketStateEnum
from mercury_ai.models.liquidity_profile import LiquidityProfile
from mercury_ai.models.mtf_consensus import MTFConsensus
from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.market_regime_enum import MarketRegimeEnum
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.market_structure import MarketStructure

def test_context_engine_aggregation():
    executor = PipelineExecutor()
    profiler = Mock(spec=PipelineProfiler)
    engine = ContextEngine(executor, profiler)
    
    evidences = [
        Evidence("Engine1", "E1", "BULLISH", 10.0, 10.0, "Desc", 1.0),
        Evidence("Engine1", "E1", "BULLISH", 10.0, 10.0, "Desc", 1.0), # Duplicate
        Evidence("Engine2", "E2", "BEARISH", 20.0, 20.0, "Desc", 1.0)
    ]
    
    market_data = Mock(spec=MarketData)
    
    ctx = MarketContext(
        market=market_data,
        trend=[],
        price_action=PriceActionAnalysis(
            trend_structure="BULLISH",
            last_event="BOS",
            confidence=80,
            explanation=["Strong bullish structure"]
        ),
        support_resistance=SupportResistanceAnalysis(
            support=95.0,
            resistance=105.0,
            distance_support=5.0,
            distance_resistance=5.0,
            explanation=["Key levels identified"]
        ),
        smart_money=SmartMoneyAnalysis(
            structure=MarketStructure(
                trend="BULLISH",
                higher_high=True,
                higher_low=True,
                confidence=75,
                explanation=["Bullish structure"]
            ),
            score=70,
            confidence=75,
            institutional_score=0.7,
            explanation=["Smart money aligned"]
        ),
        liquidity=LiquidityProfile(
            internal_liquidity=0.6,
            external_liquidity=0.4,
            liquidity_sweep=False,
            equal_highs=False,
            equal_lows=False,
            stop_hunt_probability=0.1,
            liquidity_density=0.5
        ),
        market_state=MarketState(
            state=MarketStateEnum.TRENDING,
            explanation="Market is trending"
        ),
        market_regime=MarketRegime(
            regime=MarketRegimeEnum.UNKNOWN,
            confidence=0.5,
            supporting_evidences=[]
        ),
        mtf_consensus=MTFConsensus(
            global_bias="BULLISH",
            local_bias="BULLISH",
            conflict_detected=False,
            alignment_score=80.0,
            conflict_score=0.0,
            trend_alignment=0.8,
            liquidity_alignment=0.7,
            structure_alignment=0.9,
            volatility_alignment=0.6,
            dominant_trend="BULLISH",
            institutional_consensus_strength=0.75,
            summary="Aligned bullish"
        ),
        risk_assessment=RiskAssessment(
            suggested_stop=95.0,
            suggested_take_profit=110.0,
            risk_reward_ratio=2.0,
            expected_drawdown=0.02,
            expected_volatility=0.15,
            trade_quality=0.8,
            max_exposure=0.05,
            invalidation_point=94.0,
            institutional_risk_score=0.2
        ),
    )
    context = engine.analyze(ctx, evidences)
    
    assert context is not None
