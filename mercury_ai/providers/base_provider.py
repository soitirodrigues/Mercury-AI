import re
from typing import Protocol
import pandas as pd

# Regex whitelist para símbolos: letras, números, ponto, hífen, underline, até 20 chars
_SYMBOL_RE = re.compile(r"^[A-Z0-9.\-_]{1,20}$")

# Colunas OHLCV obrigatórias
REQUIRED_OHLCV_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


def sanitize_symbol(symbol: str) -> str:
    """Valida e sanitiza um símbolo de ativo.

    - Rejeita None / vazio
    - Rejeita path traversal (../, ..\\, /, \\)
    - Rejeita caracteres especiais não whitelisted
    - Normaliza para uppercase

    Raises:
        ValueError: se o símbolo for inválido.
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError(f"Símbolo inválido: {symbol!r}")
    cleaned = symbol.strip().upper()
    if ".." in cleaned or "/" in cleaned or "\\" in cleaned:
        raise ValueError(f"Símbolo contém sequência proibida: {symbol!r}")
    if not _SYMBOL_RE.match(cleaned):
        raise ValueError(f"Símbolo não passou whitelist regex: {symbol!r}")
    return cleaned


def validate_ohlcv_schema(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Valida o schema de um DataFrame OHLCV.

    - Não vazio e mínimo de 20 barras
    - Colunas OHLCV presentes
    - Tipos numéricos
    - Sem NaN em colunas críticas (OHLC)

    Raises:
        ValueError: se o schema for inválido.
    """
    if df is None or df.empty:
        raise ValueError(f"DataFrame vazio para {symbol}")
    if len(df) < 20:
        raise ValueError(f"Dados insuficientes ({len(df)} barras < 20) para {symbol}")
    missing = [c for c in REQUIRED_OHLCV_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes {missing} para {symbol}")
    for col in REQUIRED_OHLCV_COLUMNS:
        if not pd.api.types.is_numeric_dtype(df[col]):
            raise ValueError(f"Coluna '{col}' não é numérica para {symbol}")
    for col in ("Open", "High", "Low", "Close"):
        if df[col].isna().any():
            raise ValueError(f"NaN encontrado em '{col}' para {symbol}")
    return df


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
