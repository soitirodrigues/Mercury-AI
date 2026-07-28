import pandas as pd
import numpy as np
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.data.providers.historical_data_provider import HistoricalDataProvider

def test_session_id_consistency():
    # Setup with deterministic mock data
    periods = 200
    np.random.seed(42)
    data = {
        'Close': np.random.randn(periods).cumsum() + 100,
        'High': np.random.randn(periods).cumsum() + 101,
        'Low': np.random.randn(periods).cumsum() + 99,
        'Open': np.random.randn(periods).cumsum() + 100,
        'Volume': np.random.randint(1000, 5000, periods)
    }
    df = pd.DataFrame(data, index=pd.date_range('2025-01-01', periods=periods, freq='5min'))
    provider = HistoricalDataProvider(df)
    pipeline = AnalysisPipeline(
        market_service=MarketDataService(providers=[provider]),
        providers=[provider]
    )
    
    # Analyze multiple symbols in the same session
    symbol1 = "ASSET-A"
    symbol2 = "ASSET-B"
    
    res1 = pipeline.analyze(symbol1)
    res2 = pipeline.analyze(symbol2)
    
    # Get snapshots from memory
    snap1 = pipeline.last_snapshots[symbol1]
    snap2 = pipeline.last_snapshots[symbol2]
    
    # Session IDs must be identical
    assert snap1.session_id == snap2.session_id
    assert snap1.session_id == pipeline.session_id
