import tracemalloc
import gc
from typing import Optional
from mercury_ai.models.memory_audit import MemorySnapshot, MemoryAuditResult

class MemoryAuditor:
    def __init__(self):
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        self.snapshot_before: Optional[MemorySnapshot] = None

    def _take_snapshot(self) -> MemorySnapshot:
        # Force collection before snapshot for cleaner metrics
        gc.collect()
        return MemorySnapshot(
            snapshot=tracemalloc.take_snapshot(),
            gc_count=sum(gc.get_count())
        )

    def __enter__(self):
        self.snapshot_before = self._take_snapshot()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        snapshot_after = self._take_snapshot()
        self.result = self._compare(self.snapshot_before, snapshot_after)

    def _compare(self, before: MemorySnapshot, after: MemorySnapshot) -> MemoryAuditResult:
        stats = after.snapshot.compare_to(before.snapshot, 'lineno')
        
        diff_size = 0
        diff_count = 0
        top_stats = []
        for stat in stats:
            diff_size += stat.size_diff
            diff_count += stat.count_diff
            if stat.size_diff > 0:
                top_stats.append(str(stat))
        
        return MemoryAuditResult(
            peak_memory_diff=tracemalloc.get_traced_memory()[1], # Peak since start
            allocation_diff_size=diff_size,
            allocation_diff_count=diff_count,
            gc_count_diff=after.gc_count - before.gc_count,
            top_stats=top_stats
        )
