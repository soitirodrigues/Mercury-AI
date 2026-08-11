import json
import logging
from types import SimpleNamespace

import pytest

from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics


def _make_snapshot(audit_id: str):
    return SimpleNamespace(
        timestamp="2025-01-01T00:00:00Z",
        asset="TEST-ASSET",
        timeframe="5m",
        session_id="TEST-SESSION",
        decision_result=SimpleNamespace(
            decision="BUY",
            confidence=0.75,
            audit_id=audit_id,
        ),
    )


def test_replay_storage_overwrite_logs_warning(tmp_path, caplog):
    storage = ReplayStorage(output_dir=str(tmp_path))
    audit_id = "TEST-AUDIT"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.0, hit=True)
    snapshot = _make_snapshot(audit_id)

    with caplog.at_level(logging.INFO, logger="mercury_ai.database.replay_storage"):
        storage.save(audit_id, snapshot, metrics)
        storage.save(audit_id, snapshot, metrics)

    assert any(
        "already exists and is identical" in record.message
        for record in caplog.records
    )


def test_replay_storage_file_written(tmp_path):
    storage = ReplayStorage(output_dir=str(tmp_path))
    audit_id = "TEST-AUDIT-2"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.0, hit=False)
    snapshot = _make_snapshot(audit_id)

    storage.save(audit_id, snapshot, metrics)
    files = list(tmp_path.glob("*.json"))
    assert len(files) == 1

    data = json.loads(files[0].read_text(encoding="utf-8"))
    assert data["audit_id"] == audit_id
    assert data["hit"] is False
    assert "replay_id" in data
    assert data["session_id"] == snapshot.session_id
    assert data["snapshot_filename"].endswith(".json")


def test_replay_storage_replay_id_duplicate_rejects_different_content(tmp_path):
    storage = ReplayStorage(output_dir=str(tmp_path))
    audit_id = "TEST-DUPLICATE"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.0, hit=False)
    snapshot = _make_snapshot(audit_id)

    # first save should succeed
    storage.save(audit_id, snapshot, metrics)

    # second save of same replay identity with altered metrics should raise
    metrics_changed = ReplayMetrics(mae=0.1, mfe=0.2, pl=2.0, hit=True)
    with pytest.raises(ValueError, match="duplicate replay identity"):
        storage.save(audit_id, snapshot, metrics_changed)
