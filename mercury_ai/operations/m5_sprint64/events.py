"""Sprint 6.4 — OBSERVABILITY EVENT STREAM + ORDERING & TEMPORAL INTEGRITY."""
from __future__ import annotations
import json, uuid, tempfile, os
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional
from enum import Enum

class EventType(str, Enum):
    SESSION_START = "SESSION_START"
    CYCLE_START = "CYCLE_START"
    TARGET_SELECTED = "TARGET_SELECTED"
    DATA_START = "DATA_START"
    DATA_COMPLETE = "DATA_COMPLETE"
    DATA_ERROR = "DATA_ERROR"
    DATA_TIMEOUT = "DATA_TIMEOUT"
    DATA_UNAVAILABLE = "DATA_UNAVAILABLE"
    WORKER_START = "WORKER_START"
    WORKER_COMPLETE = "WORKER_COMPLETE"
    WORKER_CRASH = "WORKER_CRASH"
    WORKER_TIMEOUT = "WORKER_TIMEOUT"
    WORKER_RESTART = "WORKER_RESTART"
    QUEUE_PRESSURE = "QUEUE_PRESSURE"
    WATCHDOG_STALL = "WATCHDOG_STALL"
    WATCHDOG_RECOVERY = "WATCHDOG_RECOVERY"
    ANALYSIS_COMPLETE = "ANALYSIS_COMPLETE"
    RANKING_COMPLETE = "RANKING_COMPLETE"
    DECISION_READY = "DECISION_READY"
    DECISION_EMITTED = "DECISION_EMITTED"
    REPLAY_START = "REPLAY_START"
    REPLAY_COMPLETE = "REPLAY_COMPLETE"
    REPLAY_DIVERGENCE = "REPLAY_DIVERGENCE"
    SESSION_COMPLETE = "SESSION_COMPLETE"
    SESSION_INTERRUPTED = "SESSION_INTERRUPTED"
    AUDIT_COLLISION = "AUDIT_COLLISION"
    ARTIFACT_WRITTEN = "ARTIFACT_WRITTEN"

# Valid logical order for per-cycle flow (allow extra events interleaved but enforce precedence)
VALID_ORDER = [
    "CYCLE_START",          # 0
    "TARGET_SELECTED",      # 1
    "DATA_START",           # 2
    "DATA_COMPLETE",        # 3 (or DATA_ERROR/DATA_TIMEOUT/DATA_UNAVAILABLE — any terminal data)
    "ANALYSIS_COMPLETE",    # 4
    "RANKING_COMPLETE",     # 5
    "DECISION_READY",       # 6
    "DECISION_EMITTED",     # 7
]
DATA_TERMINALS = {"DATA_COMPLETE", "DATA_ERROR", "DATA_TIMEOUT", "DATA_UNAVAILABLE"}
TERMINAL_EVENTS = {"DECISION_EMITTED", "SESSION_INTERRUPTED", "SESSION_COMPLETE"}

@dataclass
class ObservabilityEvent:
    event_id: str
    event_type: str
    timestamp: str
    session_id: str
    cycle_id: Optional[str]
    target_candle: Optional[str]
    asset: Optional[str] = None
    worker_id: Optional[str] = None
    incident_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @staticmethod
    def new(event_type: str, session_id: str, cycle_id: Optional[str] = None, target_candle: Optional[str] = None, asset: Optional[str]=None, worker_id: Optional[str]=None, incident_id: Optional[str]=None, details: Optional[Dict[str,Any]]=None) -> "ObservabilityEvent":
        return ObservabilityEvent(
            event_id=f"evt-{uuid.uuid4().hex[:8]}",
            event_type=event_type,
            timestamp=datetime.now(timezone.utc).isoformat(),
            session_id=session_id,
            cycle_id=cycle_id,
            target_candle=target_candle,
            asset=asset,
            worker_id=worker_id,
            incident_id=incident_id,
            details=details or {},
        )

