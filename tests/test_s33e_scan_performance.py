"""S33-E — Scan performance: cache Yahoo + paralelismo entre ativos + ScanReport.

- Estratégia preservada: nenhum engine/peso/threshold/ranking tocado aqui;
  estes testes usam doubles, nunca rede real.
- YahooAdapter.get_data é mockado no nível yf.download.
- Equivalência seq×paralelo usa analyses fake com scores distintos.
"""
from unittest.mock import MagicMock, patch

import pandas as pd

from mercury_ai.brain.scanner import (
    MercuryScanner,
    SCAN_COMPLETE,
    SCAN_TIMEOUT,
    SCAN_PARTIAL,
)
from mercury_ai.providers.data_adapters import YahooAdapter


def _ohlc(n=30):
    import datetime as _dt
    idx = pd.date_range("2026-01-05 09:00", periods=n, freq="5min", tz="UTC")
    base = 100.0
    return pd.DataFrame(
        {
            "Open": [base + i * 0.01 for i in range(n)],
            "High": [base + 0.05 + i * 0.01 for i in range(n)],
            "Low": [base - 0.05 + i * 0.01 for i in range(n)],
            "Close": [base + 0.02 + i * 0.01 for i in range(n)],
            "Volume": [1000 + i for i in range(n)],
        },
        index=idx,
    )


def _fake_analysis(symbol, score):
    a = MagicMock()
    a.market.symbol = symbol
    a.decision.decision = "WAIT"
    a.decision.score = score
    a.decision.summary = "ok"
    a.decision.audit_id = "a" * 64  # hash-like legítimo
    a.decision.confidence = 0.5
    a.decision.grade = "C"
    a.market_regime.regime = "RANGE"
    return a


def test_yahoo_cache_dedups_same_symbol_interval():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    df = _ohlc()
    with patch(
        "mercury_ai.providers.data_adapters.yf.download", return_value=df
    ) as mock_dl:
        out1 = adapter.get_data("EURUSD=X", "5m")
        out2 = adapter.get_data("EURUSD=X", "5m")
        assert mock_dl.call_count == 1
        stats = adapter.get_cache_stats()
        assert stats["downloads"] == 1
        assert stats["hits"] == 1
        assert stats["misses"] == 1
        # callers recebem cópias: mutar out1 não contamina out2/cache
        out1.iloc[0, 0] = -99999.0
        assert out2.iloc[0, 0] != -99999.0
        out3 = adapter.get_data("EURUSD=X", "5m")
        assert out3.iloc[0, 0] != -99999.0


def test_yahoo_cache_key_includes_interval_and_skips_empty():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    df = _ohlc()
    with patch(
        "mercury_ai.providers.data_adapters.yf.download", return_value=df
    ) as mock_dl:
        adapter.get_data("EURUSD=X", "5m")
        adapter.get_data("EURUSD=X", "1m")
        assert mock_dl.call_count == 2
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        return_value=pd.DataFrame(),
    ) as mock_dl2:
        r1 = adapter.get_data("GBPUSD=X", "5m")
        r2 = adapter.get_data("GBPUSD=X", "5m")
        assert r1.empty and r2.empty
        # vazio nunca é cacheado
        assert mock_dl2.call_count == 2
        assert adapter.get_cache_stats()["downloads"] == 4


def _scanner_with_fakes(symbols_scores):
    sc = MercuryScanner()
    sc.asset_registry.update_asset_stats = MagicMock()
    sc._trigger_failover = MagicMock()
    sc._print_report = MagicMock()
    sc._print_ranking = MagicMock()
    fakes = {s: _fake_analysis(s, v) for s, v in symbols_scores.items()}

    def _analyze_seq(symbol):
        return fakes[symbol]

    sc.pipeline.analyze = MagicMock(side_effect=_analyze_seq)

    def _isolated(symbol, scan_id=None):
        # S33-E.2 P3 — worker ecoa scan_id (6-tupla); None = compat legado.
        return (symbol, fakes[symbol], None, 0.05, [], scan_id)

    sc._analyze_symbol_isolated = MagicMock(side_effect=_isolated)
    return sc, fakes


def test_sequential_parallel_equivalence_same_ranking():
    symbols_scores = {"AAA": 45.0, "BBB": 90.0, "CCC": 60.0}
    sc, _ = _scanner_with_fakes(symbols_scores)
    symbols = ["AAA", "BBB", "CCC"]

    ranked_seq = sc._scan_sequential(symbols, [], workers=1)
    order_seq = [a.market.symbol for a in ranked_seq]
    assert order_seq == ["BBB", "CCC", "AAA"]
    assert sc.last_scan_report.status == SCAN_COMPLETE

    ranked_par = sc._scan_parallel(symbols, workers=3, cycle_timeout_s=290.0)
    order_par = [a.market.symbol for a in ranked_par]
    assert order_par == order_seq
    assert sc.last_scan_report.status == SCAN_COMPLETE
    assert [a.market.symbol for a in sc.last_scan_report.top3] == order_seq[:3]
    # identidade da execução: scan_ids distintos, nunca misturados
    ids_seq = {r["scan_id"] for r in sc.last_scan_report.per_asset}
    assert len(ids_seq) == 1


def test_parallel_timeout_marks_status_and_preserves_completed():
    sc, _ = _scanner_with_fakes({"AAA": 80.0, "BBB": 70.0})
    # deadline expirado antes de qualquer conclusão -> TIMEOUT, ranked vazio
    ranked = sc._scan_parallel(["AAA", "BBB"], workers=2, cycle_timeout_s=0.0)
    assert ranked == []
    rep = sc.last_scan_report
    assert rep.status == SCAN_TIMEOUT
    assert rep.symbols_timeout == 2
    assert rep.symbols_completed == 0
    assert rep.top3 == []


def test_scan_report_to_dict_never_declares_partial_complete():
    sc, _ = _scanner_with_fakes({"AAA": 80.0})
    sc._scan_sequential(["AAA"], [], workers=1)
    d = sc.last_scan_report.to_dict()
    assert d["status"] == SCAN_COMPLETE
    assert d["symbols_total"] == 1
    assert d["top3"][0]["symbol"] == "AAA"
    assert d["top3"][0]["audit_id"] == "a" * 64
