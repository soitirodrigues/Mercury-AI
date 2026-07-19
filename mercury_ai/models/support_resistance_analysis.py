from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class SupportResistanceAnalysis:
    support: Optional[float] = None
    resistance: Optional[float] = None
    nearest_support: Optional[float] = None
    nearest_resistance: Optional[float] = None
    distance_to_support_atr: Optional[float] = None
    distance_to_resistance_atr: Optional[float] = None
    support_strength: Optional[float] = None
    resistance_strength: Optional[float] = None
    price_location: Optional[str] = None
    explanation: Optional[str] = None
