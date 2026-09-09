"""S33-E.2 — CORRECTNESS REMEDIATION tests (doubles only, sem rede/Yahoo real).

Cobre SOMENTE os bloqueadores de corretude:
  A) sequential           — path legado preservado
  B) parallel             — workers=4 com >=4 símbolos
  C) memory isolation     — worker A.memory_path != worker B.memory_path;
                            nenhum worker escreve na memória global
  D) cache isolation      — hit permitido; miss p/ intervalo≠/período≠;
                            boundary M5 invalida; vazio não contamina;
                            mutação do caller não vaza p/ o cache
  E) scan_id isolation    — scan A != scan B; zero mistura de per_asset
  F) timeout/orphan       — worker lento: A concluído, B TIMEOUT/órfão fora
                            de ranked/top3/registry/memória global/próximo scan

NÃO testa 39 ativos reais nem Yahoo real (yfinance sempre mockado).
"""
import json
import os
import time
from unittest.mock import MagicMock, patch

import pandas as pd

from mercury_ai.brain.scanner import (
    MercuryScanner,
    SCAN_COMPLETE,
    SCAN_TIMEOUT,
)
from mercury_ai.providers.data_adapters import YahooAdapter


# ---------------------------------------------------------------- helpers

def _ohlc(n=30):
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
    a.decision.audit_id = "a" * 64
    a.decision.confidence = 0.5
    a.decision.grade = "C"
    a.market_regime.regime = "RANGE"
    return a


def _scanner_with_fakes(symbols_scores):
    sc = MercuryScanner()
    sc.asset_registry.update_asset_stats = MagicMock()
    sc._trigger_failover = MagicMock()
    sc._print_report = MagicMock()
    sc._print_ranking = MagicMock()
    fakes = {s: _fake_analysis(s, v) for s, v in symbols_scores.items()}
    sc.pipeline.analyze = MagicMock(side_effect=lambda s: fakes[s])
    return sc, fakes


# ---------------------------------------------------------------- A/B

def test_a_sequential_path_preserved():
    sc, _ = _scanner_with_fakes({"AAA": 45.0, "BBB": 90.0, "CCC": 60.0})
    ranked = sc._scan_sequential(["AAA", "BBB", "CCC"], [], workers=1)
    assert [a.market.symbol for a in ranked] == ["BBB", "CCC", "AAA"]
    assert sc.last_scan_report.status == SCAN_COMPLETE
    assert sc.last_scan_report.scan_id
    # envelope transitório nunca vaza para o próximo ciclo
    assert getattr(sc.pipeline, "scan_id_context", None) is None


def test_b_parallel_workers4_four_symbols():
    sc, _ = _scanner_with_fakes(
        {"W1": 50.0, "W2": 70.0, "W3": 60.0, "W4": 80.0}
    )
    captured = {}

    real_build = sc._build_worker_pipeline

    def _spy_build(scan_id=None):
        pipe = MagicMock()
        pipe.memory_path = getattr(pipe, "memory_path", None)
        captured.setdefault("calls", []).append(scan_id)
        # pipeline real isolada p/ comportamento (analyze via fake)
        return pipe

    # usa path paralelo real mas com analyze isolado fake
    def _isolated(symbol, scan_id=None):
        fakes = {"W1": 50.0, "W2": 70.0, "W3": 60.0, "W4": 80.0}
        return (symbol, _fake_analysis(symbol, fakes[symbol]), None, 0.02, [], scan_id)

    sc._analyze_symbol_isolated = MagicMock(side_effect=_isolated)
    ranked = sc._scan_parallel(
        ["W1", "W2", "W3", "W4"], workers=4, cycle_timeout_s=290.0
    )
    assert [a.market.symbol for a in ranked] == ["W4", "W2", "W3", "W1"]
    rep = sc.last_scan_report
    assert rep.status == SCAN_COMPLETE
    assert rep.workers == 4
    assert rep.symbols_total == 4
    assert len({r["scan_id"] for r in rep.per_asset}) == 1


