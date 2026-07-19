from dataclasses import dataclass

@dataclass(frozen=True)
class VersionMetadata:
    engine_version: str
    pipeline_version: str
    context_version: str
    weights_version: str
