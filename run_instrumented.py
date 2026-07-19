from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
import pandas as pd

class MockProvider:
    def get_data(self, *args, **kwargs):
        return pd.DataFrame({'Open': [10], 'High': [11], 'Low': [9], 'Close': [10], 'Volume': [10]}, index=pd.to_datetime(['2025-01-01']))
    def is_available(self): return True
    def supports_symbol(self, *args): return True
    def supports_market(self, *args): return True
    def supports_timeframe(self, *args): return True
    def max_history(self): return '1000y'
    def source_name(self): return 'Mock'

if __name__ == '__main__':
    pipeline = AnalysisPipeline(MarketDataService(providers=[MockProvider()]), providers=[MockProvider()])
    pipeline.analyze('GC=F')
