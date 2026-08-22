"""Alertas operacionais Sprint 6 §22.

Nao esconder falhas: toda falha gera evento estruturado.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

SEVERITIES = {"INFO", "WARN", "CRITICAL"}
KINDS = {
    "DEADLINE_MISSED", "STALE_DATA", "WORKER_TIMEOUT", "WORKER_CRASH",
    "WATCHDOG_STALL", "CYCLE_OVERLAP", "DATA_GAP", "RECOVERY",
    "SHUTDOWN", "RESTART", "FRESHNESS_VIOLATION", "BOUNDED_QUEUE_FULL",
    "CYCLE_TIMEOUT", "ROLLBACK", "CLOCK_INTEGRITY_FAIL",
}

@dataclass
class AlertEvent:
    kind: str
    severity: str
    timestamp: str
    cycle_id: Optional[str]
    symbol: Optional[str] = None
    description: str = ""
    recovery_action: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AlertSink:
    def __init__(self):
        self._events: List[AlertEvent] = []

    def emit(self, kind: str, severity: str, cycle_id: Optional[str], description: str,
             symbol: Optional[str] = None, recovery_action: Optional[str] = None,
             extra: Optional[Dict[str, Any]] = None) -> AlertEvent:
        assert kind in KINDS, f"unknown kind {kind}"
        assert severity in SEVERITIES
        ev = AlertEvent(
            kind=kind, severity=severity,
            timestamp=datetime.now(timezone.utc).isoformat(),
            cycle_id=cycle_id, symbol=symbol,
            description=description, recovery_action=recovery_action, extra=extra,
        )
        self._events.append(ev)
        return ev

    @property
    def events(self) -> List[AlertEvent]:
        return list(self._events)

    def to_list(self) -> List[Dict[str, Any]]:
        return [e.to_dict() for e in self._events]
