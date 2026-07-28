from pathlib import Path

from .config import (
    PROJECT_ROOT,
    IGNORE_DIRS,
    IGNORE_FILES,
    SOURCE_EXTENSIONS,
)

from .models import (
    FileInfo,
    Inventory,
)


class ProjectScanner:

    def scan(self) -> Inventory:

        inventory = Inventory()

        for file in PROJECT_ROOT.rglob("*"):

            if not file.is_file():
                continue

            if any(part in IGNORE_DIRS for part in file.parts):
                continue

            if file.name in IGNORE_FILES:
                continue

            if file.suffix.lower() not in SOURCE_EXTENSIONS:
                continue

            inventory.files.append(
                FileInfo(
                    path=str(file.relative_to(PROJECT_ROOT)),
                    extension=file.suffix.lower(),
                    size=file.stat().st_size,
                )
            )

        inventory.files.sort(key=lambda x: x.path)

        return inventory