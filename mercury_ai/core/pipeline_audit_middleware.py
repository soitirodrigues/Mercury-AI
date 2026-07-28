import time
import traceback
from typing import Any, Callable
from mercury_ai.core.pipeline_profiler import PipelineProfiler
from mercury_ai.core.audit_sink import AuditSink, AuditEvent
from datetime import datetime, timezone


class PipelineAuditMiddleware:
    """Middleware de auditoria que captura erros de estágios do pipeline.

    - Registra evento de auditoria ANTES da execução (start).
    - Em caso de exceção, registra evento de falha com detalhes do erro.
    - A exceção original é sempre propagada (não oculta nada).
    """

    def __init__(self, profiler: PipelineProfiler, sink: AuditSink):
        self.profiler = profiler
        self.sink = sink

    def __call__(self, stage_name: str, func: Callable, *args, **kwargs) -> Any:
        start_ts = datetime.now(timezone.utc).isoformat()
        t0 = time.perf_counter()

        # Evento de início (sucesso presumido)
        event = AuditEvent(
            stage_name=stage_name,
            timestamp=start_ts,
            success=True,
            duration_ms=None,
        )
        self.sink.log(event)

        try:
            result = func(*args, **kwargs)
            return result
        except Exception as exc:  # Broad catch intentional: audit middleware must log ALL exceptions before re-raising
            # Registra evento de falha com detalhes completos
            duration_ms = (time.perf_counter() - t0) * 1000.0
            error_event = AuditEvent(
                stage_name=stage_name,
                timestamp=datetime.now(timezone.utc).isoformat(),
                success=False,
                error_message=str(exc),
                error_type=type(exc).__name__,
                duration_ms=round(duration_ms, 3),
            )
            self.sink.log(error_event)
            # Propaga a exceção original — nunca oculta
            raise
