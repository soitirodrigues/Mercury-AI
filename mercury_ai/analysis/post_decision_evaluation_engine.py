from typing import List, Dict
from mercury_ai.models.decision_snapshot import DecisionSnapshot
from mercury_ai.models.performance_metrics import PerformanceMetrics

class PostDecisionEvaluationEngine:
    """
    Motor institucional de avaliação de decisões históricas.
    """

    def evaluate(self, replay_data: List[Dict]) -> PerformanceMetrics:
        engine_resp = {}
        evidence_resp = {}
        
        counts = {
            "correct": 0, "incorrect": 0, "late": 0, "early": 0,
            "missed": 0, "fp": 0, "fn": 0
        }
        
        for r in replay_data:
            snapshot: DecisionSnapshot = r['snapshot']
            metrics = r['metrics']
            
            # Deterministic outcome classification
            if snapshot.decision_result.decision == "BUY":
                if metrics.pl > 0: counts["correct"] += 1
                else: counts["incorrect"] += 1
            elif snapshot.decision_result.decision == "SELL":
                if metrics.pl < 0: counts["correct"] += 1
                else: counts["incorrect"] += 1
            else: # WAIT
                if abs(metrics.pl) > 0.05: counts["missed"] += 1 # Simplified threshold

            # Attribute responsibility to engines/evidences
            for eng, weight in snapshot.decision_result.explanation.engine_weights.items():
                if weight > 0:
                    engine_resp[eng] = engine_resp.get(eng, 0) + 1
            
            for ev in snapshot.decision_result.explanation.contributing_evidences:
                evidence_resp[ev] = evidence_resp.get(ev, 0) + 1

        return PerformanceMetrics(
            total_trades=len(replay_data),
            correct=counts["correct"],
            incorrect=counts["incorrect"],
            late_entries=counts["late"],
            early_entries=counts["early"],
            missed_trades=counts["missed"],
            false_positives=counts["fp"],
            false_negatives=counts["fn"],
            engine_responsibility=engine_resp,
            evidence_responsibility=evidence_resp
        )
