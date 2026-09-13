"""Testes M5 Top-3 (puros, deterministicos, sem rede)."""
import pandas as pd
import numpy as np

from mercury_ai.analysis.institutional_confirmation import (
    closed_df, atr14, detect_liquidity_sweep, detect_displacement,
    detect_fvg, score_setup,
)
from mercury_ai.signals.top3_selector import select_top3
from mercury_ai.signals.m5_alerts import alert_state
from mercury_ai.signals.m5_timing import compute_next_m5, compute_entry_window
from mercury_ai.signals.entry_time import (
    countdown_s,
    enrich_top3_oportunidades,
    format_br,
    next_entry_utc,
)


def _df(n=60, seed=7):
    rng = np.random.default_rng(seed)
    base = 100 + np.cumsum(rng.normal(0, 0.2, n))
    idx = pd.date_range("2026-09-13 14:00", periods=n, freq="5min", tz="UTC")
    return pd.DataFrame({
        "Open": base, "High": base + 0.3, "Low": base - 0.3,
        "Close": base + 0.05, "Volume": 1000 + np.arange(n) * 5,
    }, index=idx)


def test_closed_excludes_forming():
    df = _df()
    cl = closed_df(df)
    assert len(cl) == len(df) - 1
    assert cl.index[-1] < df.index[-1]


def test_atr_positive():
    assert atr14(closed_df(_df())) > 0


def test_detectors_return_shape():
    cl = closed_df(_df())
    a = atr14(cl)
    for fn in (detect_liquidity_sweep, detect_displacement, detect_fvg):
        r = fn(cl, a)
        assert "detected" in r and "direction" in r


def test_score_gate():
    s = score_setup({"detected": True, "direction": "BULLISH"},
                    {"detected": True, "direction": "BULLISH"},
                    True, True, True, True)
    assert s["score"] == 100.0 and s["pass_gate"] is True
    s2 = score_setup({"detected": False, "direction": "NONE"},
                     {"detected": False, "direction": "NONE"},
                     False, False, False, False)
    assert s2["score"] == 0.0 and s2["pass_gate"] is False


def test_top3_filters_and_caps():
    def e(sym, dec, score, state="VALID", rr=2.5):
        return {"symbol": sym, "decision": dec, "score": score,
                "confidence": 70,
                "signal": {"symbol": sym, "decision": dec, "entry_timing_state": state,
                           "risk_reward": rr, "score": score, "confidence": 70, "confluence": 70}}
    rep = {"top3": [e("A", "BUY", 90), e("B", "SELL", 85), e("C", "BUY", 80),
                    e("D", "BUY", 75), e("W", "WAIT", 99), e("X", "BUY", 95, "EXPIRED"),
                    e("Y", "BUY", 95, "VALID", 1.5), e("Z", "BUY", 60)],
           "ranked": []}
    top3 = select_top3(rep)
    assert len(top3) == 3
    assert [t["symbol"] for t in top3] == ["A", "B", "C"]
    assert all(t["decision"] in ("BUY", "SELL") for t in top3)


def test_alert_window():
    assert alert_state(70.0)["state"] == "EMIT"
    assert alert_state(70.0)["in_window"] is True
    assert alert_state(200.0)["state"] == "WAIT"
    assert alert_state(-5.0)["state"] == "EXPIRED"


def test_timing_strict_ceil():
    nxt = compute_next_m5("2026-09-13T14:30:00+00:00")
    assert nxt == "2026-09-13T14:35:00+00:00"
    w = compute_entry_window("2026-09-13T14:33:50+00:00", nxt)
    assert w["valid"] is True and w["state"] == "VALID"
    w2 = compute_entry_window(nxt, nxt)
    assert w2["valid"] is False and w2["state"] == "EXPIRED"


def test_entry_time_next_m5():
    # Caso do print: sinal 02:52:22 -> entrada 02:55:00Z
    assert next_entry_utc(signal_ts="2026-09-13T02:52:22.061200+00:00") == "2026-09-13T02:55:00+00:00"
    assert next_entry_utc(signal_ts="2026-09-13T02:55:00+00:00") == "2026-09-13T03:00:00+00:00"
    assert next_entry_utc() is None
    assert format_br("2026-09-13T02:55:00+00:00") == "13/09 02:55:00 UTC"
    assert format_br(None) == "--"


def test_enrich_top3_oportunidades():
    ops = [
        {"symbol": "LTC-USD", "decision": "BUY", "score": 72.99,
         "signal_ts": "2026-09-13T02:52:22+00:00"},
        {"symbol": "XRP-USD", "decision": "BUY", "score": 72.93,
         "signal": {"signal_ts": "2026-09-13T02:52:22+00:00"}},
    ]
    out = enrich_top3_oportunidades(ops)
    assert out[0]["entrada_sugerida_utc"] == "2026-09-13T02:55:00+00:00"
    assert out[0]["entrada_sugerida_br"] == "13/09 02:55:00 UTC"
    assert out[1]["entrada_sugerida_utc"] == "2026-09-13T02:55:00+00:00"
    # verbatim: originais intactos
    assert out[0]["symbol"] == "LTC-USD" and out[0]["score"] == 72.99
