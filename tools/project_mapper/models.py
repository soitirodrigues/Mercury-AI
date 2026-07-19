from dataclasses import dataclass, field


@dataclass
class FileInfo:

    path: str
    extension: str
    size: int
    ast: dict = field(default_factory=dict)


@dataclass
class Inventory:

    files: list[FileInfo] = field(default_factory=list)