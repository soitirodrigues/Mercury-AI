from dataclasses import dataclass
from typing import Tuple
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.analysis.metric_calculator import PerformanceMetrics

@dataclass(frozen=True)
class BenchmarkRunResult:
    timestamp: str
    symbol: str
    decision_result: DecisionResult
    execution_time: float
    memory_usage: float

@dataclass(frozen=True)
class BenchmarkReport:
    version: str
    results: Tuple[BenchmarkRunResult, ...]
    average_execution_time: float
    performance_metrics: PerformanceMetrics
