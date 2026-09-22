import pandas as pd

from mercury_ai.signals.price_action_patterns import detect_price_action


def _df(rows):
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"])


def test_detects_bullish_engulfing():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 4
    rows += [(100.2, 100.3, 99.9, 100.0)]  # queda
    rows.append((99.9, 100.5, 99.8, 100.4))  # engolfo de alta
    result = detect_price_action(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "BUY"
    assert result["pattern"] == "ENGULFING"


def test_detects_bearish_engulfing():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 4
    rows += [(100.2, 100.4, 100.1, 100.3)]  # alta
    rows.append((100.4, 100.5, 99.7, 99.8))  # engolfo de baixa
    result = detect_price_action(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "SELL"
    assert result["pattern"] == "ENGULFING"


def test_detects_morning_star():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 3
    rows += [(100.2, 100.3, 99.0, 99.1)]  # vela longa de baixa
    rows += [(99.1, 99.2, 99.0, 99.05)]  # indecisao
    rows.append((99.05, 99.8, 99.0, 99.7))  # alta que invade
    result = detect_price_action(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "BUY"
    # A vela de alta tambem engolfa a indecisao; engolfo tem prioridade
    assert result["pattern"] in ("MORNING_STAR", "ENGULFING")


def test_detects_pin_bar():
    rows = [(100.0, 100.3, 99.8, 100.2)] * 4
    rows += [(100.2, 100.3, 99.9, 100.0)]  # queda
    rows.append((100.0, 100.1, 99.0, 100.05))  # pin bar de alta
    result = detect_price_action(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "BUY"
    assert result["pattern"] == "PIN_BAR"


def test_no_pattern_returns_not_detected():
    rows = [(100.0 + i * 0.01, 100.2 + i * 0.01, 99.9 + i * 0.01, 100.05 + i * 0.01) for i in range(6)]
    result = detect_price_action(_df(rows))
    assert result["detected"] is False
