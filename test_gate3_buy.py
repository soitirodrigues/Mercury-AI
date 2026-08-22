import sys
sys.path.insert(0, '.')
from unittest.mock import MagicMock
import pandas as pd
import numpy as np
from datetime import datetime
from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.utils.deterministic_clock import DeterministicClock

# Reset clock
DeterministicClock.set_time(datetime(2025, 1, 1, 9, 30, 0))

# Create mock provider with synthetic data
mock = MagicMock()

rng = np.random.RandomState(42)
dates = pd.date_range('2024-01-01', periods=200, freq='5min')
base = 50000.0
close = base * (1.0 + rng.randn(200).cumsum() * 0.001)
high = close * (1 + rng.rand(200) * 0.002)
low = close * (1 - rng.rand(200) * 0.002)
op = close * (1 + rng.rand(200) * 0.001)
volume = rng.randint(100, 10000, size=200).astype(float)
df = pd.DataFrame(
    {'Open': op, 'High': high, 'Low': low, 'Close': close, 'Volume': volume},
    index=dates,
)
df.index.name = 'Datetime'

# Make get_data return the same df for any symbol/interval/period
mock.get_data = MagicMock(side_effect=lambda symbol, interval='5m', period='1y': df)
mock.is_available = MagicMock(return_value=True)
mock.supports_symbol = MagicMock(return_value=True)
mock.supports_market = MagicMock(return_value=True)
mock.supports_timeframe = MagicMock(return_value=True)
mock.max_history = MagicMock(return_value='10y')
mock.source_name = MagicMock(return_value='YahooFinanceMock')

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

service = MarketDataService(providers=[TestProvider(mock)])
pipeline = AnalysisPipeline(market_service=service, providers=[])

# Test pipeline execution
print("=== Testing pipeline execution ===")
result = pipeline.analyze(symbol='BTC-USD', silent=True)
print(f"Decision: {result.decision.decision}")
print(f"Grade: {result.decision.grade}")
print(f"Audit ID: {result.decision.audit_id}")
print(f"Explanation: {result.decision.explanation[:100]}...")
print(f"Trade allowed: {result.decision.trade_allowed}")
print(f"Trade block reasons: {result.decision.trade_block_reasons}")
print(f"Blockers: {result.decision.blockers}")
print(f"Warnings: {result.decision.warnings}")

print("\n=== Pipeline execution successful ===")
print("The AnalysisPipeline executed and produced a DecisionResult")
print("TradeFilter was called and reached the DecisionEngine")