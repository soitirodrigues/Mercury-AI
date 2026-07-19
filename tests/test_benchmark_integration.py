import pytest
import pandas as pd
from typing import List, Tuple
from mercury_ai.analysis.smart_money.liquidity_engine import LiquidityEngine, EqualHighGroup
from mercury_ai.models.swing_analysis import Swing
from mercury_ai.models.market_structure_profile import MarketStructureProfile
from mercury_ai.core.pipeline_profiler import PipelineProfiler

def create_mock_swing(price, index, timestamp, strength=0.8, atr=1.0, type='HIGH', confirmed=True):
    return Swing(
        type=type,
        classification='HH',
        price=price,
        timestamp=timestamp,
        index=index,
        atr=atr,
        strength=strength,
        volume=100.0,
        confirmed=confirmed
    )

def test_external_benchmark_run():
    engine = LiquidityEngine()
    swings = [
        create_mock_swing(100.0, 1, "T1"),
        create_mock_swing(100.2, 5, "T2")
    ]
    df = pd.DataFrame()
    profile = MarketStructureProfile()
    profiler = PipelineProfiler("LiquidityEnginePipeline")
    
    # Run pipeline externally, instrumented by the profiler
    profiler.start_pipeline()
    analysis, evidences, updated_profile = engine.analyze_tuple(df, swings, profile, profiler=profiler)
    profiler.end_pipeline()
        
    pipeline_profile = profiler.summary()
    
    assert analysis.has_equal_highs is True
    assert len(pipeline_profile.stage_profiles) >= 1
    assert pipeline_profile.total_duration > 0
