import pandas as pd
import os
from mercury_ai.providers.base_provider import MarketDataProvider

class HistoricalReplayProvider:
    def __init__(self, data_path: str = "data/replay"):
        self.data_path = data_path

    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        filename = f"replay_{symbol}.csv"
        filepath = os.path.join(self.data_path, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo de replay não encontrado: {filepath}")
            
        return pd.read_csv(filepath)

    def is_available(self) -> bool:
        return True

    def supports_symbol(self, symbol: str) -> bool:
        return True

    def supports_market(self, market: str) -> bool:
        return True

    def supports_timeframe(self, timeframe: str) -> bool:
        return True

    def max_history(self) -> str:
        return "unlimited"

    def source_name(self) -> str:
        return "HistoricalReplay"
