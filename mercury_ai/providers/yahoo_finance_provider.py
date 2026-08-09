import re
import time
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

import yfinance as yf
import pandas as pd

from mercury_ai.core.exceptions import MarketClosedException, DataValidationError

logger = logging.getLogger(__name__)

# Regex whitelist para símbolos: letras, números, ponto, hífen, underline, '=' (separador
# oficial de forex/commodity do Yahoo, ex.: EURUSD=X, CL=F), até 20 chars.
# Segurança: continua rejeitando path traversal (/, \, ..) e caracteres especiais.
_SYMBOL_RE = re.compile(r"^[A-Z0-9.\-_=]{1,20}$")

# Colunas OHLCV obrigatórias
_REQUIRED_COLUMNS = ("Open", "High", "Low", "Close", "Volume")


class _CacheEntry:
    """Entrada de cache simples com TTL."""

    __slots__ = ("data", "expires_at")

    def __init__(self, data: pd.DataFrame, ttl_seconds: float):
        self.data = data
        self.expires_at = time.monotonic() + ttl_seconds

    def is_valid(self) -> bool:
        return time.monotonic() < self.expires_at


class YahooFinanceProvider:
    """Provider Yahoo Finance com cache TTL, retry exponencial e validação de schema.

    Correções aplicadas:
      - C1: Validação de schema (colunas OHLCV, tipos numéricos, sem NaN crítico)
      - C3: Sanitização de símbolo (regex whitelist, rejeita path traversal)
      - C5: Cache em memória com TTL configurável
      - C6: Retry com backoff exponencial (3 tentativas: 1s, 2s, 4s)
    """

    def __init__(
        self,
        cache_ttl_seconds: float = 60.0,
        max_retries: int = 3,
        backoff_base: float = 1.0,
    ):
        self._cache: dict[str, _CacheEntry] = {}
        self._cache_ttl = cache_ttl_seconds
        self._max_retries = max_retries
        self._backoff_base = backoff_base

    # ------------------------------------------------------------------ #
    #  C3 — Sanitização de símbolo
    # ------------------------------------------------------------------ #
    @staticmethod
    def _sanitize_symbol(symbol: str) -> str:
        """Valida e sanitiza o símbolo antes de enviar ao Yahoo Finance.

        - Rejeita None / vazio
        - Rejeita path traversal (../, ..\\, /, \\)
        - Rejeita caracteres especiais não whitelisted
        - Normaliza para uppercase
        """
        if not symbol or not isinstance(symbol, str):
            raise DataValidationError(f"Símbolo inválido: {symbol!r}")
        cleaned = symbol.strip().upper()
        if ".." in cleaned or "/" in cleaned or "\\" in cleaned:
            raise DataValidationError(f"Símbolo contém sequência proibida: {symbol!r}")
        if not _SYMBOL_RE.match(cleaned):
            raise DataValidationError(f"Símbolo não passou whitelist regex: {symbol!r}")
        return cleaned

    # ------------------------------------------------------------------ #
    #  C5 — Cache
    # ------------------------------------------------------------------ #
    def _cache_key(self, symbol: str, interval: str, period: str) -> str:
        return f"{symbol}|{interval}|{period}"

    def _get_cached(self, key: str) -> Optional[pd.DataFrame]:
        entry = self._cache.get(key)
        if entry and entry.is_valid():
            logger.debug("Cache HIT para %s", key)
            return entry.data.copy()
        if entry:
            del self._cache[key]
        return None

    def _set_cached(self, key: str, data: pd.DataFrame):
        self._cache[key] = _CacheEntry(data, self._cache_ttl)

    # ------------------------------------------------------------------ #
    #  C6 — Retry com backoff exponencial
    # ------------------------------------------------------------------ #
    def _fetch_with_retry(self, symbol: str, interval: str, period: str) -> pd.DataFrame:
        last_exc: Optional[Exception] = None
        for attempt in range(1, self._max_retries + 1):
            try:
                ticker = yf.Ticker(symbol)
                df = ticker.history(period=period, interval=interval)
                return df
            except (ConnectionError, TimeoutError, OSError, ValueError, KeyError, RuntimeError) as exc:
                last_exc = exc
                if attempt < self._max_retries:
                    wait = self._backoff_base * (2 ** (attempt - 1))
                    logger.warning(
                        "Tentativa %d/%d falhou para %s: %s — retry em %.1fs",
                        attempt, self._max_retries, symbol, exc, wait,
                    )
                    time.sleep(wait)
        raise MarketClosedException(
            f"Falha após {self._max_retries} tentativas para {symbol}: {last_exc}"
        )

    # ------------------------------------------------------------------ #
    #  C1 — Validação de schema
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_schema(df: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Valida schema do DataFrame retornado pelo Yahoo Finance.

        - Não vazio e mínimo de 20 barras
        - Colunas OHLCV presentes
        - Tipos numéricos
        - Sem NaN em colunas críticas (OHLC)
        """
        if df is None or df.empty:
            raise MarketClosedException(f"DataFrame vazio para {symbol}")
        if len(df) < 20:
            raise MarketClosedException(
                f"Dados insuficientes ({len(df)} barras < 20) para {symbol}"
            )
        missing = [c for c in _REQUIRED_COLUMNS if c not in df.columns]
        if missing:
            raise DataValidationError(
                f"Colunas ausentes {missing} para {symbol}"
            )
        # Validar tipos numéricos
        for col in _REQUIRED_COLUMNS:
            if not pd.api.types.is_numeric_dtype(df[col]):
                raise DataValidationError(
                    f"Coluna '{col}' não é numérica para {symbol}"
                )
        # Validar NaN em OHLC (Volume pode ter NaN em alguns casos)
        for col in ("Open", "High", "Low", "Close"):
            if df[col].isna().any():
                raise DataValidationError(
                    f"NaN encontrado em '{col}' para {symbol}"
                )
        return df

    # ------------------------------------------------------------------ #
    #  API pública
    # ------------------------------------------------------------------ #
    def get_data(self, symbol: str, interval: str = "5m", period: str = "5d") -> pd.DataFrame:
        # C3: sanitizar símbolo
        clean_symbol = self._sanitize_symbol(symbol)

        # C5: checar cache
        key = self._cache_key(clean_symbol, interval, period)
        cached = self._get_cached(key)
        if cached is not None:
            return cached

        # C6: fetch com retry
        df = self._fetch_with_retry(clean_symbol, interval, period)

        # C1: validar schema
        df = self._validate_schema(df, clean_symbol)

        # C5: armazenar em cache
        self._set_cached(key, df)
        return df.copy()

    def is_available(self) -> bool:
        return True

    def supports_symbol(self, symbol: str) -> bool:
        try:
            self._sanitize_symbol(symbol)
            return True
        except DataValidationError:
            return False

    def supports_market(self, market: str) -> bool:
        return True

    def supports_timeframe(self, timeframe: str) -> bool:
        return True

    def max_history(self) -> str:
        return "10y"

    def source_name(self) -> str:
        return "YahooFinance"
