import pytest
import pandas as pd
from mercury_ai.analysis.price_action_engine import PriceActionEngine
from mercury_ai.models.price_action_analysis import PriceActionAnalysis
from mercury_ai.core.pipeline_executor import PipelineExecutor

@pytest.fixture
def price_action_engine():
    return PriceActionEngine(PipelineExecutor())

def test_price_action_engine_engulfing(price_action_engine):
    # Candle 1: Open 12, Close 11 (Bearish) - Body [11, 12]
    # Candle 2: Open 10, Close 13 (Bullish) - Body [10, 13] - Engulfs Candle 1
    data = {
        "Open": [12, 10],
        "High": [14, 15],
        "Low": [10, 8],
        "Close": [11, 13],
        "Volume": [100, 100]
    }
    df = pd.DataFrame(data)
    analysis = price_action_engine.analyze(df)
    
    assert isinstance(analysis, PriceActionAnalysis)
    assert analysis.is_engulfing is True
