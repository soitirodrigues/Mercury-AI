import numpy as np
import pandas as pd
import pytest

from mercury_ai.signals.m5_walk_forward import evaluate_walk_forward, wilson_interval


def _frame(n=100):
    index = pd.date_range("2026-01-01", periods=n, freq="5min", tz="UTC")
    close = np.arange(100.0, 100.0 + n)
    return pd.DataFrame({
        "Open": close - 0.5,
        "High": close + 0.5,
        "Low": close - 1.0,
        "Close": close,
        "Volume": 1000.0,
    }, index=index)


def _approved_flags(closed, decision):
    return {
        "has_liquidity_sweep": True,
        "in_premium_discount_zone": True,
        "reversal_candle": "BULLISH_REVERSAL" if decision == "BUY" else "BEARISH_REVERSAL",
        "trigger_aligned": True,
        "trigger_body_ratio": 0.5,
        "trigger_range_atr": 1.0,
        "has_fvg": True,
        "has_inducement": False,
    }


def test_wilson_interval_is_bounded_and_contains_rate():
    low, high = wilson_interval(98, 100)
    assert 0.0 <= low <= 0.98 <= high <= 1.0


def test_walk_forward_only_passes_closed_history_to_provider():
    frame = _frame()
    seen = []

    def provider(closed, decision):
        seen.append(len(closed))
        assert closed.index[-1] <= frame.index[len(closed) - 1]
        return _approved_flags(closed, decision)

    report = evaluate_walk_forward(
        frame,
        min_history=10,
        flag_provider=provider,
        payout=0.8,
    )

    assert report["contract"]["lookahead"] is False
    assert seen[0] == 11
    assert len(seen) == report["dataset"]["decision_indices"]
    assert report["overall"]["signals"] == len(seen)
    assert report["overall"]["hit_rate"] == 1.0
    assert report["overall"]["net_result"] == pytest.approx(71.2)
    assert report["splits"]["test"]["signals"] > 0


def test_walk_forward_labels_next_candle_not_decision_candle():
    frame = _frame(80)
    frame.iloc[40, frame.columns.get_loc("Close")] = frame.iloc[39]["Close"] - 10.0

    report = evaluate_walk_forward(
        frame,
        min_history=10,
        horizon=1,
        flag_provider=_approved_flags,
    )

    assert report["overall"]["signals"] == 69
    assert report["overall"]["losses"] >= 1
    assert report["contract"]["outcome"] == "close_after_1_candle(s)"


def test_walk_forward_uses_next_candle_open_for_binary_outcome():
    frame = _frame(80)
    frame.iloc[30, frame.columns.get_loc("Open")] = 200.0
    frame.iloc[30, frame.columns.get_loc("Close")] = 199.0

    report = evaluate_walk_forward(
        frame,
        min_history=10,
        horizon=1,
        flag_provider=_approved_flags,
    )

    assert report["overall"]["losses"] >= 1
    assert report["contract"]["entry"] == "open_of_outcome_candle"


def test_walk_forward_rejects_invalid_temporal_split():
    with pytest.raises(ValueError):
        evaluate_walk_forward(_frame(), train_ratio=0.8, validation_ratio=0.3)
