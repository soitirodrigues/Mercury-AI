import pytest
import pandas as pd
import numpy as np
from mercury_ai.analysis.momentum_engine import MomentumEngine
from mercury_ai.models.momentum_analysis import MomentumAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def momentum_engine():
    return MomentumEngine(PipelineExecutor())

def test_momentum_engine_rsi_oversold(momentum_engine):
    # Create 30 candles with downward trend
    closes = np.linspace(100, 50, 30)
    data = {
        "Open": closes,
        "High": closes + 1,
        "Low": closes - 1,
        "Close": closes,
        "Volume": [100] * 30
    }
    df = pd.DataFrame(data)
    analysis = momentum_engine.analyze(df)
    
    assert isinstance(analysis, MomentumAnalysis)
    assert analysis.rsi < 30
    assert any(e.evidence_name == "Exhaustion" for e in analysis.evidences)
