import json
import os
import re
import tempfile
import threading
from pathlib import Path
from dataclasses import asdict
from typing import List, Dict, Any
from functools import lru_cache
from mercury_ai.models.decision_snapshot import DecisionSnapshot

# Regex whitelist: letras, números, ponto, hífen e underscore.
# Rejeita path traversal (../), barras e caracteres especiais.
_SAFE_SYMBOL_RE = re.compile(r"^[A-Za-z0-9._\-]+$")


def _sanitize_filename_component(value: str) -> str:
    """Sanitiza um componente de nome de arquivo contra path traversal.

    - Rejeita strings vazias.
    - Rejeita strings com caracteres fora do whitelist (inclui '/', '\\', '..').
    - Substitui ':' por '-' para timestamps.
    """
    if not value:
        raise ValueError("Componente de nome de arquivo não pode ser vazio.")
    # Substitui ':' por '-' (comum em timestamps ISO)
    safe = value.replace(":", "-")
    # Substitui '=' por '_' (comum em símbolos do Yahoo Finance: GC=F, EURUSD=X)
    safe = safe.replace("=", "_")
    # Rejeita path traversal explícito
    if ".." in safe or "/" in safe or "\\" in safe:
        raise ValueError(f"Componente de nome de arquivo inválido (path traversal): {value!r}")
    if not _SAFE_SYMBOL_RE.match(safe):
        raise ValueError(f"Componente de nome de arquivo contém caracteres não permitidos: {value!r}")
    return safe


class DecisionSnapshotLogger:
    """Logger de snapshots de decisão com escrita atômica e thread-safe.

    - Escrita atômica: escreve em arquivo temporário e usa os.replace().
    - Thread-safe: lock de instância protege operações de save.
    - Sanitização: nomes de arquivo validados contra path traversal.
    """

    def __init__(self, base_path: str = "mercury_ai/database/snapshots"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()

    def save(self, snapshot: DecisionSnapshot) -> DecisionSnapshot:
        safe_asset = _sanitize_filename_component(str(snapshot.asset))
        safe_timestamp = _sanitize_filename_component(str(snapshot.timestamp))
        filename = f"{safe_asset}_{safe_timestamp}.json"
        filepath = self.base_path / filename

        with self._lock:
            # Escrita atômica: temp file no mesmo diretório + os.replace
            data = json.dumps(asdict(snapshot), indent=4, default=str)
            fd, tmp_path = tempfile.mkstemp(
                suffix=".tmp", prefix=".snap_", dir=str(self.base_path)
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(data)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, filepath)
            except OSError:
                # Limpa o temporário em caso de falha
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
                raise
        return snapshot

    def list_snapshots(self) -> List[Path]:
        return sorted(list(self.base_path.glob("*.json")), reverse=True)

    @lru_cache(maxsize=128)
    def load_snapshot(self, snapshot_path: Path) -> Dict[str, Any]:
        with open(snapshot_path, "r", encoding="utf-8") as f:
            return json.load(f)
