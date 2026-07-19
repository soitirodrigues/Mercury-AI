import pytest
import pandas as pd
import numpy as np
from typing import List
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data_provider import MarketDataProvider
from mercury_ai.data.market_data import MarketDataService

class RobustnessMarketDataProvider(MarketDataProvider):
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        return self.df
    
    def is_available(self) -> bool:
        return True
    
    def supports_symbol(self, symbol: str) -> bool:
        return True
    
    def source_name(self) -> str:
        return "RobustnessTest"

def test_pipeline_robustness():
    provider = RobustnessMarketDataProvider(pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"]))
    pipeline = AnalysisPipeline(market_service=MarketDataService(providers=[provider]), providers=[provider])
    
    # Scenarios: (DataFrame, expects_error)
    scenarios = [
        (pd.DataFrame(columns=["Open", "High", "Low", "Close", "Volume"], index=pd.to_datetime([])), True), # Empty
        (pd.DataFrame({"Open": [10], "High": [np.nan], "Low": [10], "Close": [10], "Volume": [10]}, index=pd.to_datetime(['2025-01-01'])), True), # NaN
        (pd.DataFrame({"Open": [10], "High": [11], "Low": [9], "Close": [10], "Volume": [0]}, index=pd.to_datetime(['2025-01-01'])), False), # Zero Volume
    ]
    
    for df, expects_error in scenarios:
        provider = RobustnessMarketDataProvider(df)
        pipeline.market_service = MarketDataService(providers=[provider])
        
        # Pipeline should not crash
        try:
            result = pipeline.analyze("TEST")
            # Snapshot should contain the warning
            snapshot = pipeline.last_snapshot
            if expects_error:
                assert "Data quality issue detected" in snapshot.audit_events
            else:
                assert "Data quality issue detected" not in snapshot.audit_events
        except Exception as e:
            pytest.fail(f"Pipeline crashed on robust test: {e}")
