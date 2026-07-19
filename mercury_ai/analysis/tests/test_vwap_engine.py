import pytest
import pandas as pd
from mercury_ai.analysis.vwap_engine import VWAPEngine
from mercury_ai.models.vwap_analysis import VWAPAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def vwap_engine():
    return VWAPEngine(PipelineExecutor())

def test_vwap_engine_calculation(vwap_engine):
    data = {
        "Open": [10, 11],
        "High": [12, 13],
        "Low": [8, 9],
        "Close": [11, 12],
        "Volume": [100, 100]
    }
    df = pd.DataFrame(data)
    analysis = vwap_engine.analyze(df)
    
    assert isinstance(analysis, VWAPAnalysis)
    assert analysis.vwap > 0
    assert analysis.institutional_bias == "BULLISH"
