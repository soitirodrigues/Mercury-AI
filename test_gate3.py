import sys
sys.path.insert(0, '.')
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from datetime import datetime
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.providers.yahoo_finance_provider import YahooFinanceProvider

# Reset clock to ensure deterministic behavior
DeterministicClock.set_time(datetime(2025, 1, 1, 9, 30, 0))

# Create mock provider - directly mock the get_data method
mock = MagicMock()

# Create synthetic OHLCV data
rng = np.random.RandomState(42)
dates = pd.date_range('2024-01-01', periods=100, freq='5min')
base = 50000.0
close = base * (1.0 + rng.randn(100).cumsum() * 0.001)
high = close * (1 + rng.rand(100) * 0.002)
low = close * (1 - rng.rand(100) * 0.002)
op = close * (1 + rng.rand(100) * 0.001)
volume = rng.randint(100, 10000, size=100).astype(float)
df = pd.DataFrame(
    {'Open': op, 'High': high, 'Low': low, 'Close': close, 'Volume': volume},
    index=dates,
)
df.index.name = 'Datetime'

# Create MarketDataService directly with the mock provider
# Instead of using YahooFinanceProvider patch
from mercury_ai.data.market_data import MarketDataService

# Create a simple provider class that wraps our mock
class TestProvider:
    def __init__(self, mock_obj):
        self.mock = mock_obj
    
    def get_data(self, symbol, interval='5m', period='1y'):
        return self.mock.get_data(symbol, interval, period)
    
    def is_available(self):
        return self.mock.is_available()
    
    def supports_symbol(self, symbol):
        return self.mock.supports_symbol(symbol)
    
    def supports_market(self, market):
        return self.mock.supports_market(market)
    
    def supports_timeframe(self, symbol, timeframe):
        return self.mock.supports_timeframe(symbol, timeframe)
    
    def max_history(self):
        return self.mock.max_history()
    
    @property
    def source_name(self):
        return self.mock.source_name

# Create service with our test provider - pass via providers list
service = MarketDataService(providers=[TestProvider(mock)])

# Create pipeline
pipeline = AnalysisPipeline(market_service=service, providers=[])

# Run analysis for BTC
result = pipeline.analyze(symbol='BTC-USD', silent=True)

print('\n=== RESULT ===')
print(f'Decision: {result.decision}')
print(f'Grade: {result.grade}')
print(f'Explanation: {result.explanation}')
print(f'\nDecision type: {type(result.decision)}')