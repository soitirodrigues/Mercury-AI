"""Sprint 6.4 §21 — Observability: ordering, duplicate, completeness, queue pressure, terminal."""
from pathlib import Path
import pytest
from mercury_ai.operations.m5_sprint64.events import EventStream, ObservabilityEvent, EventOrderValidator

def test_event_ordering_valid(tmp_path):
    base = tmp_path / "evt-order"
    base.mkdir()
    es = EventStream(base, "m5s64-ord")
    cid = "cycle-ord-1"
    tgt = "2026-09-03T10:05:00+00:00"
    for et in ["CYCLE_START","TARGET_SELECTED","DATA_START","DATA_COMPLETE","ANALYSIS_COMPLETE","RANKING_COMPLETE","DECISION_READY","DECISION_EMITTED"]:
        es.emit(ObservabilityEvent.new(et, "m5s64-ord", cid, tgt))
    v = EventOrderValidator(es.all()).validate()
    assert v["event_order_violation_total"] == 0
    assert v["event_total"] >= 8

def test_event_ordering_violation_detected(tmp_path):
    base = tmp_path / "evt-viol"
    base.mkdir()
    es = EventStream(base, "m5s64-viol")
    cid = "cycle-viol-1"
    tgt = "2026-09-03T10:05:00+00:00"
    # emit DECISION_EMITTED before DECISION_READY -> violation
    es.emit(ObservabilityEvent.new("CYCLE_START", "m5s64-viol", cid, tgt))
    es.emit(ObservabilityEvent.new("TARGET_SELECTED", "m5s64-viol", cid, tgt))
    es.emit(ObservabilityEvent.new("DATA_START", "m5s64-viol", cid, tgt))
    es.emit(ObservabilityEvent.new("DATA_COMPLETE", "m5s64-viol", cid, tgt))
    es.emit(ObservabilityEvent.new("RANKING_COMPLETE", "m5s64-viol", cid, tgt))  # before ANALYSIS_COMPLETE maybe? But we also test emitted before ready
    es.emit(ObservabilityEvent.new("DECISION_EMITTED", "m5s64-viol", cid, tgt))
    es.emit(ObservabilityEvent.new("DECISION_READY", "m5s64-viol", cid, tgt))
    v = EventOrderValidator(es.all()).validate()
    assert v["event_order_violation_total"] >= 1

def test_ranking_before_data_violation(tmp_path):
    base = tmp_path / "evt-rank"
    base.mkdir()
    es = EventStream(base, "m5s64-rank")
    cid = "cycle-rank-1"
    tgt = "2026-09-03T10:05:00+00:00"
    es.emit(ObservabilityEvent.new("CYCLE_START", "m5s64-rank", cid, tgt))
    es.emit(ObservabilityEvent.new("RANKING_COMPLETE", "m5s64-rank", cid, tgt))
    v = EventOrderValidator(es.all()).validate()
    assert v["event_order_violation_total"] >= 1

def test_duplicate_detection(tmp_path):
    base = tmp_path / "evt-dup"
    base.mkdir()
    es = EventStream(base, "m5s64-dup")
    e = ObservabilityEvent.new("CYCLE_START", "m5s64-dup", "cid-dup", "2026-09-03T10:05:00+00:00")
    es.emit(e)
    # manually duplicate same event_id
    import json
    line = json.dumps(e.to_dict(), ensure_ascii=False)
    with open(base / "audit_events.jsonl", "a", encoding="utf-8") as f:
        f.write(line + "\n")
    es2 = EventStream(base, "m5s64-dup")
    v = EventOrderValidator(es2.all()).validate()
    assert v["duplicate_event_total"] >= 1

def test_event_completeness(tmp_path):
    base = tmp_path / "evt-comp"
    base.mkdir()
    es = EventStream(base, "m5s64-comp")
    es.emit(ObservabilityEvent.new("CYCLE_START", "m5s64-comp", "cid-comp", "2026-09-03T10:05:00+00:00"))
    # missing TARGET_SELECTED -> loss
    v = EventOrderValidator(es.all()).validate()
    assert v["event_loss_total"] >= 1
    assert v["missing_terminal_total"] >= 1

def test_queue_pressure_event(tmp_path):
    base = tmp_path / "evt-q"
    base.mkdir()
    es = EventStream(base, "m5s64-q")
    es.emit(ObservabilityEvent.new("QUEUE_PRESSURE", "m5s64-q", "cid-q", "2026-09-03T10:05:00+00:00", details={"queue_max_depth": 128, "queue_maxsize": 128}))
    assert any(e.event_type=="QUEUE_PRESSURE" for e in es.all())

def test_terminal_events_present(tmp_path):
    base = tmp_path / "evt-term"
    base.mkdir()
    es = EventStream(base, "m5s64-term")
    cid = "cid-term"
    tgt = "2026-09-03T10:05:00+00:00"
    for et in ["CYCLE_START","TARGET_SELECTED","DATA_START","DATA_COMPLETE","DECISION_EMITTED"]:
        es.emit(ObservabilityEvent.new(et, "m5s64-term", cid, tgt))
    v = EventOrderValidator(es.all()).validate()
    assert v["missing_terminal_total"] == 0