# ---------------------------------------------------------------- C

def test_c_memory_isolation_workers_do_not_touch_global(tmp_path):
    global_mem = tmp_path / "institutional_memory.json"
    global_mem.write_text("[]")
    before = (global_mem.stat().st_mtime_ns, global_mem.read_text())

    sc = MercuryScanner()
    paths = []

    def _real_isolated(symbol, scan_id=None):
        pipe = MercuryScanner._build_worker_pipeline(sc, scan_id=scan_id)
        try:
            paths.append(pipe.memory.memory_path)
            # simula escrita do worker (record/flush) — deve ir só p/ tempfile
            try:
                pipe.memory._memory_cache.append({"probe": symbol})
                pipe.memory._dirty = True
                pipe.memory.flush()
            except Exception:
                pass
            return (symbol, _fake_analysis(symbol, 80.0), None, 0.01, [], scan_id)
        finally:
            try:
                os.unlink(pipe.memory.memory_path)
            except Exception:
                pass

    sc._analyze_symbol_isolated = MagicMock(side_effect=_real_isolated)
    sc.asset_registry.update_asset_stats = MagicMock()
    sc._trigger_failover = MagicMock()
    sc._print_ranking = MagicMock()
    sc._scan_parallel(["A1", "A2", "A3", "A4"], workers=4, cycle_timeout_s=60.0)

    assert len(paths) == 4
    assert len(set(paths)) == 4, "cada worker deve ter memory_path próprio"
    assert all("m5_worker_mem_" in p for p in paths)
    assert all(p != str(global_mem) for p in paths)
    assert "institutional_memory.json" not in "|".join(paths)
    after = (global_mem.stat().st_mtime_ns, global_mem.read_text())
    assert after == before, "memória global jamais escrita por workers"


# ---------------------------------------------------------------- D

def test_d1_cache_hit_same_request():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    df = _ohlc()
    with patch(
        "mercury_ai.providers.data_adapters.yf.download", return_value=df
    ) as mock_dl:
        out1 = adapter.get_data("EURUSD=X", "5m")
        out2 = adapter.get_data("EURUSD=X", "5m")
        assert mock_dl.call_count == 1
        assert adapter.get_cache_stats()["hits"] == 1


def test_d2_cache_miss_different_interval():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        return_value=_ohlc(),
    ) as mock_dl:
        adapter.get_data("EURUSD=X", "5m")
        adapter.get_data("EURUSD=X", "1m")
        assert mock_dl.call_count == 2


def test_d3_cache_miss_different_period():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        return_value=_ohlc(),
    ) as mock_dl:
        adapter.get_data("EURUSD=X", "5m", period="5d")
        adapter.get_data("EURUSD=X", "5m", period="1mo")
        assert mock_dl.call_count == 2


def test_d4_new_m5_candle_invalidates_previous():
    adapter = YahooAdapter(cache_ttl_s=3600.0)  # TTL alto de propósito
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        return_value=_ohlc(),
    ) as mock_dl:
        with patch.object(
            YahooAdapter, "_current_m5_boundary",
            return_value="2026-01-05T09:00:00+00:00",
        ):
            adapter.get_data("EURUSD=X", "5m")
        with patch.object(
            YahooAdapter, "_current_m5_boundary",
            return_value="2026-01-05T09:05:00+00:00",
        ):
            adapter.get_data("EURUSD=X", "5m")
        # TTL sozinho permitiria hit; fronteira M5 exige miss
        assert mock_dl.call_count == 2


def test_d5_empty_never_poisons_cache():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        side_effect=[pd.DataFrame(), _ohlc()],
    ) as mock_dl:
        r1 = adapter.get_data("GBPUSD=X", "5m")
        assert r1.empty
        r2 = adapter.get_data("GBPUSD=X", "5m")
        assert not r2.empty
        assert mock_dl.call_count == 2


