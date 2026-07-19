import time
import tracemalloc
import gc
from contextlib import contextmanager
from typing import List, Tuple
from mercury_ai.models.performance import StageMetric, PipelineMetric, HotspotReport
from mercury_ai.core._stage_builder import _StageBuilder


def _finalize_metric(builder: _StageBuilder, total_duration: float) -> StageMetric:
    """Converte um _StageBuilder em StageMetric (usado pelo PerformanceCollector)."""
    return StageMetric(
        name=builder.name,
        duration=builder.duration,
        memory_delta=builder.memory_delta,
        percentage_total=builder.percentage_of(total_duration),
        nested_metrics=tuple(_finalize_metric(c, total_duration) for c in builder.children),
    )

class PerformanceCollector:
    def __init__(self, pipeline_name: str):
        self.pipeline_name = pipeline_name
        self.root_builder = _StageBuilder("Root")
        self.stack: List[_StageBuilder] = [self.root_builder]
        if not tracemalloc.is_tracing():
            tracemalloc.start()

    @contextmanager
    def stage(self, name: str):
        builder = _StageBuilder(name)
        parent = self.stack[-1]
        parent.children.append(builder)
        self.stack.append(builder)
        
        gc.collect()
        builder.mem_start = tracemalloc.get_traced_memory()[0]
        builder.start_time = time.perf_counter()
        
        try:
            yield
        finally:
            builder.end_time = time.perf_counter()
            builder.mem_end = tracemalloc.get_traced_memory()[0]
            self.stack.pop()

    def collect(self) -> Tuple[PipelineMetric, HotspotReport]:
        total_duration = self.root_builder.children[-1].end_time - self.root_builder.children[0].start_time if self.root_builder.children else 0.0
        
        stage_metrics = tuple(_finalize_metric(child, total_duration) for child in self.root_builder.children)
        pipeline_metric = PipelineMetric(self.pipeline_name, total_duration, stage_metrics)
        
        # Calculate hotspots
        all_stages = self._flatten_stages(self.root_builder.children)
        sorted_stages = sorted(all_stages, key=lambda x: (x.end_time - x.start_time), reverse=True)
        hotspots = tuple(stage.name for stage in sorted_stages)
        
        hotspot_report = HotspotReport(self.pipeline_name, total_duration, hotspots)
        
        return pipeline_metric, hotspot_report

    def _flatten_stages(self, builders: List[_StageBuilder]) -> List[_StageBuilder]:
        flat = []
        for b in builders:
            flat.append(b)
            flat.extend(self._flatten_stages(b.children))
        return flat
