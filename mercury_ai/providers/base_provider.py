import re
from typing import Protocol
import pandas as pd

# Regex whitelist para símbolos: letras, números, ponto, hífen, underline, até 20 chars
_SYMBOL_RE = re.compile(r"^[A-Z0-9.\-_]{1,20}$")

# Colunas OHLCV obrigatórias (case-insensitive — aceita "open" ou "Open")
REQUIRED_OHLCV_COLUMNS = ("Open", "High", "Low", "Close")
# Volume é opcional (alguns feeds como TradingView nem sempre fornecem)
OPTIONAL_OHLCV_COLUMNS = ("Volume",)


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


def _find_column(df: pd.DataFrame, name: str) -> str | None:
    """Encontra uma coluna de forma case-insensitive.

    Retorna o nome real da coluna no DataFrame, ou None se não existir.
    """
    lower_map = {c.lower(): c for c in df.columns}
    return lower_map.get(name.lower())


def validate_ohlcv_schema(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
    """Valida o schema de um DataFrame OHLCV.

    - Não vazio e mínimo de 20 barras
    - Colunas OHLCV presentes (case-insensitive: aceita "open" ou "Open")
    - Volume é opcional (não falha se ausente)
    - Tipos numéricos
    - Sem NaN em colunas críticas (OHLC)

    Raises:
        ValueError: se o schema for inválido.
    """
    if df is None or df.empty:
        raise ValueError(f"DataFrame vazio para {symbol}")
    if len(df) < 20:
        raise ValueError(f"Dados insuficientes ({len(df)} barras < 20) para {symbol}")

    # Resolver nomes reais das colunas (case-insensitive)
    resolved = {}
    missing = []
    for col in REQUIRED_OHLCV_COLUMNS:
        real = _find_column(df, col)
        if real is None:
            missing.append(col)
        else:
            resolved[col] = real
    if missing:
        raise ValueError(f"Colunas ausentes {missing} para {symbol}")

    # Validar tipos numéricos (OHLC obrigatório)
    for col, real in resolved.items():
        if not pd.api.types.is_numeric_dtype(df[real]):
            raise ValueError(f"Coluna '{col}' não é numérica para {symbol}")

    # Validar NaN apenas em OHLC (Volume é opcional)
    for col in ("Open", "High", "Low", "Close"):
        if df[resolved[col]].isna().any():
            raise ValueError(f"NaN encontrado em '{col}' para {symbol}")

    # Volume opcional: se presente, valida tipo numérico e não-NaN
    vol_col = _find_column(df, "Volume")
    if vol_col is not None:
        if not pd.api.types.is_numeric_dtype(df[vol_col]):
            raise ValueError(f"Coluna 'Volume' não é numérica para {symbol}")
        if df[vol_col].isna().any():
            raise ValueError(f"NaN encontrado em 'Volume' para {symbol}")

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
