"""S7.1 — Nenhuma rede durante replay.

run_replay não deve chamar yfinance / yf.download quando full_df é fornecido.
"""
import pandas as pd
import numpy as np
import pytest
from unittest.mock import patch

from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine


def _make_df(n=100):
    np.random.seed(99)
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    close = 100 + np.cumsum(np.random.randn(n) * 0.3)
    return pd.DataFrame({
        "open": close - 0.1,
        "high": close + 0.2,
        "low": close - 0.2,
        "close": close,
        "volume": np.random.randint(1000, 10000, n),
    }, index=dates)


def test_no_yfinance_called_during_replay():
    df = _make_df(100)
    engine = HistoricalReplayEngine()
    with patch("yfinance.download") as mock_dl:
        with patch("yfinance.Ticker") as mock_ticker:
            mock_dl.side_effect = AssertionError("yfinance.download called during replay")
            mock_ticker.side_effect = AssertionError("yfinance.Ticker called during replay")
            # run_replay injeta HistoricalReplayProvider com full_df, não deve importar yfinance
            metrics = engine.run_replay("NO-NET", df, n_candles=5, silent=True)
            assert len(metrics) > 0


def test_replay_determinism_byte_equal():
    df = _make_df(110)
    e = HistoricalReplayEngine()
    m1 = e.run_replay("DET", df, n_candles=5, silent=True)
    m2 = e.run_replay("DET", df, n_candles=5, silent=True)
    assert len(m1) == len(m2)
    for a, b in zip(m1, m2):
        assert a.pl == b.pl
