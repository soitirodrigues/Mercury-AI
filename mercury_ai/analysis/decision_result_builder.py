import hashlib
from typing import List, Optional, Tuple

from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.version_metadata import VersionMetadata
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence_ranking import EvidenceRankingResult
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.probability_result import ProbabilityResult
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.analysis.decision_explainability import DecisionExplainability


class DecisionResultBuilder:
    """
    Builder institucional do DecisionResult.

    NÃO executa cálculos.
    NÃO altera regras.
    NÃO decide BUY/SELL/WAIT.

    Apenas monta o objeto DecisionResult utilizando todos os
    parâmetros já calculados anteriormente.
    """

    def build(
        self,
        *,
        final_decision: str,
        grade: str,
        calibrated_confidence: float,
        confluence_result: ConfluenceResult,
        risk_score: float,
        institutional_score: float,
        trade_quality_score: float,
        ranked_result: EvidenceRankingResult,
        buy_prob: float,
        sell_prob: float,
        wait_prob: float,
        expected_risk: float,
        expected_reward: float,
        expected_drawdown: float,
        explanation: TradingExplanation,
        resolved_bundle: MarketEvidenceBundle,
        final_warnings: List[str],
        confidence_result: ConfidenceResult,
        explainability: Optional[DecisionExplainability] = None,
    ) -> DecisionResult:

        # =====================================================
        # AUDIT
        # =====================================================

        audit_input = (
            f"{resolved_bundle.asset}"
            f"{resolved_bundle.timeframe}"
            f"{len(resolved_bundle.evidences)}"
        )

        audit_id = hashlib.sha256(
            audit_input.encode()
        ).hexdigest()

        # =====================================================
        # VERSION METADATA
        # =====================================================

        version_metadata = VersionMetadata(
            engine_version="1.2.0",
            pipeline_version="1.2.0",
            context_version="1.2.0",
            weights_version="1.2.0",
        )

        # =====================================================
        # WARNINGS
        # =====================================================

        warnings = tuple(
            list(explanation.warnings)
            + final_warnings
        )

        # =====================================================
        # WEAKNESSES
        # =====================================================

        weaknesses = tuple(
            f"{e.engine_name} low quality"
            for e in resolved_bundle.evidences
            if e.quality_score < 50
        )

        # =====================================================
        # BLOCKERS
        # =====================================================

        blockers = tuple(
            explanation.conflicts
        )

        # =====================================================
        # DECISION RESULT
        # =====================================================

        return DecisionResult(
            decision=final_decision,
            grade=grade,
            # DESIGN NOTE: confidence é armazenado em escala 0-1 (não 0-100) por
            # compatibilidade histórica com todos os consumidores UI que usam
            # o padrão decision.confidence*100 para exibição.
            confidence=calibrated_confidence / 100.0,
            clarity=confluence_result.agreement_percentage,
            risk_score=risk_score,
            score=institutional_score,
            quality=trade_quality_score,
            expected_strength=ranked_result.total_weight,
            buy_probability=buy_prob,
            sell_probability=sell_prob,
            wait_probability=wait_prob,
            expected_risk=expected_risk,
            expected_reward=expected_reward,
            expected_drawdown=expected_drawdown,
            audit_id=audit_id,
            version_metadata=version_metadata,
            explanation=explanation,
            summary=explanation.exec_summary,
            technical_reason=explanation.decision_rationale,
            warnings=warnings,
            weaknesses=weaknesses,
            blockers=blockers,
            institutional_alignment=confidence_result.is_high,
            evidence_ranking=ranked_result,
            explainability=explainability,
        )