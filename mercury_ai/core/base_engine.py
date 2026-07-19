from abc import ABC, abstractmethod
from typing import Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class EngineResult:
    score: float
    confidence: float
    evidences: Tuple[str, ...]
    warnings: Tuple[str, ...]
    execution_time: float

class BaseEngine(ABC):
    @abstractmethod
    def analyze(self, *args, **kwargs) -> EngineResult:
        pass
