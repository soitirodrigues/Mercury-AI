from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass


@dataclass(frozen=True)
class AuditEvent:
    stage_name: str
    timestamp: str
    success: bool = True
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    duration_ms: Optional[float] = None


class AuditSink(ABC):
    @abstractmethod
    def log(self, event: AuditEvent):
        pass


class MemoryAuditSink(AuditSink):
    def __init__(self):
        self._events: List[AuditEvent] = []

    def log(self, event: AuditEvent):
        self._events.append(event)

    def get_events(self) -> List[AuditEvent]:
        return self._events

    def get_failed_events(self) -> List[AuditEvent]:
        """Retorna apenas eventos de falha para diagnóstico."""
        return [e for e in self._events if not e.success]
