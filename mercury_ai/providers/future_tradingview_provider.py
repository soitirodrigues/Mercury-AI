"""TradingView data provider for Mercury-AI.

Implements the ``MarketDataProvider`` Protocol from ``base_provider.py``.

TradingView does not provide an official public REST API. This provider uses
the community-maintained ``tvDatafeed`` library when available. If the library
is not installed, the provider degrades gracefully — ``is_available()`` returns
``False`` and ``get_data()`` raises ``ProviderError`` with a clear message.

Design follows ``yahoo_finance_provider.py``:
- In-memory cache with TTL (``_CacheEntry``)
- Retry with exponential backoff (``_fetch_with_retry``)
- Schema validation via shared ``validate_ohlcv_schema`` from ``base_provider``
- Symbol sanitization via shared ``sanitize_symbol`` from ``base_provider``
"""

from __future__ import annotations

import logging
import time
from typing import Optional

import pandas as pd

from mercury_ai.core.exceptions import (
    InvalidSymbolError,
    MarketClosedException,
    ProviderError,
)
from mercury_ai.providers.base_provider import sanitize_symbol, validate_ohlcv_schema

logger = logging.getLogger("FutureTradingViewProvider")

# ---------------------------------------------------------------------------
# Optional dependency: tvDatafeed
# ---------------------------------------------------------------------------
try:
    from tvDatafeed import TvDatafeed, Interval as TvInterval  # type: ignore

    _TVDATAFEED_AVAILABLE = True
except ImportError:  # pragma: no cover — exercised via is_available()
    TvDatafeed = None  # type: ignore[assignment]
    TvInterval = None  # type: ignore[assignment]
    _TVDATAFEED_AVAILABLE = False


# ---------------------------------------------------------------------------
# Interval mapping (Mercury canonical → TradingView)
# ---------------------------------------------------------------------------
# TradingView interval strings accepted by tvDatafeed:
#   1m, 5m, 15m, 30m, 1h, 2h, 4h, 1d, 1W, 1M
_INTERVAL_MAP: dict[str, str] = {
    "1m": "1m",
    "5m": "5m",
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "2h": "2h",
    "4h": "4h",
    "1d": "1D",
    "1D": "1D",
    "1w": "1W",
    "1W": "1W",
    "1mo": "1M",
    "1M": "1M",
}

# Markets supported by TradingView: forex, crypto, futures, stock, index, cfd
_SUPPORTED_MARKETS = frozenset({"forex", "crypto", "futures", "stock", "index", "cfd"})


class _CacheEntry:
    """Simple TTL cache entry (mirrors ``yahoo_finance_provider``)."""

    __slots__ = ("data", "expires_at")

    def __init__(self, data: pd.DataFrame, ttl_seconds: float) -> None:
        self.data = data
        self.expires_at = time.monotonic() + ttl_seconds

    def is_valid(self) -> bool:
        return time.monotonic() < self.expires_at


