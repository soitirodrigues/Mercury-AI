from __future__ import annotations

import json
import os
import threading
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from mercury_ai.utils.atomic_io import atomic_json_write
from mercury_ai.utils.deterministic_clock import DeterministicClock


@dataclass
class AuditEvent:
    user: str
    action: str
    target: str
    severity: str
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user": self.user,
            "action": self.action,
            "target": self.target,
            "severity": self.severity,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AuditEvent":
        return cls(
            user=data["user"],
            action=data["action"],
            target=data["target"],
            severity=data["severity"],
            timestamp=data["timestamp"],
        )


class SecurityCenter:
    """
    Central de auditoria e segurança institucional.

    Persiste o audit trail em disco de forma atômica (crash-safe) usando
    ``mercury_ai.utils.atomic_io.atomic_json_write``. O trail é carregado
    na inicialização (se o arquivo existir) e salvo a cada ``log_event``.
    """

    def __init__(self, state_path: str = "data/audit_trail.json"):
        self._state_path = state_path
        self._audit_trail: List[AuditEvent] = []
        self._lock = threading.Lock()
        self._load()

    def _load(self) -> None:
        """Carrega o audit trail do disco, se o arquivo existir."""
        if not self._state_path or not os.path.exists(self._state_path):
            return
        try:
            with open(self._state_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list):
                self._audit_trail = [AuditEvent.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            # Arquivo corrompido ou incompatível — começa com trail vazio
            self._audit_trail = []

    def _save(self) -> None:
        """Persiste o audit trail em disco de forma atômica."""
        if not self._state_path:
            return
        payload = [e.to_dict() for e in self._audit_trail]
        atomic_json_write(self._state_path, payload)

    def log_event(self, user: str, action: str, target: str, severity: str = "INFO"):
        event = AuditEvent(user=user, action=action, target=target, severity=severity)
        with self._lock:
            self._audit_trail.append(event)
            self._save()

    def generate_audit_trail(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [e.to_dict() for e in self._audit_trail]

    def generate_security_report(self) -> Dict[str, Any]:
        with self._lock:
            critical_count = len([e for e in self._audit_trail if e.severity == "CRITICAL"])
            return {
                "total_events": len(self._audit_trail),
                "critical_events": critical_count,
                "status": "SECURE" if critical_count == 0 else "WARNING"
            }
