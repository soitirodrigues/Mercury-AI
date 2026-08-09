"""Tests for the TradingView data provider."""

import importlib
import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

from mercury_ai.core.exceptions import (
    InvalidSymbolError,
    MarketClosedException,
    ProviderError,
)
from mercury_ai.providers import future_tradingview_provider as tv_module
from mercury_ai.providers.future_tradingview_provider import FutureTradingViewProvider


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def provider_no_lib():
    """Provider instance with tvDatafeed unavailable."""
    with patch.object(tv_module, "_TVDATAFEED_AVAILABLE", False):
        p = FutureTradingViewProvider()
        yield p


@pytest.fixture
def provider_with_mock_tv():
    """Provider instance with a mocked tvDatafeed client."""
    mock_tv = MagicMock()
    with patch.object(tv_module, "_TVDATAFEED_AVAILABLE", True), \
         patch.object(tv_module, "TvDatafeed", MagicMock(return_value=mock_tv)):
        p = FutureTradingViewProvider(username="user", password="pass")
        p._tv = mock_tv
        yield p


def _make_valid_ohlcv(n_bars: int = 25) -> pd.DataFrame:
    """Generate a valid OHLCV DataFrame with n_bars rows."""
    idx = pd.date_range("2024-01-01", periods=n_bars, freq="5min")
    rng = np.random.default_rng(42)
    close = 100 + rng.random(n_bars).cumsum()
    df = pd.DataFrame(
        {
            "Open": close - rng.random(n_bars),
            "High": close + rng.random(n_bars),
            "Low": close - rng.random(n_bars),
            "Close": close,
            "Volume": rng.integers(1000, 10000, size=n_bars),
        },
        index=idx,
    )
    return df


# ---------------------------------------------------------------------------
# is_available / supports_* / source_name / max_history
# ---------------------------------------------------------------------------
def test_is_available_false_when_lib_missing(provider_no_lib):
    assert provider_no_lib.is_available() is False


def test_is_available_true_when_client_initialized(provider_with_mock_tv):
    assert provider_with_mock_tv.is_available() is True


def test_source_name():
    p = FutureTradingViewProvider()
    assert p.source_name() == "TradingView"


def test_max_history():
    p = FutureTradingViewProvider()
    assert p.max_history() == "20y"


def test_supports_symbol_valid():
    p = FutureTradingViewProvider()
    assert p.supports_symbol("AAPL") is True
    assert p.supports_symbol("BINANCE:BTCUSDT") is True


def test_supports_symbol_invalid():
    p = FutureTradingViewProvider()
    assert p.supports_symbol("") is False
    assert p.supports_symbol("../etc/passwd") is False
    assert p.supports_symbol(None) is False  # type: ignore[arg-type]


def test_supports_market():
    p = FutureTradingViewProvider()
    assert p.supports_market("stock") is True
    assert p.supports_market("crypto") is True
    assert p.supports_market("forex") is True
    assert p.supports_market("futures") is True
    assert p.supports_market("index") is True
    assert p.supports_market("cfd") is True
    assert p.supports_market("options") is False


def test_supports_timeframe():
    p = FutureTradingViewProvider()
    assert p.supports_timeframe("5m") is True
    assert p.supports_timeframe("1h") is True
    assert p.supports_timeframe("1d") is True
    assert p.supports_timeframe("3m") is False


# ---------------------------------------------------------------------------
# get_data — error cases
# ---------------------------------------------------------------------------
def test_get_data_raises_when_lib_missing(provider_no_lib):
    with pytest.raises(ProviderError, match="tvDatafeed library not installed"):
        provider_no_lib.get_data("AAPL")


def test_get_data_invalid_symbol(provider_with_mock_tv):
    with pytest.raises((InvalidSymbolError, ValueError)):
        provider_with_mock_tv.get_data("../etc/passwd")


def test_get_data_unsupported_interval(provider_with_mock_tv):
    with pytest.raises(ValueError, match="Unsupported interval"):
        provider_with_mock_tv.get_data("AAPL", interval="3m")


