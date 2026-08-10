# -*- coding: utf-8 -*-
"""B4-C5 - Testes de replay com dataset timezone-aware (snapshot save).

Valida a correção R1 end-to-end: replay sobre dataset com index tz-aware
(ex.: Europe/London) faz o DeterministicClock virar tz-aware e a pipeline
salvar snapshots com timestamp ISO 8601 com offset ('+01:00'). Antes do
B4-C5 isso crashava no SnapshotLogger; agora deve salvar sem exceção,
preservar o determinismo e restaurar o clock ao final.
"""
import pytest
import pandas as pd
import numpy as np

import mercury_ai.core.analysis_pipeline as analysis_pipeline
import mercury_ai.analysis.historical_replay_engine as replay_engine_module
from mercury_ai.analysis.historical_replay_engine import HistoricalReplayEngine
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
from mercury_ai.database.replay_storage import ReplayStorage
from mercury_ai.utils.deterministic_clock import DeterministicClock

# run_replay executa pipeline.analyze() (~20+ engines) por candle.
pytestmark = pytest.mark.timeout(300)


def _make_df(tz=None):
    """DataFrame OHLCV (lowercase) com 100 candles 5min, index naive ou tz-aware."""
    np.random.seed(42)
    dates = pd.date_range("2024-01-01", periods=100, freq="5min", tz=tz)
    close = 100.0 + np.cumsum(np.random.randn(100) * 0.3)
    return pd.DataFrame({
        "open": close - 0.1,
        "high": close + 0.2,
        "low": close - 0.2,
        "close": close,
        "volume": np.random.randint(1000, 10000, 100),
    }, index=dates)


@pytest.fixture
def redirect_storage(tmp_path, monkeypatch):
    """Redireciona snapshot_logger da pipeline e ReplayStorage para tmp_path.

    Evita escrever em mercury_ai/database/snapshots e data/replay_results.
    A pipeline referencia `DecisionSnapshotLogger` como nome de módulo no
    momento da chamada, então o monkeypatch redireciona sem alterar produção.
    """
    snap_dir = tmp_path / "snapshots"
    replay_dir = tmp_path / "replay_results"
    monkeypatch.setattr(
        analysis_pipeline, "DecisionSnapshotLogger",
        lambda: DecisionSnapshotLogger(base_path=str(snap_dir))
    )
    monkeypatch.setattr(
        replay_engine_module, "ReplayStorage",
        lambda: ReplayStorage(output_dir=str(replay_dir))
    )
    return snap_dir, replay_dir


def test_replay_tz_aware_dataset_no_crash(tmp_path, redirect_storage):
    """Replay com dataset Europe/London (tz-aware) NÃO crasha no save."""
    snap_dir, replay_dir = redirect_storage
    df = _make_df(tz="Europe/London")
    assert df.index.tz is not None  # pré-condição: index é tz-aware

    engine = HistoricalReplayEngine()
    metrics = engine.run_replay("TZ-TEST", df, n_candles=5, silent=True)

    assert isinstance(metrics, list)
    assert len(metrics) > 0  # replay executou e produziu métricas

    # Snapshots foram salvos (caminho real da pipeline) SEM crash.
    snaps = sorted(snap_dir.glob("*.json"))
    assert len(snaps) > 0
    for p in snaps:
        # Filename não pode conter '+' (sanitização R1 aplicada).
        assert "+" not in p.name, f"filename não sanitizado: {p.name}"

    # Clock determinístico restaurado ao final (relógio real = None).
    assert DeterministicClock.snapshot() is None


def test_replay_naive_dataset_no_crash(tmp_path, redirect_storage):
    """Replay com dataset naive continua funcionando (não-regressão)."""
    snap_dir, replay_dir = redirect_storage
    df = _make_df(tz=None)
    assert df.index.tz is None

    engine = HistoricalReplayEngine()
    metrics = engine.run_replay("NAIVE-TEST", df, n_candles=5, silent=True)

    assert isinstance(metrics, list)
    assert len(metrics) > 0
    snaps = sorted(snap_dir.glob("*.json"))
    assert len(snaps) > 0
    assert DeterministicClock.snapshot() is None


def test_replay_tz_aware_deterministic(tmp_path, redirect_storage):
    """Replay tz-aware é determinístico (2 execuções -> mesmas métricas)."""
    snap_dir, replay_dir = redirect_storage
    df = _make_df(tz="Europe/London")

    engine = HistoricalReplayEngine()
    m1 = engine.run_replay("TZD", df, n_candles=5, silent=True)
    m2 = engine.run_replay("TZD", df, n_candles=5, silent=True)

    pl1 = [m.pl for m in m1]
    pl2 = [m.pl for m in m2]
    hit1 = [m.hit for m in m1]
    hit2 = [m.hit for m in m2]
    assert pl1 == pl2
    assert hit1 == hit2
    assert DeterministicClock.snapshot() is None
