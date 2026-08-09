from dataclasses import dataclass
from typing import Tuple
from mercury_ai.models.market_data import MarketData

@dataclass(frozen=True)
class StressTestResult:
    pipeline_name: str
    scenario: str
    dataset_size: int
    repetitions: int
    runtimes: Tuple[float, ...]
    peak_memory: Tuple[int, ...]
    exceptions: Tuple[Exception, ...]
    is_deterministic: bool
    failure_count: int
