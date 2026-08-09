from dataclasses import dataclass
from typing import Any
import os
import re
import threading

from mercury_ai.utils.atomic_io import atomic_json_write

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

    def save(self, audit_id: str, snapshot: Any, metrics: ReplayMetrics):
        safe_audit_id = _sanitize_audit_id(audit_id)
        data = {
            "audit_id": audit_id,
            "decision": snapshot.decision_result.decision,
            "confidence": snapshot.decision_result.confidence,
            "mae": metrics.mae,
            "mfe": metrics.mfe,
            "pl": metrics.pl,
            "hit": metrics.hit,
            "timestamp": snapshot.timestamp
        }
        with self._lock:
            atomic_json_write(
                f"{self.output_dir}/{safe_audit_id}.json",
                data,
                indent=4,
            )
