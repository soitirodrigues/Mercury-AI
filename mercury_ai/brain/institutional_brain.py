from typing import List
from mercury_ai.models.analysis_result import AnalysisResult
from mercury_ai.models.evidence import Evidence

class InstitutionalBrain:
    """
    Camada de inteligência artificial explicável da Mercury AI.
    Fornece racional institucional para decisões baseada em evidências.
    """

    def explain(self, result: AnalysisResult) -> str:
        """
        Gera uma explicação em linguagem natural para a decisão tomada.
        """
        decision = result.confluence.decision
        evidences = self._get_all_evidences(result)
        
        contributing_engines = list(set([e.engine_name for e in evidences if e.strength > 50]))
        highest_weight_evidence = max(evidences, key=lambda e: e.weight) if evidences else None

        explanation = f"Decisão: {decision}.\n"
        explanation += f"Motores contribuintes: {', '.join(contributing_engines)}.\n"
        
        if highest_weight_evidence:
            explanation += f"Principal fator: {highest_weight_evidence.engine_name} - {highest_weight_evidence.evidence_name} "
            explanation += f"(Peso: {highest_weight_evidence.weight}).\n"
            
        explanation += f"Justificativa: {result.confluence.explanation}"
        
        return explanation

    def _get_all_evidences(self, result: AnalysisResult) -> List[Evidence]:
        all_evidences = []
        # Aggregate all evidence lists provided by the pipeline
        sources = [
            result.trend, 
            result.mtf_evidences, 
            result.smart_money.evidences if hasattr(result.smart_money, 'evidences') else [],
            result.liquidity_analysis.evidences if hasattr(result.liquidity_analysis, 'evidences') else [],
            result.volume_analysis.evidences if hasattr(result.volume_analysis, 'evidences') else []
        ]
        for source in sources:
            if source:
                all_evidences.extend(source)
        return all_evidences
