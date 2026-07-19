"""
Construtor de estágio compartilhado para profiling de pipeline.

Usado por PipelineProfiler e PerformanceCollector para construir
árvores de estágios aninhados durante a execução do pipeline.
"""
from __future__ import annotations

from typing import List


class _StageBuilder:
    """Constrói uma árvore de estágios de execução com métricas de tempo e memória."""

    __slots__ = ("name", "start_time", "end_time", "mem_start", "mem_end", "mem_peak", "children")

    def __init__(self, name: str) -> None:
        self.name = name
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.mem_start: int = 0
        self.mem_end: int = 0
        self.mem_peak: int = 0
        self.children: List[_StageBuilder] = []

    @property
    def duration(self) -> float:
        """Duração do estágio em segundos."""
        return self.end_time - self.start_time

    @property
    def memory_delta(self) -> int:
        """Delta de memória (final - inicial), nunca negativo."""
        return max(0, self.mem_end - self.mem_start)

    def percentage_of(self, total_duration: float) -> float:
        """Percentual deste estágio em relação à duração total."""
        if total_duration <= 0:
            return 0.0
        return (self.duration / total_duration) * 100.0