from mercury_ai.models.decision_trace import DecisionTrace, DecisionNode
from dataclasses import replace

class DecisionTraceEngine:
    """
    Registra determinística o caminho lógico da decisão institucional.
    """
    
    def __init__(self):
        self.trace = DecisionTrace()

    def log_step(self, engine: str, evidence: str, weight: float, score: float, influence: str, result: str):
        # We need to update nodes, DecisionTrace.nodes must be mutable if it's a list, but FrozenInstanceError means the dataclass itself cannot be updated.
        # DecisionTrace.nodes should probably be a tuple if frozen.
        node = DecisionNode(engine, evidence, weight, score, influence, result)
        self.trace = replace(self.trace, nodes=self.trace.nodes + (node,))

    def finalize(self, final_score: float, final_decision: str) -> DecisionTrace:
        self.trace = replace(self.trace, final_score=final_score, final_decision=final_decision)
        return self.trace
