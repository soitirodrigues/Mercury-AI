"""Sprint 6.4 §21 — Artifact integrity + tamper/missing/partial/collision."""
import json, hashlib
from pathlib import Path
import pytest
from mercury_ai.operations.m5_sprint64.audit import AuditStore, AuditRecord
from mercury_ai.operations.m5_sprint64.artifact import ArtifactManifest, sha256_file

def _cr(cycle_id, target="2026-09-03T10:05:00+00:00"):
    return {"cycle_id": cycle_id, "target_candle": target, "executor_type": "thread", "workers": 2, "universe": 1, "per_asset": {"EURUSD=X": {"symbol": "EURUSD=X", "status": "REAL_SIGNAL", "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 10, "error": None}}, "top3": [], "ranked": [], "cycle_result": "QUALIFYING_PASS"}

def _make_manifest(tmp_path, name="m5s64-art"):
    store = AuditStore(base_dir=tmp_path, session_id=name)
    store.create_session_dir()
    for cid in ["c1","c2"]:
        rec = AuditRecord.from_cycle_report(store.session_id, _cr(cid))
        store.write_cycle_record(rec)
    m = ArtifactManifest(store.session_dir, store.session_id)
    for p in (store.session_dir / "cycle_audit").glob("*.json"):
        m.register(p)
    m.save_atomic()
    return store, m

def test_hash_verification(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-hash")
    res = m.verify()
    assert res.artifact_integrity_pass is True
    assert res.artifact_hash_mismatch_total == 0
    assert res.missing_artifact_total == 0

def test_tamper_detection(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-tamper")
    rel = list(m.entries.keys())[0]
    orig_hash = m.entries[rel].artifact_hash
    p = store.session_dir / rel
    if not p.exists():
        p = Path(m.entries[rel].artifact_path)
    data = p.read_bytes()
    p.write_bytes(data + b"X")
    res = m.verify()
    assert res.artifact_hash_mismatch_total == 1
    assert res.artifact_integrity_pass is False
    # restore
    p.write_bytes(data)
    res2 = m.verify()
    assert res2.artifact_hash_mismatch_total == 0

def test_missing_artifact(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-missing")
    # remove one file
    p = store.session_dir / "cycle_audit" / "c1.json"
    p.unlink()
    res = m.verify()
    assert res.missing_artifact_total == 1
    assert res.artifact_integrity_pass is False

def test_partial_artifact_not_accepted(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-partial")
    partial = store.session_dir / "cycle_audit" / ".partial.json"
    with open(partial, "w", encoding="utf-8") as f:
        f.write('{"incomplete":')
        f.flush()
    # manifest does not include partial; verify should flag unexpected
    res = m.verify()
    assert res.unexpected_artifact_total >= 1
    # partial not listed as valid artifact, so not accepted as complete
    assert "cycle_audit/.partial.json" not in m.entries

def test_collision_prevention(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-coll")
    rec = AuditRecord.from_cycle_report(store.session_id, _cr("c1"))
    w = store.write_cycle_record(rec)
    assert w["written"] is False
    assert w["collision"] is True

def test_unexpected_artifact_detection(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-unexp")
    extra = store.session_dir / "unexpected.txt"
    extra.write_text("hello", encoding="utf-8")
    res = m.verify()
    assert res.unexpected_artifact_total >= 1

def test_manifest_save_atomic(tmp_path):
    store, m = _make_manifest(tmp_path, "m5s64-art-atomic")
    # save again atomically should succeed
    r = m.save_atomic()
    assert r["saved"] is True
    assert (store.session_dir / "manifest.json").exists()
