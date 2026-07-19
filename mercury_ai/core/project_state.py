from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ProjectState:
    """
    Lê o snapshot gerado pelo Mercury Project Mapper.

    Este passa a ser o ponto oficial de acesso ao conhecimento
    estrutural do projeto.
    """

    def __init__(self, snapshot_path: str = ".mercury/mercury_snapshot.json"):

        self.snapshot_path = Path(snapshot_path)

        if not self.snapshot_path.exists():
            raise FileNotFoundError(
                f"Snapshot não encontrado: {self.snapshot_path}"
            )

        with open(self.snapshot_path, "r", encoding="utf-8") as f:
            self.data: dict[str, Any] = json.load(f)

    @property
    def metadata(self):
        return self.data.get("metadata", {})

    @property
    def json(self):
        return self.data.get("json", {})

    @property
    def documents(self):
        return self.data.get("documents", {})

    @property
    def statistics(self):
        return self.data.get("statistics", {})

    def get(self, name: str, default=None):
        return self.json.get(name, default)

    def has(self, name: str) -> bool:
        return name in self.json

    def summary(self):
        lines = [
            "----------------------------------",
            " Mercury Project State",
            "----------------------------------",
            f"JSON ............. {self.statistics.get('json_files',0)}",
            f"Markdown ......... {self.statistics.get('markdown_files',0)}",
            f"Documentos ....... {self.statistics.get('total_documents',0)}",
            "----------------------------------",
        ]
        return "\n".join(lines)