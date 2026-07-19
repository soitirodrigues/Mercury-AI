import time
import tracemalloc
import gc
import threading
from contextlib import contextmanager
from typing import List
from mercury_ai.models.profiler_models import StageProfile, PipelineProfile

class _StageBuilder:
    def __init__(self, name: str):
        self.name = name
        self.start_time = 0.0
        self.end_time = 0.0
        self.mem_start = 0
        self.mem_end = 0
        self.mem_peak = 0
        self.children: List['_StageBuilder'] = []

    def finalize(self, total_duration: float) -> StageProfile:
        duration = self.end_time - self.start_time
        percentage = (duration / total_duration * 100) if total_duration > 0 else 0.0
        return StageProfile(
            name=self.name,
            duration=duration,
            memory_peak=self.mem_peak,
            memory_delta=max(0, self.mem_end - self.mem_start),
            percentage_total=percentage,
            nested_stages=tuple(child.finalize(total_duration) for child in self.children)
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
        stage_profiles = tuple(child.finalize(total_duration) for child in self._local.root.children)
        return PipelineProfile(self.pipeline_name, total_duration, stage_profiles)

    def json(self) -> str:
        import json
        from dataclasses import asdict
        return json.dumps(asdict(self.summary()), indent=2)

    def pretty_print(self):
        # Placeholder for pretty print implementation
        print(self.json())
