import json
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.direction import AnalysisDirection


def _make_snapshot(audit_id: str):
    snapshot = MagicMock()
    snapshot.decision_result.decision = "BUY"
    snapshot.decision_result.confidence = 0.75
    snapshot.timestamp = "2025-01-01T00:00:00Z"
    snapshot.decision_result.audit_id = audit_id
    return snapshot


def test_replay_storage_overwrite_logs_warning(tmp_path, caplog):
    storage = ReplayStorage(output_dir=str(tmp_path))
    audit_id = "TEST-AUDIT"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.0, hit=True)
    snapshot = _make_snapshot(audit_id)

    storage.save(audit_id, snapshot, metrics)
    storage.save(audit_id, snapshot, metrics)

    assert any(
        "overwriting existing replay_result" in record.message
        for record in caplog.records
    )


def test_replay_storage_file_written(tmp_path):
    storage = ReplayStorage(output_dir=str(tmp_path))
    audit_id = "TEST-AUDIT-2"
    metrics = ReplayMetrics(mae=0.1, mfe=0.2, pl=1.0, hit=False)
    snapshot = _make_snapshot(audit_id)

    storage.save(audit_id, snapshot, metrics)
    path = tmp_path / f"{audit_id}.json"
    assert path.exists()

    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["audit_id"] == audit_id
    assert data["hit"] is False
