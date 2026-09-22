import pandas as pd

from mercury_ai.signals.ccl_continuation import detect_ccl


def _df(rows):
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"])


def test_detects_bullish_ccl():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 14
    # Continuacao compradora: 2 velas fortes de alta
    rows += [(100.2, 100.9, 100.1, 100.8), (100.8, 101.6, 100.7, 101.5)]
    # Consolidacao: caixa estreita
    rows += [(101.5, 101.55, 101.45, 101.5), (101.5, 101.55, 101.45, 101.5), (101.5, 101.55, 101.45, 101.5)]
    # Liquidez: sweep da caixa por baixo e fecha de volta
    rows.append((101.5, 101.6, 101.3, 101.55))
    result = detect_ccl(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "BUY"


def test_detects_bearish_ccl():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 14
    rows += [(100.2, 100.3, 99.3, 99.4), (99.4, 99.5, 98.6, 98.7)]
    rows += [(98.7, 98.75, 98.65, 98.7), (98.7, 98.75, 98.65, 98.7), (98.7, 98.75, 98.65, 98.7)]
    rows.append((98.7, 98.9, 98.6, 98.65))
    result = detect_ccl(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "SELL"


def test_no_continuation_no_signal():
    rows = [(100.0 + i * 0.01, 100.2 + i * 0.01, 99.9 + i * 0.01, 100.05 + i * 0.01) for i in range(20)]
    result = detect_ccl(_df(rows))
    assert result["detected"] is False


def test_short_df_returns_not_detected():
    rows = [(100.0, 100.2, 99.8, 100.1)] * 5
    result = detect_ccl(_df(rows))
    assert result["detected"] is False
