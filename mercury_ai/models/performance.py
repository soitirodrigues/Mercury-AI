from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class StageMetric:
    name: str
    duration: float
    memory_delta: int
    percentage_total: float
    nested_metrics: Tuple['StageMetric', ...]

@dataclass(frozen=True)
class PipelineMetric:
    pipeline_name: str
    total_duration: float
    stage_metrics: Tuple[StageMetric, ...]

@dataclass(frozen=True)
class HotspotReport:
    pipeline_name: str
    total_duration: float
    hotspots: Tuple[str, ...]  # Sorted by duration (descending)