# ---------------------------------------------------------------------------
# get_data — success cases
# ---------------------------------------------------------------------------
def test_get_data_success(provider_with_mock_tv):
    raw_df = _make_valid_ohlcv(25)
    # TradingView returns lowercase columns
    raw_df.columns = [c.lower() for c in raw_df.columns]
    provider_with_mock_tv._tv.get_hist.return_value = raw_df

    result = provider_with_mock_tv.get_data("AAPL", interval="5m", period="5d")

    assert isinstance(result, pd.DataFrame)
    assert len(result) >= 20
    assert "Open" in result.columns
    assert "Close" in result.columns
    assert "Volume" in result.columns


def test_get_data_caches_result(provider_with_mock_tv):
    raw_df = _make_valid_ohlcv(25)
    raw_df.columns = [c.lower() for c in raw_df.columns]
    provider_with_mock_tv._tv.get_hist.return_value = raw_df

    first = provider_with_mock_tv.get_data("AAPL", interval="5m", period="5d")
    second = provider_with_mock_tv.get_data("AAPL", interval="5m", period="5d")

    # Should only call the API once due to caching
    assert provider_with_mock_tv._tv.get_hist.call_count == 1
    # DataFrames should be equal (copy, not same object)
    assert first is not second
    pd.testing.assert_frame_equal(first, second)


def test_get_data_empty_response_raises(provider_with_mock_tv):
    provider_with_mock_tv._tv.get_hist.return_value = pd.DataFrame()
    with pytest.raises(MarketClosedException):
        provider_with_mock_tv.get_data("AAPL", interval="5m", period="5d")


def test_get_data_none_response_raises(provider_with_mock_tv):
    provider_with_mock_tv._tv.get_hist.return_value = None
    with pytest.raises(MarketClosedException):
        provider_with_mock_tv.get_data("AAPL", interval="5m", period="5d")


# ---------------------------------------------------------------------------
# _period_to_bars
# ---------------------------------------------------------------------------
def test_period_to_bars_days():
    assert FutureTradingViewProvider._period_to_bars("5d") >= 200
    assert FutureTradingViewProvider._period_to_bars("1d") >= 200


def test_period_to_bars_months():
    assert FutureTradingViewProvider._period_to_bars("1mo") >= 200
    assert FutureTradingViewProvider._period_to_bars("3mo") >= 200


def test_period_to_bars_years():
    assert FutureTradingViewProvider._period_to_bars("1y") >= 252


def test_period_to_bars_empty():
    assert FutureTradingViewProvider._period_to_bars("") == 200


# ---------------------------------------------------------------------------
# _infer_market
# ---------------------------------------------------------------------------
def test_infer_market_crypto():
    assert FutureTradingViewProvider._infer_market("BINANCE:BTCUSDT") == "crypto"


def test_infer_market_forex():
    assert FutureTradingViewProvider._infer_market("OANDA:EURUSD") == "forex"


def test_infer_market_futures():
    assert FutureTradingViewProvider._infer_market("CME_MINI:ES1!") == "futures"


def test_infer_market_index():
    assert FutureTradingViewProvider._infer_market("TVC:SPX") == "index"


def test_infer_market_stock_default():
    assert FutureTradingViewProvider._infer_market("AAPL") == "stock"


# ---------------------------------------------------------------------------
# _normalize_columns
# ---------------------------------------------------------------------------
def test_normalize_columns_lowercase():
    df = pd.DataFrame(
        {"open": [1], "high": [2], "low": [0.5], "close": [1.5], "volume": [100]}
    )
    result = FutureTradingViewProvider._normalize_columns(df)
    assert "Open" in result.columns
    assert "High" in result.columns
    assert "Low" in result.columns
    assert "Close" in result.columns
    assert "Volume" in result.columns


def test_normalize_columns_mixed_case():
    df = pd.DataFrame(
        {"Open": [1], "HIGH": [2], "Low": [0.5], "Close": [1.5], "volume": [100]}
    )
    result = FutureTradingViewProvider._normalize_columns(df)
    assert "Open" in result.columns
    assert "High" in result.columns
    assert "Low" in result.columns
    assert "Close" in result.columns
    assert "Volume" in result.columns
