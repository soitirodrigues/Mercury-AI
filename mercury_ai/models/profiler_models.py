from dataclasses import dataclass, field
from typing import Tuple

@dataclass(frozen=True)
class StageProfile:
    name: str
    duration: float
    memory_peak: int
    memory_delta: int
    percentage_total: float
    nested_stages: Tuple['StageProfile', ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class PipelineProfile:
    pipeline_name: str
    total_duration: float
    stage_profiles: Tuple[StageProfile, ...]

@dataclass(frozen=True)
class HotspotSummary:
    pipeline_name: str
    hotspots: Tuple[str, ...]
