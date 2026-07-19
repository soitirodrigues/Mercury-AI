from abc import ABC, abstractmethod
from typing import List
from dataclasses import dataclass

@dataclass(frozen=True)
class AuditEvent:
    stage_name: str
    timestamp: str

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
