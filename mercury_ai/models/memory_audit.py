from dataclasses import dataclass, field
from typing import List
import tracemalloc
import time

@dataclass(frozen=True)
class MemorySnapshot:
    snapshot: tracemalloc.Snapshot
    gc_count: int
    timestamp: float = field(default_factory=time.time)

@dataclass(frozen=True)
class MemoryAuditResult:
    peak_memory_diff: int
    allocation_diff_size: int
    allocation_diff_count: int
    gc_count_diff: int
    top_stats: List[str] # Detailed breakdown of allocation growth
