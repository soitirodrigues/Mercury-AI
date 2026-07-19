import pandas as pd
import os
from typing import Optional

class HistoricalReplayProvider:
    def __init__(self, data_path: str = "data/replay"):
        self.data_path = data_path
        self._df: Optional[pd.DataFrame] = None
        self._current_index: int = 0

    def set_data(self, df: pd.DataFrame):
        """Define o DataFrame completo para replay."""
        self._df = df

    def set_index(self, index: int):
        """Define o índice atual do replay (previne look-ahead bias)."""
        self._current_index = index

    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        # Se temos dados em memória, retorna fatia até o índice atual
        if self._df is not None:
            return self._df.iloc[:self._current_index + 1]
        
        # Fallback: carrega do disco
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