class FutureTradingViewProvider:
    """TradingView data provider implementing ``MarketDataProvider`` Protocol.

    Parameters
    ----------
    username : str
        TradingView username (required by tvDatafeed).
    password : str
        TradingView password.
    cache_ttl_seconds : float
        Cache time-to-live in seconds (default 60).
    max_retries : int
        Maximum fetch retries (default 3).
    backoff_base : float
        Base for exponential backoff in seconds (default 1.0).
    """

    def __init__(
        self,
        username: str = "",
        password: str = "",
        cache_ttl_seconds: float = 60.0,
        max_retries: int = 3,
        backoff_base: float = 1.0,
    ) -> None:
        self._username = username
        self._password = password
        self._cache_ttl = cache_ttl_seconds
        self._max_retries = max_retries
        self._backoff_base = backoff_base
        self._cache: dict[str, _CacheEntry] = {}
        self._tv: Optional[object] = None

        if _TVDATAFEED_AVAILABLE and username and password:
            try:
                self._tv = TvDatafeed(username, password)  # type: ignore[misc]
                logger.info("TradingView connection established")
            except Exception as exc:  # pragma: no cover — network/auth failure
                logger.warning("TradingView connection failed: %s", exc)
                self._tv = None
        elif _TVDATAFEED_AVAILABLE and not username:
            # Anonymous mode — limited but functional for some symbols
            try:
                self._tv = TvDatafeed()  # type: ignore[misc]
                logger.info("TradingView anonymous connection established")
            except Exception as exc:  # pragma: no cover
                logger.warning("TradingView anonymous connection failed: %s", exc)
                self._tv = None

    # ------------------------------------------------------------------
    # Cache helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _cache_key(symbol: str, interval: str, n_bars: int) -> str:
        return f"{symbol}|{interval}|{n_bars}"

    def _get_cached(self, key: str) -> Optional[pd.DataFrame]:
        entry = self._cache.get(key)
        if entry is None:
            return None
        if entry.is_valid():
            return entry.data.copy()
        del self._cache[key]
        return None

    def _set_cached(self, key: str, data: pd.DataFrame) -> None:
        self._cache[key] = _CacheEntry(data, self._cache_ttl)

    # ------------------------------------------------------------------
    # Interval / period helpers
    # ------------------------------------------------------------------
    def _map_interval(self, interval: str) -> str:
        mapped = _INTERVAL_MAP.get(interval)
        if mapped is None:
            raise ValueError(f"Unsupported interval '{interval}' for TradingView")
        return mapped

    @staticmethod
    def _period_to_bars(period: str) -> int:
        """Convert a Mercury period string (e.g. '5d') into a bar count.

        TradingView's tvDatafeed accepts ``n_bars`` rather than a date range.
        """
        period = period.strip().lower()
        if not period:
            return 200
        unit = period[-1]
        try:
            value = int(period[:-1])
        except ValueError:
            return 200
        if unit == "d":
            # ~6.5 trading hours/day for stocks; use generous estimate
            return max(value * 80, 200)
        if unit == "w":
            return max(value * 5, 200)
        if unit == "mo":
            return max(value * 22, 200)
        if unit == "y":
            return max(value * 252, 200)
        return 200

    # ------------------------------------------------------------------
    # Retry logic
    # ------------------------------------------------------------------
    def _fetch_with_retry(
        self,
        symbol: str,
        tv_interval: str,
        n_bars: int,
        market: str,
    ) -> pd.DataFrame:
        """Fetch data from TradingView with exponential backoff."""
        last_exc: Optional[Exception] = None
        for attempt in range(1, self._max_retries + 1):
            try:
                if self._tv is None:
                    raise ProviderError("TradingView client not initialized")
                df = self._tv.get_hist(  # type: ignore[union-attr]
                    symbol=symbol,
                    interval=tv_interval,
                    n_bars=n_bars,
                    market=market,
                )
                if df is None or len(df) == 0:
                    raise MarketClosedException(
                        f"TradingView returned no data for {symbol}"
                    )
                return df
            except (
                ConnectionError,
                TimeoutError,
                OSError,
                ValueError,
                KeyError,
                RuntimeError,
            ) as exc:
                last_exc = exc
                wait = self._backoff_base * (2 ** (attempt - 1))
                logger.warning(
                    "TradingView fetch attempt %d/%d failed: %s — retrying in %.1fs",
                    attempt,
                    self._max_retries,
                    exc,
                    wait,
                )
                time.sleep(wait)

        raise MarketClosedException(
            f"TradingView fetch failed for {symbol} after {self._max_retries} retries: {last_exc}"
        )

    # ------------------------------------------------------------------
    # Public API — MarketDataProvider Protocol
    # ------------------------------------------------------------------
    def get_data(
        self,
        symbol: str,
        interval: str = "5m",
        period: str = "5d",
    ) -> pd.DataFrame:
        """Fetch OHLCV data from TradingView.

        Parameters
        ----------
        symbol : str
            TradingView symbol (e.g. ``"AAPL"``, ``"BINANCE:BTCUSDT"``).
        interval : str
            Bar interval (e.g. ``"5m"``, ``"1h"``, ``"1d"``).
        period : str
            History period (e.g. ``"5d"``, ``"1mo"``).

        Returns
        -------
        pandas.DataFrame
            Validated OHLCV DataFrame with columns Open, High, Low, Close, Volume.

        Raises
        ------
        InvalidSymbolError
            If the symbol fails sanitization.
        ProviderError
            If the tvDatafeed library is not installed.
        MarketClosedException
            If all retries fail or no data is returned.
        DataValidationError
            If the returned data fails schema validation.
        """
        clean_symbol = sanitize_symbol(symbol) if ":" not in symbol else symbol.strip().upper()
        if ":" not in clean_symbol:
            # Already validated by sanitize_symbol above
            pass
        else:
            # Validate exchange:symbol format (e.g. BINANCE:BTCUSDT)
            parts = clean_symbol.split(":")
            if len(parts) != 2 or not parts[0] or not parts[1]:
                raise InvalidSymbolError(f"Símbolo TradingView inválido: {symbol!r}")
            from mercury_ai.providers.base_provider import _SYMBOL_RE

            if not _SYMBOL_RE.match(parts[0]) or not _SYMBOL_RE.match(parts[1]):
                raise InvalidSymbolError(f"Símbolo TradingView inválido: {symbol!r}")
        tv_interval = self._map_interval(interval)
        n_bars = self._period_to_bars(period)

        # Determine market from symbol prefix (e.g. "BINANCE:BTCUSDT" → crypto)
        market = self._infer_market(clean_symbol)

        cache_key = self._cache_key(clean_symbol, tv_interval, n_bars)
        cached = self._get_cached(cache_key)
        if cached is not None:
            return cached

        if not _TVDATAFEED_AVAILABLE:
            raise ProviderError(
                "tvDatafeed library not installed. Install with: pip install tvDatafeed"
            )

        df = self._fetch_with_retry(clean_symbol, tv_interval, n_bars, market)

        # Normalize column names to match our schema
        df = self._normalize_columns(df)

        validate_ohlcv_schema(df, clean_symbol)

        self._set_cached(cache_key, df)
        return df.copy()

    @staticmethod
    def _infer_market(symbol: str) -> str:
        """Infer TradingView market from symbol prefix."""
        if ":" in symbol:
            prefix = symbol.split(":")[0].upper()
            crypto_exchanges = {"BINANCE", "COINBASE", "KRAKEN", "BITSTAMP", "OKX"}
            if prefix in crypto_exchanges:
                return "crypto"
            if prefix in {"FX", "FX_IDC", "OANDA", "SAXO"}:
                return "forex"
            if prefix in {"CME", "CME_MINI", "CBOT", "COMEX", "NYMEX", "ICE", "EUREX"}:
                return "futures"
            if prefix in {"SP", "NASDAQ", "DJ", "TVC"}:
                return "index"
            return "stock"
        return "stock"

    @staticmethod
    def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Normalize TradingView column names to our canonical schema."""
        rename_map: dict[str, str] = {}
        for col in df.columns:
            lower = col.lower()
            if lower == "open":
                rename_map[col] = "Open"
            elif lower == "high":
                rename_map[col] = "High"
            elif lower == "low":
                rename_map[col] = "Low"
            elif lower == "close":
                rename_map[col] = "Close"
            elif lower == "volume":
                rename_map[col] = "Volume"
        if rename_map:
            df = df.rename(columns=rename_map)
        return df

    def is_available(self) -> bool:
        """Return True if tvDatafeed is installed and client is initialized."""
        return _TVDATAFEED_AVAILABLE and self._tv is not None

    def supports_symbol(self, symbol: str) -> bool:
        """Return True if the symbol is valid for TradingView.

        TradingView symbols may include an exchange prefix separated by ``:``
        (e.g. ``BINANCE:BTCUSDT``, ``OANDA:EURUSD``). The base ``sanitize_symbol``
        rejects ``:`` for safety in file-path contexts, so we validate the
        prefix and suffix separately here.
        """
        if not symbol or not isinstance(symbol, str):
            return False
        cleaned = symbol.strip().upper()
        if ".." in cleaned or "/" in cleaned or "\\" in cleaned:
            return False
        if ":" in cleaned:
            parts = cleaned.split(":")
            if len(parts) != 2:
                return False
            prefix, suffix = parts
            if not prefix or not suffix:
                return False
            # Validate both parts against the whitelist regex (without the colon)
            from mercury_ai.providers.base_provider import _SYMBOL_RE

            return bool(_SYMBOL_RE.match(prefix) and _SYMBOL_RE.match(suffix))
        try:
            sanitize_symbol(symbol)
            return True
        except (InvalidSymbolError, ValueError):
            return False

    def supports_market(self, market: str) -> bool:
        """Return True if the market type is supported by TradingView."""
        return market.lower() in _SUPPORTED_MARKETS

    def supports_timeframe(self, timeframe: str) -> bool:
        """Return True if the timeframe is supported by TradingView."""
        return timeframe in _INTERVAL_MAP

    def max_history(self) -> str:
        """Return the maximum history available from TradingView."""
        return "20y"

    def source_name(self) -> str:
        """Return the provider source name."""
        return "TradingView"
