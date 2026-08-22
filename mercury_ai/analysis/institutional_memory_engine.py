import json
import os
import hashlib
import threading
import logging
import tempfile
import time
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
        # Modo isolado Sprint4 (FROZEN_EQUIVALENCE_ISOLATED): cada pipeline pode pedir
        # memória isolada via memory_path distinto. Nesse modo NÃO usar singleton:
        # cria instância própria sem polluir _instance global.
        isolated = os.environ.get("FROZEN_EQUIVALENCE_ISOLATED") == "1"
        if isolated and memory_path != "data/institutional_memory.json":
            # Bypass singleton — instância isolada por pipeline
            self.memory_path = memory_path
            self._memory_cache = []
            self._dirty = False
            self._initialized = True
            if not os.path.exists(self.memory_path):
                self._initialize_memory()
            self._load_into_cache()
            return
        # Caminho normal: singleton
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
        """Persiste o cache em RAM para o disco de forma atômica.

        Sprint 5 — hardening cross-process:
          - filelock (se instalado) para serializar escritores concorrentes
            (ProcessPool). Sem filelock, cai no fallback atômico por processo.
          - Operação ainda protegida por _lock (thread-safe intra-processo).
        """
        with self._lock:
            if not self._dirty:
                return

            # Tenta adquirir lock inter-processo (filelock) se disponível.
            _flock = None
            try:
                import filelock  # optional dep
                lock_path = f"{self.memory_path}.lock"
                _flock = filelock.FileLock(lock_path, timeout=5)
                _flock.acquire()
            except ImportError:
                _flock = None
            except Exception:
                _flock = None

            try:
                # Reconcilia: re-ler disco antes de escrever para não sobrescrever
                # decisões gravadas por outro processo entre o load inicial e o flush.
                try:
                    with open(self.memory_path, 'r') as _f:
                        _disk = json.load(_f)
                    # Merge por audit_id: preserva entradas de disco não presentes no cache
                    _existing_ids = {e.get('audit_id') for e in self._memory_cache if isinstance(e, dict) and 'audit_id' in e}
                    for _entry in _disk:
                        if isinstance(_entry, dict) and _entry.get('audit_id') not in _existing_ids:
                            self._memory_cache.append(_entry)
                    _existing_ids = None
                except Exception:
                    pass

                temp_path = f"{self.memory_path}.tmp"
                # mkstemp atômico no mesmo diretório
                fd, tmp = tempfile.mkstemp(suffix=".tmp", prefix=".mem_", dir=os.path.dirname(self.memory_path) or ".")
                try:
                    with os.fdopen(fd, 'w', encoding="utf-8") as f:
                        json.dump(self._memory_cache, f, indent=4)
                        f.flush()
                        try:
                            os.fsync(f.fileno())
                        except Exception:
                            pass
                    max_retries = 5
                    for i in range(max_retries):
                        try:
                            os.replace(tmp, self.memory_path)
                            self._dirty = False
                            return
                        except OSError as e:
                            if i == max_retries - 1:
                                raise e
                            time.sleep(0.05 * (2 ** i))
                except Exception:
                    try:
                        os.unlink(tmp)
                    except Exception:
                        pass
                    raise
            except (OSError, json.JSONDecodeError, TypeError, ValueError) as e:
                logger.error(f"Critical failure flushing institutional memory: {e}", exc_info=True)
                raise e
            finally:
                if _flock is not None:
                    try:
                        _flock.release()
                    except Exception:
                        pass

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
        Analisa o histórico e retorna um fator de reforço (0.0 a 1.0).

        Quando não há dados suficientes (sem histórico ou sem outcomes
        registrados), retorna 0.5 — valor neutro que não penaliza nem
        reforça a decisão.  Quando há histórico, calcula a média dos
        outcomes ajustada pela variância (penalizando setups instáveis).
        """
        # Valor neutro quando não há dados suficientes para avaliar.
        NEUTRAL_SCORE = 0.5

        setup_key = self._get_setup_key(asset, evidences)

        with self._lock:
            memory = self._load_memory()

        history = [m for m in memory if m['setup_key'] == setup_key]
        if not history:
            return NEUTRAL_SCORE

        outcomes = [m['outcome'] for m in history if 'outcome' in m]
        if not outcomes:
            return NEUTRAL_SCORE

        # Reforça sucesso, penaliza falha
        avg_outcome = sum(outcomes) / len(outcomes)

        # Penality for high variance (instability)
        variance = sum((o - avg_outcome) ** 2 for o in outcomes) / len(outcomes)

        raw_score = avg_outcome - (variance * 0.5)

        # Garante que o score fique no intervalo [0.0, 1.0].
        # Se o cálculo resultar em valor <= 0 (setup muito instável),
        # usamos o neutro 0.5 como piso de segurança.
        if raw_score <= 0.0:
            return NEUTRAL_SCORE

        return max(0.0, min(1.0, raw_score))

    def record_decision(self, snapshot: DecisionSnapshot):
        setup_key = self._get_setup_key(snapshot.asset, snapshot.evidence_bundle.evidences)
        
        entry = {
            'setup_key': setup_key,
            'audit_id': snapshot.decision_result.audit_id,
        'replay_id': getattr(snapshot, 'replay_id', ''),
            'timestamp': snapshot.timestamp
        }
        
        with self._lock:
            memory = self._load_memory()
            memory.append(entry)
            self._save_memory(memory)

    def record_outcome(self, audit_id: str, outcome: float, replay_id: str = ""):
        with self._lock:
            memory = self._load_memory()
            for entry in memory:
                if entry['audit_id'] == audit_id and (
                    not replay_id or entry.get('replay_id', '') == replay_id
                ):
                    entry['outcome'] = outcome
            self._save_memory(memory)
