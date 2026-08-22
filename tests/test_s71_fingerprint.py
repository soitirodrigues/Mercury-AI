"""S7.1 — Fingerprint dataset_hash/config_hash.

- Mesmo df → mesmo dataset_hash; 1 candle adulterado → hash difere.
- Config hash estável.
- Pipeline persiste fingerprint no snapshot.
- ReplayCache com run_id distingue datasets.
"""
import pandas as pd
import numpy as np
import pytest
from unittest.mock import MagicMock

from mercury_ai.analysis.replay_fingerprint import compute_dataset_hash, compute_config_hash
from mercury_ai.analysis.replay_cache import ReplayCache


def _make_df(n=50):
    np.random.seed(7)
    dates = pd.date_range("2024-01-01", periods=n, freq="5min")
    close = 100 + np.cumsum(np.random.randn(n) * 0.5)
    return pd.DataFrame({
        "open": close - 0.2,
        "high": close + 0.3,
        "low": close - 0.3,
        "close": close,
        "volume": np.random.randint(1000, 10000, n),
    }, index=dates)


def test_dataset_hash_stable_for_same_df():
    df = _make_df()
    h1 = compute_dataset_hash(df)
    h2 = compute_dataset_hash(df)
    assert h1 == h2
    assert len(h1) == 64


def test_dataset_hash_differs_when_one_candle_altered():
    df = _make_df()
    h1 = compute_dataset_hash(df)
    df2 = df.copy()
    df2.iloc[10, df2.columns.get_loc("close")] += 50.0
    h2 = compute_dataset_hash(df2)
    assert h1 != h2


def test_dataset_hash_empty_returns_64hex():
    import pandas as pd
    df = pd.DataFrame()
    h = compute_dataset_hash(df)
    assert len(h) == 64


def test_config_hash_stable():
    h1 = compute_config_hash(weights={"a": 1.0, "b": 2.0}, version_metadata={"version": "1.0"})
    h2 = compute_config_hash(weights={"a": 1.0, "b": 2.0}, version_metadata={"version": "1.0"})
    assert h1 == h2


def test_config_hash_differs_on_weight_change():
    h1 = compute_config_hash(weights={"a": 1.0}, version_metadata={"version": "1.0"})
    h2 = compute_config_hash(weights={"a": 2.0}, version_metadata={"version": "1.0"})
    assert h1 != h2


def test_replay_cache_run_id_distinguishes_datasets():
    cache = ReplayCache(maxsize=10)
    cache.put("X", 5, "val-a", run_id="run-a")
    # Mesmo (symbol,index) mas run_id diferente → miss
    assert cache.get("X", 5, run_id="run-b") is None
    assert cache.get("X", 5, run_id="run-a") == "val-a"
    # Legado (sem run_id) não colide com chave com run_id
    cache.put("Y", 5, "legacy")
    assert cache.get("Y", 5) == "legacy"
    assert cache.get("Y", 5, run_id="run-a") is None


def test_replay_cache_legacy_still_works():
    cache = ReplayCache(maxsize=10)
    cache.put("Z", 1, "hello")
    assert cache.get("Z", 1) == "hello"
    assert cache.get("Z", 2) is None


def test_snapshot_logger_stores_fingerprint(tmp_path):
    from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
    from mercury_ai.models.decision_snapshot import DecisionSnapshot
    from mercury_ai.models.decision_result import DecisionResult
    from mercury_ai.models.version_metadata import VersionMetadata

    vm = VersionMetadata(engine_version="1.0.0", pipeline_version="1.0.0", context_version="1.0.0", weights_version="1.0.0")
    dr = DecisionResult(decision="WAIT", grade="N/A", confidence=0.0, clarity=0.0, risk_score=0.0, score=0.0,
                        quality=0.0, expected_strength=0.0, buy_probability=0.0, sell_probability=0.0,
                        wait_probability=100.0, expected_risk=0.0, expected_reward=0.0, expected_drawdown=0.0,
                        audit_id="test", version_metadata=vm, summary="s", explanation="e")
    snap = DecisionSnapshot(timestamp="2024-01-01T00:00:00", asset="TEST-ASSET", timeframe="5m",
                            context=MagicMock(), evidence_bundle=MagicMock(), decision_result=dr,
                            version_metadata=vm, audit_events=(), session_id="sess",
                            dataset_hash="abc123", config_hash="def456")
    logger = DecisionSnapshotLogger(base_path=str(tmp_path))
    logger.save(snap)
    files = [p for p in tmp_path.glob("*.json") if not p.name.startswith("backup_")]
    assert len(files) == 1
    import json
    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["dataset_hash"] == "abc123"
    assert data["config_hash"] == "def456"


def test_snapshot_logger_backward_compatible_without_fingerprint(tmp_path):
    """Snapshots antigos sem dataset_hash/config_hash continuam válidos (dict.get)."""
    from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger
    from mercury_ai.models.decision_snapshot import DecisionSnapshot
    from mercury_ai.models.decision_result import DecisionResult
    from mercury_ai.models.version_metadata import VersionMetadata

    vm = VersionMetadata(engine_version="1.0.0", pipeline_version="1.0.0", context_version="1.0.0", weights_version="1.0.0")
    dr = DecisionResult(decision="WAIT", grade="N/A", confidence=0.0, clarity=0.0, risk_score=0.0, score=0.0,
                        quality=0.0, expected_strength=0.0, buy_probability=0.0, sell_probability=0.0,
                        wait_probability=100.0, expected_risk=0.0, expected_reward=0.0, expected_drawdown=0.0,
                        audit_id="test2", version_metadata=vm, summary="s", explanation="e")
    snap = DecisionSnapshot(timestamp="2024-01-01T00:00:00", asset="TEST2", timeframe="5m",
                            context=MagicMock(), evidence_bundle=MagicMock(), decision_result=dr,
                            version_metadata=vm, audit_events=(), session_id="sess2")
    logger = DecisionSnapshotLogger(base_path=str(tmp_path))
    logger.save(snap)
    files = list(tmp_path.glob("*.json"))
    data = __import__("json").loads(files[0].read_text(encoding="utf-8"))
    # Campos existem mas vazios (default "")
    assert data.get("dataset_hash", "") == ""
    assert data.get("config_hash", "") == ""


def test_replay_storage_persists_fingerprint(tmp_path):
    from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
    from types import SimpleNamespace

    storage = ReplayStorage(output_dir=str(tmp_path))
    snap = SimpleNamespace(timestamp="2025-01-01T00:00:00Z", asset="TEST", timeframe="5m",
                           session_id="sess", decision_result=SimpleNamespace(decision="BUY", confidence=0.7, audit_id="AUD1"),
                           dataset_hash="dh123", config_hash="ch456")
    # Mock compute_replay_id_from_snapshot para não quebrar
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=0.01, hit=True)
    storage.save("AUD1", snap, metrics, run_id="run1")
    files = [p for p in tmp_path.glob("*.json") if not p.name.startswith("backup_")]
    assert len(files) == 1
    data = __import__("json").loads(files[0].read_text(encoding="utf-8"))
    assert data["dataset_hash"] == "dh123"
    assert data["config_hash"] == "ch456"