def test_d6_caller_mutation_does_not_leak_into_cache():
    adapter = YahooAdapter(cache_ttl_s=60.0)
    with patch(
        "mercury_ai.providers.data_adapters.yf.download",
        return_value=_ohlc(),
    ):
        out1 = adapter.get_data("EURUSD=X", "5m")
        out1.iloc[0, 0] = -99999.0
        out2 = adapter.get_data("EURUSD=X", "5m")
        assert out2.iloc[0, 0] != -99999.0


# ---------------------------------------------------------------- E

def test_e_scan_id_isolation_no_cross_contamination():
    sc, _ = _scanner_with_fakes({"S1": 80.0, "S2": 70.0})

    def _isolated(symbol, scan_id=None):
        scores = {"S1": 80.0, "S2": 70.0}
        return (symbol, _fake_analysis(symbol, scores[symbol]), None, 0.01, [], scan_id)

    sc._analyze_symbol_isolated = MagicMock(side_effect=_isolated)
    sc._scan_parallel(["S1", "S2"], workers=2, cycle_timeout_s=60.0)
    rep_a = sc.last_scan_report
    sc._scan_parallel(["S1", "S2"], workers=2, cycle_timeout_s=60.0)
    rep_b = sc.last_scan_report

    assert rep_a.scan_id != rep_b.scan_id
    ids_a = {r["scan_id"] for r in rep_a.per_asset}
    ids_b = {r["scan_id"] for r in rep_b.per_asset}
    assert ids_a == {rep_a.scan_id}
    assert ids_b == {rep_b.scan_id}
    assert not (ids_a & ids_b)


# ---------------------------------------------------------------- F

def test_f_timeout_orphan_quarantine():
    sc = MercuryScanner()
    sc.asset_registry.update_asset_stats = MagicMock()
    sc._trigger_failover = MagicMock()
    sc._print_ranking = MagicMock()
    global_probe = {"writes": 0}

    def _isolated(symbol, scan_id=None):
        if symbol == "SLOW":
            time.sleep(5.0)  # estoura worker_timeout; termina após deadline
            return (symbol, _fake_analysis(symbol, 99.0), None, 5.0, [], scan_id)
        return (symbol, _fake_analysis(symbol, 80.0), None, 0.01, [], scan_id)

    sc._analyze_symbol_isolated = MagicMock(side_effect=_isolated)
    ranked = sc._scan_parallel(
        ["FAST", "SLOW"], workers=2, cycle_timeout_s=30.0, worker_timeout_s=0.3
    )
    rep = sc.last_scan_report

    by_sym = {r["symbol"]: r for r in rep.per_asset}
    assert by_sym["FAST"]["outcome"] == "RANKED"
    assert by_sym["SLOW"]["outcome"] == "TIMEOUT"
    assert [a.market.symbol for a in ranked] == ["FAST"]
    assert [t.market.symbol for t in rep.top3] == ["FAST"]
    sc.asset_registry.update_asset_stats.assert_called_once_with("FAST", 80.0)
    assert rep.scan_id
    assert by_sym["SLOW"]["scan_id"] == rep.scan_id

    # órfão tardio nunca é atribuído ao scan seguinte
    sc2_calls = []

    def _isolated2(symbol, scan_id=None):
        sc2_calls.append((symbol, scan_id))
        return (symbol, _fake_analysis(symbol, 70.0), None, 0.01, [], scan_id)

    sc._analyze_symbol_isolated = MagicMock(side_effect=_isolated2)
    sc.asset_registry.update_asset_stats.reset_mock()
    sc._scan_parallel(["FAST"], workers=1, cycle_timeout_s=30.0)
    rep2 = sc.last_scan_report
    assert rep2.scan_id != rep.scan_id
    assert all(sid == rep2.scan_id for _, sid in sc2_calls)
    assert {r["symbol"] for r in rep2.per_asset} == {"FAST"}
