import pytest
from pathlib import Path
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
import shutil
import pandas as pd
import numpy as np
from mercury_ai.data.providers.historical_data_provider import HistoricalDataProvider
from mercury_ai.data.market_data import MarketDataService

def test_pipeline_snapshot_persistence():
    # Setup - clean both snapshot dir and institutional memory
    snapshot_dir = Path("mercury_ai/database/snapshots")
    if snapshot_dir.exists():
        shutil.rmtree(snapshot_dir, ignore_errors=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    
    # Clean corrupted institutional memory
    import json
    memory_file = Path("data/institutional_memory.json")
    if memory_file.exists():
        memory_file.unlink()
    
    # Minimal mock data
    periods = 100
    data = {
        'Close': np.random.randn(periods).cumsum() + 100,
        'High': np.random.randn(periods).cumsum() + 101,
        'Low': np.random.randn(periods).cumsum() + 99,
        'Open': np.random.randn(periods).cumsum() + 100,
        'Volume': np.random.randint(1000, 5000, periods)
    }
    df = pd.DataFrame(data, index=pd.date_range('2025-01-01', periods=periods, freq='5min'))
    provider = HistoricalDataProvider(df)
    
    pipeline = AnalysisPipeline(market_service=MarketDataService(providers=[provider]), providers=[provider])
    
    # Run analysis for a symbol
    pipeline.analyze("EURUSD=X")
    
    # Verify snapshot file exists
    snapshots = list(snapshot_dir.glob("*.json"))
    assert len(snapshots) > 0
