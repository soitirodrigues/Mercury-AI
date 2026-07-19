from typing import List
from mercury_ai.models.analysis_result import AnalysisResult

class RankingEngine:
    """
    Motor institucional de ranqueamento de oportunidades.
    """

    def rank(self, analyses: List[AnalysisResult]) -> List[AnalysisResult]:
        """
        Ordena os resultados das análises com base em um escore institucional.
        """
        def calculate_rank_score(analysis: AnalysisResult) -> float:
            score = 0.0
            
            # Confluence Score
            score += analysis.confluence.score
            
            # Confidence
            score += analysis.confluence.confidence
            
            # Smart Money Score (se disponível)
            if hasattr(analysis, 'smart_money'):
                score += analysis.smart_money.score
                
            return score

        # Ordena de forma decrescente pelo escore calculado
        return sorted(analyses, key=calculate_rank_score, reverse=True)
