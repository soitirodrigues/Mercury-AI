import json
from typing import List, Dict, Optional
from mercury_ai.models.regression import BenchmarkMetrics, RegressionResult

class RegressionDetector:
    def __init__(self, history_file: str, thresholds: Dict[str, float]):
        self.history_file = history_file
        self.thresholds = thresholds # e.g., {"duration": 0.1, "memory": 0.1}
        self.history: List[BenchmarkMetrics] = self._load_history()

    def _load_history(self) -> List[BenchmarkMetrics]:
        try:
            with open(self.history_file, 'r') as f:
                data = json.load(f)
                return [BenchmarkMetrics(**m) for m in data]
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_history(self):
        with open(self.history_file, 'w') as f:
            json.dump([m.__dict__ for m in self.history], f, indent=2)

    def detect(self, current: BenchmarkMetrics) -> RegressionResult:
        if not self.history:
            return RegressionResult(False, 0.0, 0.0, 0.0, 0.0, "No baseline")

        baseline = self.history[-1]
        
        perf_delta = (current.duration - baseline.duration) / baseline.duration
        mem_delta = (current.peak_memory - baseline.peak_memory) / baseline.peak_memory
        alloc_delta = (current.allocation_count - baseline.allocation_count) / baseline.allocation_count
        gc_delta = (current.gc_count - baseline.gc_count) / baseline.gc_count

        is_regression = (
            perf_delta > self.thresholds.get("duration", 0.05) or
            mem_delta > self.thresholds.get("memory", 0.05)
        )
        
        msg = f"Perf Delta: {perf_delta:.1%}, Mem Delta: {mem_delta:.1%}" if is_regression else "Stable"
        
        return RegressionResult(is_regression, perf_delta, mem_delta, alloc_delta, gc_delta, msg)
