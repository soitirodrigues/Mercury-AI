from typing import Protocol, List
import pandas as pd

class IDataProvider(Protocol):
    name: str
    supported_timeframes: List[str]
    supported_markets: List[str]
    supported_assets: List[str]
    request_limit: int
    priority: int
    
    def get_data(self, symbol: str, interval: str = "5m") -> pd.DataFrame:
        ...
    def check_health(self) -> bool:
        ...
