from typing import List

from mercury_ai.models.analysis_result import AnalysisResult


class RankingEngine:
    """
    Motor institucional de ranqueamento.

    O DecisionEngine já calcula o Institutional Score.
    O RankingEngine apenas ordena as oportunidades.
    """

    def rank(
        self,
        analyses: List[AnalysisResult]
    ) -> List[AnalysisResult]:

        return sorted(
            analyses,
            key=lambda analysis: analysis.decision.score,
            reverse=True
        )
