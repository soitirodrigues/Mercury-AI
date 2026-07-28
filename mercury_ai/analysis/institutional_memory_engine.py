import json
import os
import hashlib
import threading
import logging
from mercury_ai.models.decision_snapshot import DecisionSnapshot

logger = logging.getLogger(__name__)

class InstitutionalMemoryEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(InstitutionalMemoryEngine, cls).__new__(cls)
            return cls._instance

    def __init__(self, memory_path: str = "data/institutional_memory.json"):
        # Use a lock to ensure initialization happens only once
        with self._lock:
            if hasattr(self, '_initialized'):
                return
            self.memory_path = memory_path
            self._memory_cache = []
            self._dirty = False
            if not os.path.exists(self.memory_path):
                self._initialize_memory()
            self._load_into_cache()
            self._initialized = True

    def _load_into_cache(self):
        """Carrega a memória do disco para o cache em RAM."""
        try:
            with open(self.memory_path, 'r') as f:
                self._memory_cache = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Institutional memory corrupted or inaccessible: {e}. Resetting memory.")
            self._initialize_memory()
            self._memory_cache = []

    def _initialize_memory(self):
        """Cria o arquivo de memória se não existir ou estiver corrompido."""
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)
        with open(self.memory_path, 'w') as f:
            json.dump([], f)

    def flush(self):
        """Persiste o cache em RAM para o disco de forma atômica."""
        with self._lock:
            if not self._dirty:
                return
            
            temp_path = f"{self.memory_path}.tmp"
            try:
                with open(temp_path, 'w') as f:
                    json.dump(self._memory_cache, f, indent=4)
                
                max_retries = 5
                for i in range(max_retries):
                    try:
                        os.replace(temp_path, self.memory_path)
                        self._dirty = False
                        return
                    except OSError as e:
                        if i == max_retries - 1:
                            raise e
                        import time
                        time.sleep(0.05 * (2 ** i)) # Backoff exponencial: 0.05, 0.1, 0.2...
            except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Critical failure flushing institutional memory: {e}", exc_info=True)
                raise e

    def _load_memory(self) -> list:
        """Mantido para compatibilidade, mas agora retorna o cache."""
        return self._memory_cache

    def _save_memory(self, memory: list):
        """Mantido para compatibilidade, mas agora apenas atualiza o cache."""
        self._memory_cache = memory
        self._dirty = True
        # REMOVIDO: Chamada automática ao flush() para evitar conflitos de I/O no Windows durante processamento paralelo.
        # A persistência agora é controlada exclusivamente via flush() explícito.

    def _get_setup_key(self, asset: str, evidences: tuple) -> str:
        # Deterministic hash of setup
        setup = sorted([f"{e.engine_name}_{e.evidence_name}_{e.direction}" for e in evidences])
        return hashlib.sha256(f"{asset}_{'_'.join(setup)}".encode()).hexdigest()

    def get_consistency_score(self, asset: str, evidences: tuple) -> float:
        """
        Analisa o histórico e retorna um fator de reforço (-1.0 a 1.0).
        """
        setup_key = self._get_setup_key(asset, evidences)
        
        with self._lock:
            memory = self._load_memory()
            
        history = [m for m in memory if m['setup_key'] == setup_key]
        if not history:
            return 0.0
            
        outcomes = [m['outcome'] for m in history if 'outcome' in m]
        if not outcomes:
            return 0.0
            
        # Reforça sucesso, penaliza falha
        avg_outcome = sum(outcomes) / len(outcomes)
        
        # Penality for high variance (instability)
        variance = sum((o - avg_outcome)**2 for o in outcomes) / len(outcomes)
        
        return avg_outcome - (variance * 0.5)

    def record_decision(self, snapshot: DecisionSnapshot):
        setup_key = self._get_setup_key(snapshot.asset, snapshot.evidence_bundle.evidences)
        
        entry = {
            'setup_key': setup_key,
            'audit_id': snapshot.decision_result.audit_id,
            'asset': snapshot.asset,
            'decision': snapshot.decision_result.decision,
            'confidence': snapshot.decision_result.confidence,
            'timestamp': snapshot.timestamp
        }
        
        with self._lock:
            memory = self._load_memory()
            memory.append(entry)
            self._save_memory(memory)

    def record_outcome(self, audit_id: str, outcome: float):
        with self._lock:
            memory = self._load_memory()
            for entry in memory:
                if entry['audit_id'] == audit_id:
                    entry['outcome'] = outcome
            self._save_memory(memory)
