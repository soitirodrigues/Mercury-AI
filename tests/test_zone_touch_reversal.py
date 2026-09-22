import pandas as pd
import pytest

from mercury_ai.signals.zone_touch_reversal import detect_zone_reversal


def _df(rows):
    return pd.DataFrame(rows, columns=["Open", "High", "Low", "Close"])


def _flat_history(n=70, price=100.0):
    # Corpos repetidos na mesma faixa -> zona de toque de corpo
    return [(price, price + 0.2, price - 0.2, price + 0.05) for _ in range(n)]


def test_detects_sell_at_resistance_zone():
    # Historico oscila entre corpos em 100.0 e 100.5 -> duas zonas
    rows = []
    for i in range(70):
        base = 100.5 if i % 2 == 0 else 100.0
        rows.append((base, base + 0.15, base - 0.15, base + 0.05))
    # Trigger: sobe ate a zona 100.5 e rejeita com pavio superior
    rows.append((100.45, 100.70, 100.30, 100.40))
    result = detect_zone_reversal(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "SELL"
    assert result["touches"] >= 2
    assert result["zone"] is not None


def test_detects_buy_at_support_zone():
    rows = []
    for i in range(70):
        base = 100.5 if i % 2 == 0 else 100.0
        rows.append((base, base + 0.15, base - 0.15, base + 0.05))
    # Trigger: cai ate a zona 100.0 e rejeita com pavio inferior
    rows.append((99.95, 100.20, 99.78, 100.08))
    result = detect_zone_reversal(_df(rows))
    assert result["detected"] is True
    assert result["direction"] == "BUY"


def test_no_signal_without_rejection_wick():
    rows = []
    for i in range(70):
        base = 100.5 if i % 2 == 0 else 100.0
        rows.append((base, base + 0.15, base - 0.15, base + 0.05))
    # Corpo grande sem pavio de rejeicao na zona
    rows.append((100.48, 100.52, 100.10, 100.15))
    result = detect_zone_reversal(_df(rows))
    assert result["detected"] is False


def test_short_df_returns_not_detected():
    rows = _flat_history(10)
    result = detect_zone_reversal(_df(rows))
    assert result["detected"] is False
    assert result["direction"] == "NONE"


def test_no_lookahead_zone_excludes_trigger():
    # Historico plano sem rejeicao na trigger -> sem deteccao
    rows = _flat_history()
    rows.append((100.0, 100.01, 99.99, 99.99))  # sem pavio de rejeicao
    result = detect_zone_reversal(_df(rows))
    assert result["detected"] is False
