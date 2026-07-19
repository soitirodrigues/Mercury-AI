import pytest
import pandas as pd
from mercury_ai.analysis.fair_value_gap_engine import FairValueGapEngine
from mercury_ai.models.fair_value_gap_analysis import FairValueGapAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def fvg_engine():
    return FairValueGapEngine(PipelineExecutor())

def test_fvg_engine_bullish(fvg_engine):
    data = {
        "Open": [10, 10, 10],
        "High": [12, 12, 14],
        "Low": [8, 8, 13],
        "Close": [11, 11, 13],
        "Volume": [100, 100, 100]
    }
    # C1 High: 12, C3 Low: 13 -> Bullish FVG
    df = pd.DataFrame(data)
    analysis = fvg_engine.analyze(df)
    
    assert isinstance(analysis, FairValueGapAnalysis)
    assert analysis.is_bullish_fvg is True
    assert analysis.is_open is True
    assert len(analysis.evidences) == 1
