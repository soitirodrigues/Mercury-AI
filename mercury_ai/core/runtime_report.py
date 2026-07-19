from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class TelemetryData:
    engine_name: str
    start_time: str
    end_time: str
    execution_time: float
    input_object: Any
    output_object: Any
    creator: Optional[str] = None
    modifier: Optional[str] = None
    consumer: Optional[str] = None
    disposer: Optional[str] = None
    persister: Optional[str] = None
    evidence_count: int = 0
    warnings: int = 0
    conflicts: int = 0
    dataframe_size: Optional[int] = None
    memory_usage: Optional[float] = None

@dataclass
class RuntimeReport:
    symbol: str
    stages: List[TelemetryData] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "symbol": self.symbol,
            "stages": [stage.__dict__ for stage in self.stages]
        }
