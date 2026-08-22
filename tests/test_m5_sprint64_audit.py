"""Sprint 6.4 §21 — Audit tests: session identity, cycle identity, provenance, immutable record, correlation."""
import json, uuid, tempfile, time
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pytest

from mercury_ai.operations.m5_sprint64.audit import AuditIdentity, AuditRecord, AuditStore
from mercury_ai.operations.m5_sprint64.provenance import DecisionProvenance

def _fake_cycle_report(cycle_id="m5s64-test-0001", target="2026-09-03T10:05:00+00:00"):
    # minimal per_asset 2 symbols, one fresh one error for coverage
    return {
        "cycle_id": cycle_id,
        "target_candle": target,
        "executor_type": "process",
        "workers": 4,
        "universe": 2,
        "per_asset": {
            "EURUSD=X": {"symbol": "EURUSD=X", "status": "REAL_SIGNAL", "decision": "BUY", "audit_id": "a"*64, "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 12.3, "error": None, "trade_allowed": True, "prob_sum_ok": True, "confidence": 0.6, "confluence": 70, "grade": "B"},
            "GBPUSD=X": {"symbol": "GBPUSD=X", "status": "ERROR", "decision": "ERROR", "audit_id": "PIPELINE_ERROR", "fresh": False, "fresh_status": "ERROR", "decision_candle": None, "wall_ms": 5, "error": "boom", "trade_allowed": False},
        },
        "top3": [{"rank": 1, "symbol": "EURUSD=X", "decision": "BUY", "score": 12.3, "audit_id": "a"*64}],
        "ranked": [{"rank": 1, "symbol": "EURUSD=X", "decision": "BUY", "score": 12.3}],
        "cycle_result": "QUALIFYING_PASS",
        "next_candle_result": "QUALIFYING_PASS",
    }

def test_session_identity_unique():
    s1 = AuditIdentity.new_session()
    s2 = AuditIdentity.new_session()
    assert s1 != s2
    assert s1.startswith("m5s64-")
    assert len(s1) == len("m5s64-") + 8

def test_cycle_identity_unique():
    c1 = AuditIdentity.new_cycle()
    c2 = AuditIdentity.new_cycle()
    assert c1 != c2

def test_audit_store_immutable_no_overwrite(tmp_path):
    base = tmp_path / "reports64"
    store = AuditStore(base_dir=base, session_id="m5s64-unique123")
    r1 = store.create_session_dir()
    assert r1["created"] is True
    r2 = store.create_session_dir()
    assert r2["collision"] is True
    # ensure historical_overwrite check
    chk = store.verify_no_historical_overwrite()
    assert chk["no_historical_overwrite"] is True

def test_audit_atomic_write_collision(tmp_path):
    base = tmp_path / "reports64b"
    store = AuditStore(base_dir=base, session_id="m5s64-colltest")
    store.create_session_dir()
    rec = AuditRecord.from_cycle_report(store.session_id, _fake_cycle_report(cycle_id="cyc-001"))
    w1 = store.write_cycle_record(rec)
    assert w1["written"] is True
    w2 = store.write_cycle_record(rec)
    assert w2["written"] is False
    assert w2["collision"] is True
    assert store.check_collision_attempt("cyc-001") is True

def test_canonical_record_fields(tmp_path):
    base = tmp_path / "reports64c"
    store = AuditStore(base_dir=base, session_id="m5s64-fields")
    store.create_session_dir()
    cr = _fake_cycle_report()
    rec = AuditRecord.from_cycle_report(store.session_id, cr, clock_start_iso="2026-09-03T10:05:00+00:00")
    d = rec.to_dict()
    for k in ["session_id","cycle_id","clock_start","target_candle","target_close","next_start","executor","universe_size","assets_expected","assets_completed","fresh_assets","stale_assets","error_assets","timeout_assets","ranking_signature","decision_signature","final_decision","top3","cycle_result","per_asset"]:
        assert k in d, f"missing {k}"
    # per asset required fields
    for pa in d["per_asset"]:
        for kk in ["symbol","status","fresh","fresh_status","data_timestamp","decision_candle","analysis_status","ranking_eligible","wall_ms","error","timeout","worker_id"]:
            assert kk in pa
    assert d["ranking_signature"] is not None
    assert d["decision_signature"] is not None

def test_decision_provenance_complete(tmp_path):
    base = tmp_path / "reports64d"
    store = AuditStore(base_dir=base, session_id="m5s64-prov")
    store.create_session_dir()
    cr = _fake_cycle_report()
    rec = AuditRecord.from_cycle_report(store.session_id, cr)
    prov = DecisionProvenance.from_audit_record(rec.to_dict())
    assert prov.is_complete() is True
    assert prov.session_id == store.session_id
    assert prov.target_candle is not None

def test_event_correlation_cycle_ids(tmp_path):
    from mercury_ai.operations.m5_sprint64.events import EventStream, ObservabilityEvent
    base = tmp_path / "evttest"
    base.mkdir()
    es = EventStream(base, "m5s64-evttest")
    es.emit(ObservabilityEvent.new("CYCLE_START", "m5s64-evttest", "cycle-1", "2026-09-03T10:05:00+00:00"))
    es.emit(ObservabilityEvent.new("TARGET_SELECTED", "m5s64-evttest", "cycle-1", "2026-09-03T10:05:00+00:00"))
    es2 = EventStream(base, "m5s64-evttest")
    assert es2.count() == 2

def test_no_history_overwrite_across_sessions(tmp_path):
    base = tmp_path / "hist"
    s1 = AuditStore(base_dir=base, session_id="m5s64-a")
    s1.create_session_dir()
    rec = AuditRecord.from_cycle_report(s1.session_id, _fake_cycle_report("cyc-a"))
    s1.write_cycle_record(rec)
    s2 = AuditStore(base_dir=base, session_id="m5s64-b")
    s2.create_session_dir()
    # ensure first session file still exists and not overwritten
    assert (base / "m5s64-a" / "cycle_audit" / "cyc-a.json").exists()
    assert not (base / "m5s64-a" / "cycle_audit" / "cyc-b.json").exists()
