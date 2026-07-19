from dataclasses import dataclass
from typing import Tuple

@dataclass(frozen=True)
class DataQualityResult:
    """
    Structured result of DataQualityEngine analysis.
    """
    score: float
    warnings: Tuple[str, ...]
    missing_inputs: Tuple[str, ...]
    stale_data: bool
    quality_level: str
