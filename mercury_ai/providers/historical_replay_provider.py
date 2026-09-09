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
            df_slice = self._df.iloc[:self._current_index + 1]
            if df_slice.empty:
                return df_slice
            # Fase 4 — M5 preserva comportamento temporal exato (sem transformação)
            if interval == "5m":
                return df_slice
            # M1 não desagregável a partir de base M5 — retorna fatia M5 por compatibilidade
            if interval == "1m":
                return df_slice
            # Fase 5 — timeframes superiores agregam EXCLUSIVAMENTE df_slice (anti-lookahead)
            return self._resample_slice(df_slice, interval)
        
        # Fallback: carrega do disco
        filename = f"replay_{symbol}.csv"
        filepath = os.path.join(self.data_path, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo de replay não encontrado: {filepath}")
            
        return pd.read_csv(filepath)

    def _resample_slice(self, df_slice: pd.DataFrame, interval: str) -> pd.DataFrame:
        """Agrega df_slice (já fatiado até current_index) para o interval solicitado.

        Ordem temporal obrigatória (Fase 3):
          full_df -> current_index -> df_slice -> agregação -> retorno
        Nunca full_df -> resample -> slice.

        Semântica OHLCV: open=first, high=max, low=min, close=last, volume=sum
        Somente para colunas existentes. Timestamp = início do candle (floor).
        Candle parcial é preservado (não elimina, não completa com futuro).
        """
        interval_to_rule = {
            "15m": "15min",
            "30m": "30min",
            "1h": "1h",
            "4h": "4h",
            "1d": "1D",
            "1wk": "1W",
            "1mo": "ME",
        }
        rule = interval_to_rule.get(interval)
        if rule is None:
            # tenta inferir numericamente (ex: "15m" -> "15min")
            if isinstance(interval, str) and interval.endswith("m"):
                try:
                    num = int(interval[:-1])
                    rule = f"{num}min"
                except ValueError:
                    return df_slice
            elif isinstance(interval, str) and interval.endswith("h"):
                rule = interval
            else:
                return df_slice

        # Monta agg apenas para OHLCV existentes (não inventa colunas)
        agg = {}
        for col in df_slice.columns:
            lower = str(col).lower()
            if lower == "open":
                agg[col] = "first"
            elif lower == "high":
                agg[col] = "max"
            elif lower == "low":
                agg[col] = "min"
            elif lower == "close":
                agg[col] = "last"
            elif lower == "volume":
                agg[col] = "sum"
        if not agg:
            return df_slice

        # Garante DatetimeIndex
        if not isinstance(df_slice.index, pd.DatetimeIndex):
            try:
                tmp = df_slice.copy()
                tmp.index = pd.to_datetime(tmp.index)
                df_slice = tmp
            except Exception:
                return df_slice
        if not isinstance(df_slice.index, pd.DatetimeIndex):
            return df_slice
        # Ordena se necessário
        try:
            if not df_slice.index.is_monotonic_increasing:
                df_slice = df_slice.sort_index()
        except Exception:
            df_slice = df_slice.sort_index()

        # Agregação por floor + groupby evita bins vazios de mercado fechado
        try:
            floored = df_slice.index.floor(rule)
        except Exception:
            # fallback resample
            try:
                resampled = df_slice.resample(rule).agg(agg)
                resampled = resampled.dropna(how="all")
                close_cols = [c for c in resampled.columns if str(c).lower() == "close"]
                if close_cols:
                    resampled = resampled.dropna(subset=close_cols, how="all")
                return resampled
            except Exception:
                return df_slice

        try:
            grouped = df_slice.groupby(floored, sort=True).agg(agg)
            grouped.index.name = df_slice.index.name
            if not isinstance(grouped.index, pd.DatetimeIndex):
                try:
                    grouped.index = pd.to_datetime(grouped.index)
                except Exception:
                    pass
            return grouped
        except Exception:
            try:
                resampled = df_slice.resample(rule).agg(agg).dropna(how="all")
                return resampled
            except Exception:
                return df_slice

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
