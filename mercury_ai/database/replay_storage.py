from dataclasses import dataclass
from typing import Any, Dict
import json
import logging
import os
import re
import threading

from mercury_ai.database.snapshot_logger import compute_replay_id_from_snapshot, snapshot_filename_for
from mercury_ai.utils.atomic_io import atomic_json_write

logger = logging.getLogger(__name__)

# Regex whitelist para nomes de arquivo: letras, números, ponto, hífen, underscore.
# Rejeita path traversal (../, ..\, /, \) e caracteres especiais.
_SAFE_REPLAY_RE = re.compile(r"^[A-Za-z0-9._\-]+$")


def _sanitize_audit_id(audit_id: str) -> str:
    """Sanitiza audit_id contra path traversal antes de usá-lo em nome de arquivo.

    - Rejeita strings vazias.
    - Substitui ':' por '-' (timestamps ISO).
    - Rejeita path traversal explícito (.., /, \\).
    - Rejeita caracteres fora do whitelist.
    """
    if not audit_id:
        raise ValueError("audit_id não pode ser vazio.")
    safe = audit_id.replace(":", "-")
    if ".." in safe or "/" in safe or "\\" in safe:
        raise ValueError(f"audit_id inválido (path traversal): {audit_id!r}")
    if not _SAFE_REPLAY_RE.match(safe):
        raise ValueError(f"audit_id contém caracteres não permitidos: {audit_id!r}")
    return safe


@dataclass(frozen=True)
class ReplayMetrics:
    mae: float
    mfe: float
    pl: float
    hit: bool


class ReplayStorage:
    """Armazenamento de resultados de replay com escrita atômica e thread-safe.

    Correções aplicadas:
      - C2: threading.Lock protege operações de save (thread-safe).
      - C3: audit_id sanitizado contra path traversal antes de construir nome de arquivo.
    """

    def __init__(self, output_dir: str = "data/replay_results"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._lock = threading.Lock()

    def _existing_file_matches(self, filepath: str, new_data: Dict[str, Any]) -> bool:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            return False
        return existing == new_data

    def save(self, audit_id: str, snapshot: Any, metrics: ReplayMetrics, run_id: str = ""):
        safe_audit_id = _sanitize_audit_id(audit_id)
        replay_id = compute_replay_id_from_snapshot(snapshot)
        # run_id/execution_id (B5-C4): distingue execuções independentes do mesmo
        # snapshot (ex.: mesmo candle com janela forward diferente). Quando vazio,
        # mantém o contrato legado de um único arquivo por (audit_id, replay_id).
        safe_run_id = _sanitize_audit_id(run_id) if run_id else ""
        run_suffix = f"_{safe_run_id}" if safe_run_id else ""
        filepath = f"{self.output_dir}/{safe_audit_id}_{replay_id}{run_suffix}.json"
        data = {
            "audit_id": audit_id,
            "replay_id": replay_id,
            "run_id": run_id,
            "snapshot_filename": snapshot_filename_for(snapshot),
            "session_id": getattr(snapshot, "session_id", ""),
            "asset": getattr(snapshot, "asset", ""),
            "timeframe": getattr(snapshot, "timeframe", ""),
            "timestamp": snapshot.timestamp,
            "decision": snapshot.decision_result.decision,
            "confidence": snapshot.decision_result.confidence,
            "mae": metrics.mae,
            "mfe": metrics.mfe,
            "pl": metrics.pl,
            "hit": metrics.hit,
        }
        with self._lock:
            if os.path.exists(filepath):
                if self._existing_file_matches(filepath, data):
                    logger.info(
                        "ReplayStorage.save: replay result for replay_id=%s run_id=%s already exists and is identical; skipping write.",
                        replay_id,
                        run_id or "-",
                    )
                    return
                raise ValueError(
                    f"ReplayStorage.save: duplicate replay identity detected for replay_id={replay_id} run_id={run_id or '-'} audit_id={audit_id}"
                )
            atomic_json_write(
                filepath,
                data,
                indent=4,
            )
