import pytest
import pandas as pd
from mercury_ai.analysis.volume_engine import VolumeEngine
from mercury_ai.models.volume_analysis import VolumeAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def volume_engine():
    return VolumeEngine(PipelineExecutor())

def test_volume_engine_spike(volume_engine):
    # Create 20 candles with low volume, then a spike
    volumes = [100] * 19 + [300]
    data = {
        "Open": [10] * 20,
        "High": [12] * 20,
        "Low": [8] * 20,
        "Close": [11] * 20,
        "Volume": volumes
    }
    df = pd.DataFrame(data)
    analysis = volume_engine.analyze(df)
    
    assert isinstance(analysis, VolumeAnalysis)
    assert analysis.is_volume_spike is True
    assert analysis.relative_volume > 2.0
    assert len(analysis.evidences) == 1
