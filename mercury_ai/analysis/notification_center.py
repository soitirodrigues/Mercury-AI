import csv
from dataclasses import dataclass, field
from typing import List, Optional
from mercury_ai.utils.deterministic_clock import DeterministicClock
from mercury_ai.utils.atomic_io import atomic_json_write

@dataclass
class Notification:
    type: str
    message: str
    timestamp: str = field(default_factory=lambda: DeterministicClock.utcnow().isoformat())

class NotificationCenter:
    """
    Camada de notificação institucional aprimorada.
    Tipos suportados: 
    - Scanner, Snapshot, Replay, Health, Erro, etc.
    """
    def __init__(self):
        self._history: List[Notification] = []

    def send(self, n_type: str, message: str):
        self._history.append(Notification(n_type, message))

    def get_history(self, filter_type: Optional[str] = None, search_text: Optional[str] = None) -> List[Notification]:
        history = self._history
        if filter_type:
            history = [n for n in history if n.type == filter_type]
        if search_text:
            history = [n for n in history if search_text.lower() in n.message.lower()]
        return history

    def export_to_json(self, filepath: str):
        atomic_json_write(filepath, [n.__dict__ for n in self._history], indent=4)

    def export_to_csv(self, filepath: str):
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['type', 'message', 'timestamp'])
            for n in self._history:
                writer.writerow([n.type, n.message, n.timestamp])
