from typing import Any, Callable
from mercury_ai.core.pipeline_profiler import PipelineProfiler
from mercury_ai.core.audit_sink import AuditSink, AuditEvent
from datetime import datetime

class PipelineAuditMiddleware:
    def __init__(self, profiler: PipelineProfiler, sink: AuditSink):
        self.profiler = profiler
        self.sink = sink

    def __call__(self, stage_name: str, func: Callable, *args, **kwargs) -> Any:
        # Audit logic: Record structured audit event to the sink
        event = AuditEvent(stage_name=stage_name, timestamp=datetime.utcnow().isoformat())
        self.sink.log(event)
        
        return func(*args, **kwargs)
