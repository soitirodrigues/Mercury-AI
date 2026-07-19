from dataclasses import dataclass
from typing import Any, Dict

@dataclass(frozen=True)
class PerformanceMetrics:
    total_trades: int
    correct: int
    incorrect: int
    late_entries: int
    early_entries: int
    missed_trades: int
    false_positives: int
    false_negatives: int
    engine_responsibility: Dict[str, int]
    evidence_responsibility: Dict[str, int]
