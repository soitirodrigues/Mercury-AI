from typing import List
from mercury_ai.models.evidence import Evidence
from dataclasses import replace

class EvidenceQualityEngine:
    """
    Motor institucional de avaliação e integração de qualidade de evidências.
    """

    def evaluate(self, evidences: List[Evidence]) -> List[Evidence]:
        """
        Calcula e atribui scores de qualidade baseados na independência e ausência de conflitos.
        """
        if not evidences:
            return []
        
        # 1. Avaliação de Independência/Redundância (Simples por nome de engine)
        engine_counts = {}
        for e in evidences:
            engine_counts[e.engine_name] = engine_counts.get(e.engine_name, 0) + 1
            
        # 2. Avaliação de Conflitos
        # Para simplificar, consideramos conflitos baseados na direção dentro da mesma engine ou globalmente
        bullish = [e for e in evidences if e.direction == "BULLISH"]
        bearish = [e for e in evidences if e.direction == "BEARISH"]
        conflict = len(bullish) > 0 and len(bearish) > 0
        
        evaluated_evidences = []
        for e in evidences:
            # Penaliza redundância (evidências do mesmo motor)
            redundancy_penalty = 0.9 if engine_counts[e.engine_name] > 1 else 1.0
            
            # Penaliza conflito
            conflict_penalty = 0.7 if conflict else 1.0
            
            # Novo score de qualidade
            quality_score = e.quality_score * redundancy_penalty * conflict_penalty
            
            evaluated_evidences.append(replace(e, quality_score=max(0.0, min(100.0, quality_score))))
            
        return evaluated_evidences
