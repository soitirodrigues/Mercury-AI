from typing import Any, Callable, Type, Optional, List, Dict
from mercury_ai.core.pipeline_profiler import PipelineProfiler
import logging

logger = logging.getLogger(__name__)

class PipelineContractError(Exception):
    pass

class PipelineExecutor:
    def __init__(self, profiler: Optional[PipelineProfiler] = None):
        self.profiler = profiler
        self.history: List[Dict[str, Any]] = []

    def execute(self, stage_name: str, func: Callable, expected_output_type: Type, *args, **kwargs) -> Any:
        
        # 1. Profiling
        from contextlib import nullcontext
        def stage():
            return self.profiler.stage(stage_name) if self.profiler else nullcontext()
        
        try:
            with stage():
                result = func(*args, **kwargs)
                
            # 2. Contract Validation
            if not isinstance(result, expected_output_type):
                raise PipelineContractError(f"Pipeline Stage '{stage_name}' output contract violation. Expected {expected_output_type}, got {type(result)}")
            
            self.history.append({"stage": stage_name, "status": "success"})
            return result
            
        except Exception as e:  # Broad catch intentional: pipeline executor wraps ALL stage errors into PipelineContractError
            logger.error(f"Pipeline Stage '{stage_name}' falhou: {type(e).__name__}: {e}", exc_info=True)
            self.history.append({"stage": stage_name, "status": "failed", "error": str(e)})
            if isinstance(e, PipelineContractError):
                raise
            raise PipelineContractError(f"Pipeline Stage '{stage_name}' failed: {e}") from e
