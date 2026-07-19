import json
from pathlib import Path


class SnapshotBuilder:
    """
    Consolida automaticamente todos os artefatos existentes
    dentro da pasta .mercury em um único arquivo:

        .mercury/mercury_snapshot.json

    Não é necessário alterar este arquivo quando novos Builders
    forem adicionados ao Project Mapper.
    """

    def __init__(self):

        self.output_dir = Path(".mercury")
        self.snapshot_file = self.output_dir / "mercury_snapshot.json"

    def _load_json(self, file: Path):

        try:
            with open(file, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception:
            return None

    def _load_text(self, file: Path):

        try:
            return file.read_text(encoding="utf-8")

        except Exception:
            return ""

    def build(self):

        snapshot = {

            "metadata": {
                "generator": "Mercury Project Mapper",
                "version": "1.0.0"
            },

            "json": {},

            "documents": {}

        }

        if not self.output_dir.exists():
            self.output_dir.mkdir(parents=True, exist_ok=True)

        #
        # Carrega automaticamente TODOS os JSON
        #
        for file in sorted(self.output_dir.glob("*.json")):

            # Evita colocar o snapshot dentro dele mesmo
            if file.name == "mercury_snapshot.json":
                continue

            data = self._load_json(file)

            snapshot["json"][file.stem] = data

        #
        # Carrega automaticamente TODOS os Markdown
        #
        for file in sorted(self.output_dir.glob("*.md")):

            snapshot["documents"][file.stem] = self._load_text(file)

        #
        # Estatísticas rápidas
        #
        snapshot["statistics"] = {

            "json_files": len(snapshot["json"]),

            "markdown_files": len(snapshot["documents"]),

            "total_documents":
                len(snapshot["json"]) +
                len(snapshot["documents"])

        }

        with open(
            self.snapshot_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                snapshot,
                f,
                indent=4,
                ensure_ascii=False
            )

        print("----------------------------------")
        print("Snapshot Builder")
        print("----------------------------------")
        print(f"JSON       : {len(snapshot['json'])}")
        print(f"Markdown   : {len(snapshot['documents'])}")
        print("Arquivo gerado:")
        print(self.snapshot_file)
        print("----------------------------------")