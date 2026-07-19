import uuid
from mercury_ai.config import settings
from mercury_ai.utils.deterministic_clock import DeterministicClock

class SessionManager:
    """
    Gerenciador de metadados institucionais de sessão.
    """
    def __init__(self, operator: str = settings.OPERATOR):
        self.session_id = str(uuid.uuid4())
        self.operator = operator
        self.version = settings.VERSION
        self.environment = "DEMO" if settings.READ_ONLY else "REAL"
        self.timestamp = DeterministicClock.utcnow().isoformat()
    
    def get_info(self) -> dict:
        return {
            "session_id": self.session_id,
            "operator": self.operator,
            "version": self.version,
            "environment": self.environment,
            "timestamp": self.timestamp
        }
