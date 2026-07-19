from dataclasses import dataclass


@dataclass(frozen=True)
class InstitutionalScoreResult:
    institutional_score: float
    probability_score: float
    confluence_score: float
    confidence_score: float
    trade_quality_score: float
    resolved_quality_score: float
    risk_score: float
    conflict_penalty: float


class InstitutionalScoreEngine:
    """
    Motor institucional de cálculo do score final.

    Responsável exclusivo pela fórmula de composição
    do Institutional Score, isolando a regra de negócio
    do orquestrador.
    """

    def calculate(
        self,
        probability_score: float,
        confluence_score: float,
        confidence_score: float,
        trade_quality_score: float,
        resolved_quality_score: float,
        risk_score: float,
        conflict_penalty: float,
    ) -> InstitutionalScoreResult:

        # ----------------------------------------------------
        # Fórmula de composição do Institutional Score
        #
        # Pesos calibrados para refletir a hierarquia
        # institucional de importância:
        #
        #   probability_score  → 35% (direção + convicção)
        #   confluence_score   → 25% (alinhamento entre engines)
        #   confidence_score   → 15% (qualidade + consenso)
        #   trade_quality_score→ 10% (filtro institucional)
        #   resolved_quality   →  5% (qualidade das evidências)
        #   risk_penalty        → 10% (risco reduz score)
        # ----------------------------------------------------

        institutional_score = (
            probability_score * 0.35 +
            confluence_score * 0.25 +
            confidence_score * 0.15 +
            trade_quality_score * 0.10 +
            resolved_quality_score * 0.05 +
            (100.0 - risk_score) * 0.10
        )

        # ----------------------------------------------------
        # Penalidade de conflito
        #
        # conflict_penalty é o consensus score do ConflictResolutionEngine:
        #   1.0 = consenso total (todos sinais alinhados) → sem penalidade
        #   0.0 = conflito máximo (empate bullish/bearish) → score zerado
        #
        # Usado diretamente como penalty_factor multiplicativo.
        # ----------------------------------------------------

        penalty_factor = max(0.0, min(conflict_penalty, 1.0))
        institutional_score *= penalty_factor

        institutional_score = max(
            0.0,
            min(
                institutional_score,
                100.0,
            ),
        )

        return InstitutionalScoreResult(
            institutional_score=institutional_score,
            probability_score=probability_score,
            confluence_score=confluence_score,
            confidence_score=confidence_score,
            trade_quality_score=trade_quality_score,
            resolved_quality_score=resolved_quality_score,
            risk_score=risk_score,
            conflict_penalty=conflict_penalty,
        )