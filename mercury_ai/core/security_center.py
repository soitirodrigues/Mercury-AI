from dataclasses import dataclass, field
from typing import List, Dict, Any
from mercury_ai.utils.deterministic_clock import DeterministicClock

@dataclass
class AuditEvent:
    user: str
    action: str
    target: str
    severity: str
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())

class SecurityCenter:
    """
    Central de auditoria e segurança institucional.
    """
    def __init__(self):
        self._audit_trail: List[AuditEvent] = []

    def log_event(self, user: str, action: str, target: str, severity: str = "INFO"):
        event = AuditEvent(user=user, action=action, target=target, severity=severity)
        self._audit_trail.append(event)

    def generate_audit_trail(self) -> List[Dict[str, Any]]:
        return [e.__dict__ for e in self._audit_trail]

    def generate_security_report(self) -> Dict[str, Any]:
        # Simple analysis
        critical_count = len([e for e in self._audit_trail if e.severity == "CRITICAL"])
        return {
            "total_events": len(self._audit_trail),
            "critical_events": critical_count,
            "status": "SECURE" if critical_count == 0 else "WARNING"
        }
