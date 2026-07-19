from dataclasses import dataclass, field
from typing import Tuple
from mercury_ai.models.decision_node import DecisionNode

@dataclass(frozen=True)
class DecisionTrace:
    nodes: Tuple[DecisionNode, ...] = field(default_factory=tuple)
    final_score: float = 0.0
    final_decision: str = ""