class EventStream:
    """Persisted JSONL event stream per session (atomic append)."""
    def __init__(self, session_dir: Path, session_id: str):
        self.session_dir = Path(session_dir)
        self.session_id = session_id
        self.path = self.session_dir / "audit_events.jsonl"
        self._events: List[ObservabilityEvent] = []
        self._load()

    def _load(self):
        if not self.path.exists():
            return
        try:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    d = json.loads(line)
                    self._events.append(ObservabilityEvent(**d))
        except Exception:
            pass

    def emit(self, event: ObservabilityEvent):
        self._events.append(event)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        # atomic append via write to temp then rename? For JSONL we just append line-wise with flush+fsync
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False, default=str) + "\n")
            f.flush()
            try:
                os.fsync(f.fileno())
            except:
                pass

    def all(self) -> List[ObservabilityEvent]:
        return list(self._events)

    def count(self) -> int:
        return len(self._events)

class EventOrderValidator:
    """Validates ordering logic per cycle_id."""
    def __init__(self, events: List[ObservabilityEvent]):
        self.events = events

    def validate(self) -> Dict[str, Any]:
        violations = []
        # group by cycle_id
        from collections import defaultdict
        by_cycle: Dict[str, List[ObservabilityEvent]] = defaultdict(list)
        for e in self.events:
            if e.cycle_id:
                by_cycle[e.cycle_id].append(e)
        # order map
        order_index = {k: i for i, k in enumerate(VALID_ORDER)}
        # For DATA terminals, map to same index as DATA_COMPLETE
        for t in DATA_TERMINALS:
            order_index[t] = order_index["DATA_COMPLETE"]

        for cycle_id, evts in by_cycle.items():
            # sorted by timestamp
            try:
                sorted_evts = sorted(evts, key=lambda x: x.timestamp)
            except:
                sorted_evts = evts
            last_idx = -1
            seen_types = set()
            for e in sorted_evts:
                et = e.event_type
                # detect duplicate events: same event_id duplicate? event_id should be unique
                if et not in order_index:
                    continue  # non-ordered events (WATCHDOG, QUEUE_PRESSURE, WORKER_*) are allowed anywhere
                idx = order_index[et]
                if idx < last_idx:
                    violations.append({"cycle_id": cycle_id, "violation": f"{et} before earlier stage", "last_idx": last_idx, "current_idx": idx})
                else:
                    last_idx = idx
                # specific rule checks
                # DECISION_EMITTED before DECISION_READY
                if et == "DECISION_EMITTED" and "DECISION_READY" not in [x.event_type for x in sorted_evts[:sorted_evts.index(e)]]:
                    violations.append({"cycle_id": cycle_id, "violation": "DECISION_EMITTED before DECISION_READY"})
                if et == "RANKING_COMPLETE":
                    # must have some DATA terminal before
                    prefix = [x.event_type for x in sorted_evts[:sorted_evts.index(e)]]
                    if not any(t in prefix for t in DATA_TERMINALS):
                        violations.append({"cycle_id": cycle_id, "violation": "RANKING_COMPLETE before DATA_COMPLETE/ERROR"})

        # duplicate detection: event_id duplicates
        ids = [e.event_id for e in self.events]
        duplicate_event_total = len(ids) - len(set(ids))
        # also detect logical duplicate: same cycle_id+event_type+asset repeated identical timestamp? Simple: count same tuple
        dup_logical = 0
        seen_tuple = {}
        for e in self.events:
            key = (e.cycle_id, e.event_type, e.asset, e.timestamp)
            if key in seen_tuple:
                dup_logical += 1
            else:
                seen_tuple[key] = 1
        # terminal event check: each CYCLE_START should have a terminal
        missing_terminal = 0
        for cycle_id, evts in by_cycle.items():
            types = {x.event_type for x in evts}
            if "CYCLE_START" in types and not any(t in types for t in TERMINAL_EVENTS):
                missing_terminal += 1
        # event loss: gap in sequence? We consider loss if expected ordered events missing
        event_loss_total = 0
        for cycle_id, evts in by_cycle.items():
            types = {x.event_type for x in evts}
            if "CYCLE_START" in types and "TARGET_SELECTED" not in types:
                event_loss_total += 1
        return {
            "event_order_violation_total": len(violations),
            "violations": violations,
            "duplicate_event_total": duplicate_event_total,
            "duplicate_logical_total": dup_logical,
            "missing_terminal_total": missing_terminal,
            "event_loss_total": event_loss_total,
            "event_total": len(self.events),
        }
