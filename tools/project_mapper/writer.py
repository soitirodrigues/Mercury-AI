import json
from dataclasses import asdict
from pathlib import Path

from .config import PROJECT_ROOT


OUTPUT = PROJECT_ROOT / ".mercury"


class InventoryWriter:

    def save(self, inventory):

        OUTPUT.mkdir(exist_ok=True)

        with open(
            OUTPUT / "project_inventory.json",
            "w",
            encoding="utf8",
        ) as f:

            json.dump(
                asdict(inventory),
                f,
                indent=4,
                ensure_ascii=False,
            )