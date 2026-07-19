from typing import Protocol
import pandas as pd

class MarketDataProvider(Protocol):
    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        ...

    def is_available(self) -> bool:
        ...

    def supports_symbol(self, symbol: str) -> bool:
        ...

    def supports_market(self, market: str) -> bool:
        ...

    def supports_timeframe(self, timeframe: str) -> bool:
        ...

    def max_history(self) -> str:
        ...

    def source_name(self) -> str:
        ...
