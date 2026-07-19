import time
import tracemalloc
import gc
import threading
from contextlib import contextmanager
from mercury_ai.models.profiler_models import StageProfile, PipelineProfile
from mercury_ai.core._stage_builder import _StageBuilder


def _finalize_stage(builder: _StageBuilder, total_duration: float) -> StageProfile:
    """Converte um _StageBuilder em StageProfile (usado pelo PipelineProfiler)."""
    return StageProfile(
        name=builder.name,
        duration=builder.duration,
        memory_peak=builder.mem_peak,
        memory_delta=builder.memory_delta,
        percentage_total=builder.percentage_of(total_duration),
        nested_stages=tuple(_finalize_stage(c, total_duration) for c in builder.children),
    )

class PipelineProfiler:
    def __init__(self, pipeline_name: str, active: bool = True):
        self.pipeline_name = pipeline_name
        self.active = active
        self._local = threading.local()
        self._local.stack = []
        self._local.root = None

    def start_pipeline(self):
        if not self.active: return
        self._local.root = _StageBuilder("Root")
        self._local.stack = [self._local.root]
        if not tracemalloc.is_tracing():
            tracemalloc.start()

    def end_pipeline(self):
        if not self.active: return
        tracemalloc.stop()

    def start_stage(self, name: str):
        if not self.active: return
        builder = _StageBuilder(name)
        parent = self._local.stack[-1]
        parent.children.append(builder)
        self._local.stack.append(builder)
        
        gc.collect()
        builder.mem_start = tracemalloc.get_traced_memory()[0]
        builder.start_time = time.perf_counter()

    def end_stage(self, name: str):
        if not self.active: return
        builder = self._local.stack.pop()
        builder.end_time = time.perf_counter()
        _, builder.mem_peak = tracemalloc.get_traced_memory()
        builder.mem_end = tracemalloc.get_traced_memory()[0]

    @contextmanager
    def stage(self, name: str):
        self.start_stage(name)
        try:
            yield
        finally:
            self.end_stage(name)

    def summary(self) -> PipelineProfile:
        if not self._local.root or not self._local.root.children:
            return PipelineProfile(self.pipeline_name, 0.0, ())
        
        total_duration = self._local.root.children[-1].end_time - self._local.root.children[0].start_time
        stage_profiles = tuple(_finalize_stage(child, total_duration) for child in self._local.root.children)
        return PipelineProfile(self.pipeline_name, total_duration, stage_profiles)

    def json(self) -> str:
        import json
        from dataclasses import asdict
        return json.dumps(asdict(self.summary()), indent=2)

    def pretty_print(self):
        return self.json()
