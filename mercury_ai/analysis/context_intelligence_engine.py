from typing import List
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_context import MarketContext

class ContextIntelligenceEngine:
    """
    Motor institucional para avaliação de contexto de evidências.
    """

    def evaluate(self, evidences: List[Evidence], market_context: MarketContext) -> List[Evidence]:
        # 1. Avaliação Determinística de Contexto
        context_score = 100.0
        context_evidences = []

        # Exemplo: avaliar alinhamento com regime
        if market_context.market_state and market_context.market_state.state == "RANGE":
            context_score -= 20.0
            context_evidences.append(Evidence("ContextEngine", "Market State", "NEUTRAL", 50.0, 70.0, "Contexto de Consolidação", 10.0))

        # 2. Aplicação do Score (Manter estrutura neutra para evidências existentes)
        from dataclasses import replace
        updated_evidences = []
        for e in evidences:
            updated_evidences.append(replace(e, context_score=max(0.0, min(100.0, context_score))))
            
        return updated_evidences + context_evidences
