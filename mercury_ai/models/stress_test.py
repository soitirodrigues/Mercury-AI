from dataclasses import dataclass
from typing import List
from mercury_ai.models.market_data import MarketData

@dataclass(frozen=True)
class StressTestResult:
    pipeline_name: str
    scenario: str
    dataset_size: int
    repetitions: int
    runtimes: List[float]
    peak_memory: List[int]
    exceptions: List[Exception]
    is_deterministic: bool
    failure_count: int
