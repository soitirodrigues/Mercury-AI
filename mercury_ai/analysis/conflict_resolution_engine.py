from typing import List, Tuple
from dataclasses import replace
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext
from mercury_ai.analysis.adaptive_weight_engine import AdaptiveWeightEngine

class ConflictResolutionEngine:
    """
    Motor institucional de resolução de conflitos entre evidências baseada em pesos.
    """
    def __init__(self):
        self.adaptive_weights = AdaptiveWeightEngine()

    def resolve(self, evidences: List[Evidence], context: MarketContext) -> Tuple[List[Evidence], float]:
        """
        Resolve conflitos baseando-se no peso adaptativo das evidências.
        """
        if not evidences:
            return [], 0.0
            
        weights = self.adaptive_weights.calculate_weights(context)
        
        # Aplicar pesos adaptativos
        weighted_evidences = []
        for e in evidences:
            # Map engine name (e.g., "TrendEngine") to weight keys ("Trend")
            # Remove 'Engine' suffix to match AdaptiveWeightEngine keys
            weight_key = e.engine_name.replace('Engine', '')
            
            # Fallback if specific engine weight not found
            base_weight = weights.get(weight_key, weights.get(e.engine_name, 1.0))
            weighted_evidences.append(replace(e, weight=e.weight * base_weight))
            
        bullish_evidences = [e for e in weighted_evidences if e.direction == "BULLISH"]
        bearish_evidences = [e for e in weighted_evidences if e.direction == "BEARISH"]
        
        bullish_weight = sum(e.weight for e in bullish_evidences)
        bearish_weight = sum(e.weight for e in bearish_evidences)
        
        total_weight = bullish_weight + bearish_weight
        
        if total_weight == 0:
            return weighted_evidences, 1.0
            
        if bullish_weight >= bearish_weight:
            prevailed = bullish_evidences
            winner_weight = bullish_weight
            loser_weight = bearish_weight
        else:
            prevailed = bearish_evidences
            winner_weight = bearish_weight
            loser_weight = bullish_weight
            
        # ConflictResolutionScore
        score = (winner_weight - loser_weight) / total_weight
        
        return prevailed, score
