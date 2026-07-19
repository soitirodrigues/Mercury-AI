from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class BenchmarkMetrics:
    timestamp: float
    duration: float
    peak_memory: int
    allocation_count: int
    gc_count: int

@dataclass(frozen=True)
class RegressionResult:
    is_regression: bool
    performance_delta: float  # % change
    memory_delta: float       # % change
    allocation_delta: float   # % change
    gc_delta: float           # % change
    message: str
