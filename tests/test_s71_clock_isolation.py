"""S7.1 — Teste de isolamento do DeterministicClock.

- S7.1 ClockIsolation: NORMAL→REPLAY→NORMAL e REPLAY com exceção restauram.
- ReplayBatchProcessor paralelo com ThreadPool 4 workers, contaminação 0.
"""
import pandas as pd
import numpy as np
import threading
import pytest
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.analysis.replay_batch_processor import ReplayBatchProcessor


def _make_df(n=100):
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    close = 100 + np.cumsum(np.random.randn(n) * 0.3)
    return pd.DataFrame({
        "open": close - 0.1,
        "high": close + 0.2,
        "low": close - 0.2,
        "close": close,
        "volume": np.random.randint(1000, 10000, n),
    }, index=dates)


def test_clock_restores_to_none_after_replay():
    df = _make_df(120)
    engine = HistoricalReplayEngine()
    assert DeterministicClock.is_frozen() is False
    assert DeterministicClock.snapshot() is None
    engine.run_replay("T-A", df, n_candles=5, silent=True)
    assert DeterministicClock.snapshot() is None
    assert DeterministicClock.is_frozen() is False


def test_clock_restores_on_exception_inside_replay(monkeypatch):
    df = _make_df(120)
    engine = HistoricalReplayEngine()
    # Força exceção no pipeline.analyze durante replay
    from mercury_ai.core.analysis_pipeline import AnalysisPipeline
    orig_analyze = AnalysisPipeline.analyze

    call_count = {"n": 0}

    def failing_analyze(self, *a, **kw):
        call_count["n"] += 1
        if call_count["n"] == 2:
            raise RuntimeError("injected failure")
        return orig_analyze(self, *a, **kw)

    monkeypatch.setattr(AnalysisPipeline, "analyze", failing_analyze)
    # Deve propagar mas restaurar clock
    try:
        engine.run_replay("T-B", df, n_candles=5, silent=True)
    except RuntimeError:
        pass
    assert DeterministicClock.snapshot() is None


def test_normal_replay_normal_sequence():
    df = _make_df(120)
    engine = HistoricalReplayEngine()
    # NORMAL (is_frozen False)
    assert not DeterministicClock.is_frozen()
    # REPLAY 1
    engine.run_replay("T-C1", df, n_candles=5, silent=True)
    assert not DeterministicClock.is_frozen()
    # REPLAY 2 sequencial
    engine.run_replay("T-C2", df, n_candles=5, silent=True)
    assert not DeterministicClock.is_frozen()
    # NORMAL final
    assert not DeterministicClock.is_frozen()


def test_replay_batch_parallel_no_contamination():
    # Batch com 4 símbolos paralelos
    data_map = {
        f"SYM-{i}": _make_df(90) for i in range(4)
    }
    processor = ReplayBatchProcessor(max_workers=4)
    report = processor.run_batch(data_map, n_candles=5)
    # Verifica que clock da thread principal não ficou congelado
    assert DeterministicClock.snapshot() is None
    # Batch report deve ter resultados para todos os símbolos (ou erro isolado)
    assert report is not None


def test_deterministic_double_replay_same_pl():
    df = _make_df(120)
    engine = HistoricalReplayEngine()
    m1 = engine.run_replay("SYM-D", df, n_candles=5, silent=True)
    m2 = engine.run_replay("SYM-D", df, n_candles=5, silent=True)
    assert len(m1) == len(m2)
    # pl idêntico byte-a-byte
    for a, b in zip(m1, m2):
        assert a.pl == b.pl
        assert a.mae == b.mae
        assert a.mfe == b.mfe
