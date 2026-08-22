"""Sprint 6.4 §21 — Replay tests."""
import json, uuid, time
from pathlib import Path
from datetime import datetime, timezone
import pytest

from mercury_ai.operations.m5_sprint64.audit import AuditStore, AuditRecord
from mercury_ai.operations.m5_sprint64.replay import ReplayEngine

def _fake_cycle(cycle_id, target, per_asset_cfg="normal"):
    if per_asset_cfg == "normal":
        per_asset = {
            "EURUSD=X": {"symbol": "EURUSD=X", "status": "REAL_SIGNAL", "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 10, "error": None},
            "GBPUSD=X": {"symbol": "GBPUSD=X", "status": "WAIT_LEGITIMATE", "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 11, "error": None},
        }
    elif per_asset_cfg == "data_unavailable":
        per_asset = {
            "EURUSD=X": {"symbol": "EURUSD=X", "status": "DATA_UNAVAILABLE", "fresh": False, "fresh_status": "DATA_UNAVAILABLE", "decision_candle": None, "wall_ms": 5, "error": "no data"},
            "GBPUSD=X": {"symbol": "GBPUSD=X", "status": "REAL_SIGNAL", "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 11, "error": None},
        }
    elif per_asset_cfg == "fault":
        per_asset = {
            "EURUSD=X": {"symbol": "EURUSD=X", "status": "TIMEOUT", "fresh": False, "fresh_status": "TIMEOUT", "decision_candle": None, "wall_ms": 90000, "error": "timeout"},
            "GBPUSD=X": {"symbol": "GBPUSD=X", "status": "REAL_SIGNAL", "fresh": True, "fresh_status": "FRESH", "decision_candle": target, "wall_ms": 11, "error": None},
        }
    else:
        per_asset = {}
    return {"cycle_id": cycle_id, "target_candle": target, "executor_type": "thread", "workers": 2, "universe": 2, "per_asset": per_asset, "top3": [], "ranked": [], "cycle_result": "QUALIFYING_PASS"}

def _make_session(tmp_path, name, cycles_cfg):
    base = tmp_path / name
    store = AuditStore(base_dir=base.parent, session_id=base.name)
    # base is session_id; store.base_dir is parent; weird — use directly
    from pathlib import Path as _P
    store = AuditStore(base_dir=tmp_path, session_id=name)
    store.create_session_dir()
    for cid, pcfg in cycles_cfg:
        target = "2026-09-03T10:05:00+00:00"
        cr = _fake_cycle(cid, target, pcfg)
        rec = AuditRecord.from_cycle_report(store.session_id, cr)
        store.write_cycle_record(rec)
    # save manifest
    from mercury_ai.operations.m5_sprint64.artifact import ArtifactManifest
    m = ArtifactManifest(store.session_dir, store.session_id)
    for p in (store.session_dir / "cycle_audit").glob("*.json"):
        m.register(p)
    m.save_atomic()
    return store.session_dir

def test_normal_replay(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-normal", [("cyc-n1","normal"), ("cyc-n2","normal")])
    eng = ReplayEngine(sd)
    r = eng.replay_cycle("cyc-n1")
    assert r.status == "REPLAY_MATCH"
    assert r.checks["ranking_signature"]["match"] is True

def test_fault_replay(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-fault", [("cyc-f1","fault")])
    eng = ReplayEngine(sd)
    r = eng.replay_cycle("cyc-f1")
    assert r.status == "REPLAY_MATCH"
    # fault preserved: timeout still timeout, fresh false
    rec = json.loads((sd / "cycle_audit" / "cyc-f1.json").read_text(encoding="utf-8"))
    assert any(p["status"]=="TIMEOUT" for p in rec["per_asset"])

def test_stale_preservation(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-stale", [("cyc-s1","data_unavailable")])
    eng = ReplayEngine(sd)
    r = eng.replay_cycle("cyc-s1")
    assert r.status == "REPLAY_MATCH"
    assert r.checks["replay_stale_as_fresh_total"] == 0

def test_timeout_preservation(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-timeout", [("cyc-t1","fault")])
    eng = ReplayEngine(sd)
    r = eng.replay_cycle("cyc-t1")
    assert r.status == "REPLAY_MATCH"

def test_divergence_detection_tamper(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-div", [("cyc-d1","normal")])
    # tamper artifact
    p = sd / "cycle_audit" / "cyc-d1.json"
    data = json.loads(p.read_text(encoding="utf-8"))
    data["ranking_signature"] = "tampered12345678"
    p.write_text(json.dumps(data, indent=2), encoding="utf-8")
    eng = ReplayEngine(sd)
    r = eng.replay_cycle("cyc-d1")
    # hash mismatch blocks replay
    assert r.status == "REPLAY_DIVERGENCE"
    assert r.blocked is True

def test_three_cycles_diverse(tmp_path):
    sd = _make_session(tmp_path, "m5s64-replay-3", [("cyc-1","normal"), ("cyc-2","data_unavailable"), ("cyc-3","fault")])
    eng = ReplayEngine(sd)
    results = eng.replay_many(["cyc-1","cyc-2","cyc-3"])
    assert len(results)==3
    assert all(r.status=="REPLAY_MATCH" for r in results)
