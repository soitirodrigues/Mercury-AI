from dataclasses import dataclass, field

@dataclass
class FileInfo:
    path: str
    extension: str
    size: int

@dataclass
class Inventory:
    files: list[FileInfo] = field(default_factory=list)