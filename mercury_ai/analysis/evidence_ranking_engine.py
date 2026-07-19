from typing import List
from dataclasses import replace
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.evidence_ranking import EvidenceRankingResult

class EvidenceRankingEngine:
    """
    Motor institucional para ranking de evidências por contribuição.
    """

    def calculate_contribution_score(self, e: Evidence) -> float:
        # Calcular score de contribuição: peso * confiança * força (normalizado)
        # Normalização: / 1,000,000 (100 * 100 * 100)
        return (e.weight * e.confidence * e.strength) / 1000000.0

    def rank(self, evidences: List[Evidence]) -> EvidenceRankingResult:
        if not evidences:
            raise ValueError("No evidences to rank.")

        # Atualizar score de cada evidência
        ranked_evidences = []
        for e in evidences:
            score = self.calculate_contribution_score(e)
            ranked_evidences.append(replace(e, contribution_score=score))

        # Ordenar por contribution_score descendente
        ranked = sorted(ranked_evidences, key=lambda e: (e.contribution_score, e.engine_name, e.evidence_name), reverse=True)

        total_weight = sum(e.weight for e in ranked)
        total_score = sum(e.contribution_score for e in ranked)
        
        bullish_weight = sum(e.weight for e in ranked if e.direction == "BULLISH")
        bearish_weight = sum(e.weight for e in ranked if e.direction == "BEARISH")
        neutral_weight = sum(e.weight for e in ranked if e.direction == "NEUTRAL")

        bullish_score = sum(e.contribution_score for e in ranked if e.direction == "BULLISH")
        bearish_score = sum(e.contribution_score for e in ranked if e.direction == "BEARISH")
        neutral_score = sum(e.contribution_score for e in ranked if e.direction == "NEUTRAL")

        contribution_percentage = {
            "BULLISH": (bullish_score / total_score) * 100 if total_score > 0 else 0,
            "BEARISH": (bearish_score / total_score) * 100 if total_score > 0 else 0,
            "NEUTRAL": (neutral_score / total_score) * 100 if total_score > 0 else 0,
        }

        # Top evidences por direção
        bullish_evs = [e for e in ranked if e.direction == "BULLISH"]
        bearish_evs = [e for e in ranked if e.direction == "BEARISH"]
        neutral_evs = [e for e in ranked if e.direction == "NEUTRAL"]

        return EvidenceRankingResult(
            ranked_evidences=ranked,
            contribution_percentage=contribution_percentage,
            strongest_evidence=ranked[0],
            weakest_evidence=ranked[-1],
            total_weight=total_weight,
            bullish_weight=bullish_weight,
            bearish_weight=bearish_weight,
            neutral_weight=neutral_weight,
            bullish_score=bullish_score,
            bearish_score=bearish_score,
            neutral_score=neutral_score,
            top_bullish_evidence=bullish_evs[0] if bullish_evs else None,
            top_bearish_evidence=bearish_evs[0] if bearish_evs else None,
            top_neutral_evidence=neutral_evs[0] if neutral_evs else None
        )
