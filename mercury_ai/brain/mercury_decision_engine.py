import logging
from typing import Optional

from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.models.trade_filter_result import TradeFilterResult

from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

from mercury_ai.analysis.validation_engine import ValidationEngine
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine
from mercury_ai.analysis.evidence_ranking_engine import EvidenceRankingEngine
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine
from mercury_ai.analysis.confidence_engine import ConfidenceEngine
from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
from mercury_ai.analysis.narrative_engine import NarrativeEngine
from mercury_ai.analysis.institutional_score_engine import InstitutionalScoreEngine
from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine
from mercury_ai.analysis.decision_result_builder import DecisionResultBuilder
from mercury_ai.analysis.market_thesis_builder import MarketThesisBuilder
from mercury_ai.analysis.risk_engine import RiskEngine
from mercury_ai.analysis.market_state_engine import MarketStateEngine
from mercury_ai.analysis.confluence_score_engine import ConfluenceScoreEngine
from mercury_ai.analysis.decision_explainability import DecisionExplainability

from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.config.institutional_weights import (
    INSTITUTIONAL_WEIGHTS_NORMALIZED,
)

logger = logging.getLogger(__name__)


class MercuryDecisionEngine:
    """
    Orquestrador institucional do Mercury AI.

    Fluxo:

        Validation → Quality → Conflict → Ranking → Memory
        → Confidence → Confluence → Probability
        → Decision Resolver → Narrative → Institutional Score
        → Builder → DecisionResult
    """

    def __init__(
        self,
        executor: PipelineExecutor,
        profiler: Optional[PipelineProfiler] = None,
    ):
        self.executor = executor
        self.profiler = profiler

        self.validation = ValidationEngine()
        self.quality = EvidenceQualityEngine()
        self.ranking = EvidenceRankingEngine()
        self.conflict_resolver = ConflictResolutionEngine()
        self.confidence = ConfidenceEngine()

        # ConfluenceEngine recebe MarketThesisBuilder via DI (SRP)
        self.confluence = ConfluenceEngine(
            thesis_builder=MarketThesisBuilder(
                risk_engine=RiskEngine(),
                confidence_engine=self.confidence,
                state_engine=MarketStateEngine(),
                score_engine=ConfluenceScoreEngine(),
            ),
        )

        self.memory = InstitutionalMemoryEngine()
        self.narrative = NarrativeEngine()
        self.score_engine = InstitutionalScoreEngine()
        self.decision_resolver = DecisionResolverEngine()
        self.builder = DecisionResultBuilder()

        # ProbabilityEngine usa pesos canônicos normalizados
        self.probability_engine = ProbabilityEngine(
            weights={
                "trend": INSTITUTIONAL_WEIGHTS_NORMALIZED["trend"],
                "structure": INSTITUTIONAL_WEIGHTS_NORMALIZED["market_structure"],
                "liquidity": INSTITUTIONAL_WEIGHTS_NORMALIZED["liquidity"],
                "volatility": INSTITUTIONAL_WEIGHTS_NORMALIZED["volatility"],
            }
        )

    # ============================================================
    # PUBLIC ENTRY
    # ============================================================

    def analyze(
        self,
        context: MarketContext,
        evidence_bundle: MarketEvidenceBundle,
        trade_filter_result: TradeFilterResult,
    ) -> DecisionResult:
        return self.executor.execute(
            "AnalyzeDecision",
            self._analyze_logic,
            DecisionResult,
            context,
            evidence_bundle,
            trade_filter_result,
        )

    # ============================================================
    # ORCHESTRATION
    # ============================================================

    def _analyze_logic(
        self,
        context: MarketContext,
        evidence_bundle: MarketEvidenceBundle,
        trade_filter_result: TradeFilterResult,
    ) -> DecisionResult:

        # =====================================================
        # 1) VALIDATION
        # =====================================================
        is_valid, validation_warnings = self.validation.validate_all(
            context, evidence_bundle
        )

        if not trade_filter_result.allowed:
            is_valid = False
            validation_warnings.extend(trade_filter_result.reasons)

        logger.debug("\n================ VALIDATION ================")
        logger.debug("is_valid.......: %s", is_valid)
        logger.debug("trade_allowed..: %s", trade_filter_result.allowed)
        logger.debug("warnings.......: %s", validation_warnings)
        logger.debug("===========================================\n")

        # =====================================================
        # 2) QUALITY
        # =====================================================
        quality_result = self.quality.evaluate(
            list(evidence_bundle.evidences)
        )

        resolved_quality_score = (
            sum(e.quality_score for e in quality_result) / len(quality_result)
            if quality_result
            else 100.0
        )

        logger.debug("========== QUALITY ==========")
        logger.debug("Evidences.......: %d", len(quality_result))
        logger.debug("Average Quality.: %.2f", resolved_quality_score)
        logger.debug("=============================\n")

        # =====================================================
        # 3) CONFLICT
        # =====================================================
        resolved_evidences, conflict_score = (
            self.conflict_resolver.resolve(quality_result, context)
        )

        logger.debug("========== CONFLICT ==========")
        logger.debug("Resolved........: %d", len(resolved_evidences))
        logger.debug("Conflict Score..: %.2f", conflict_score)
        logger.debug("==============================\n")

        # =====================================================
        # 4) RANKING
        # =====================================================
        ranked_result = self.ranking.rank(resolved_evidences)

        # =====================================================
        # 5) MEMORY
        # =====================================================
        consistency_score = self.memory.get_consistency_score(
            context.market.symbol,
            tuple(resolved_evidences),
        )

        logger.debug("========== MEMORY ==========")
        logger.debug("Consistency.....: %.2f", consistency_score)
        logger.debug("============================\n")

        # =====================================================
        # 6) BUNDLE
        # =====================================================
        resolved_bundle = MarketEvidenceBundle(
            evidences=tuple(resolved_evidences),
            timestamp=evidence_bundle.timestamp,
            asset=evidence_bundle.asset,
            timeframe=evidence_bundle.timeframe,
        )

        # =====================================================
        # 7) CONFIDENCE
        # =====================================================
        confidence_result = self.confidence.calculate(
            context, resolved_bundle
        )

        confidence_result = self.confidence.calibrate(
            confidence_result,
            consistency_score,
        )

        logger.debug("")
        logger.debug("========== CONFIDENCE ==========")
        logger.debug("Quality.............: %.2f", confidence_result.average_quality)
        logger.debug("Consensus...........: %.2f", confidence_result.consensus_score)
        logger.debug("Market..............: %.2f", confidence_result.market_score)
        logger.debug("Confirmations.......: %d", confidence_result.confirmation_count)
        logger.debug("Confidence..........: %.2f", confidence_result.final_confidence)
        logger.debug("================================")
        logger.debug("")

        # =====================================================
        # 8) CONFLUENCE
        # =====================================================
        confluence_result, institutional_contributions = self.confluence.analyze(
            context, resolved_bundle
        )

        logger.debug("")
        logger.debug("========== CONFLUENCE ==========")
        logger.debug("BUY Score........: %.2f", confluence_result.buy_score)
        logger.debug("SELL Score.......: %.2f", confluence_result.sell_score)
        logger.debug("NEUTRAL..........: %.2f", confluence_result.neutral_score)
        logger.debug("Agreement........: %.2f", confluence_result.agreement_percentage)
        logger.debug("Weighted.........: %.2f", confluence_result.weighted_score)
        logger.debug("Confidence.......: %.2f", confluence_result.confidence)
        logger.debug("Direction........: %s", confluence_result.dominant_direction)
        logger.debug("================================")
        logger.debug("")

        # =====================================================
        # 9) PROBABILITY
        # =====================================================
        probability_result = self.probability_engine.analyze(
            context=context,
            evidence_bundle=resolved_bundle,
            confluence_score=confluence_result.weighted_score,
            confidence_score=confidence_result.final_confidence,
            dominant_direction=confluence_result.dominant_direction.value,
        )

        logger.debug("")
        logger.debug("========== PROBABILITY ==========")
        logger.debug("BUY..............: %.2f", probability_result.buy_probability)
        logger.debug("SELL.............: %.2f", probability_result.sell_probability)
        logger.debug("WAIT.............: %.2f", probability_result.neutral_probability)
        logger.debug("Grade............: %s", probability_result.opportunity_grade)
        logger.debug("Risk.............: %.2f", probability_result.expected_risk)
        logger.debug("=================================")
        logger.debug("")

        # =====================================================
        # 10) DECISION RESOLVER
        # =====================================================
        resolver_result = self.decision_resolver.resolve(
            dominant_direction=confluence_result.dominant_direction.value,
            is_valid=is_valid,
            opportunity_grade=probability_result.opportunity_grade,
            conflicting_signals=confluence_result.conflicting_signals,
        )

        final_decision = resolver_result.decision

        if resolver_result.confidence_override is not None:
            confidence_result = ConfidenceResult(
                confidence_score=confidence_result.confidence_score,
                final_confidence=resolver_result.confidence_override,
                confidence_grade=self.confidence._get_grade(resolver_result.confidence_override),
                is_high=resolver_result.confidence_override > 70,
                average_quality=confidence_result.average_quality,
                consensus_score=confidence_result.consensus_score,
                market_score=confidence_result.market_score,
                confirmation_count=confidence_result.confirmation_count,
            )

        # =====================================================
        # 10.5) EXPLAINABILITY (coleta, nao altera nada)
        # =====================================================
        explainability = DecisionExplainability(
            decision=final_decision,
            reason=(
                f"Regra {resolver_result.triggered_rule}: "
                f"dominant_direction={confluence_result.dominant_direction.value}, "
                f"grade={probability_result.opportunity_grade}, "
                f"conflict={confluence_result.conflicting_signals}, "
                f"is_valid={is_valid}"
            ),
            dominant_direction=confluence_result.dominant_direction.value,
            opportunity_grade=probability_result.opportunity_grade,
            conflicting_signals=confluence_result.conflicting_signals,
            institutional_score=0.0,  # preenchido apos o score engine
            confidence=confidence_result.final_confidence,
            triggered_rule=resolver_result.triggered_rule,
            contributions=tuple(institutional_contributions),
            decision_chain=(
                f"1.Validation: is_valid={is_valid}",
                f"2.Quality: avg={resolved_quality_score:.2f}",
                f"3.Conflict: score={conflict_score:.2f}",
                f"4.Ranking: {len(ranked_result.ranked_evidences)} evidencias",
                f"5.Memory: consistency={consistency_score:.2f}",
                f"6.Confidence: final={confidence_result.final_confidence:.2f}",
                f"7.Confluence: direction={confluence_result.dominant_direction.value}, weighted={confluence_result.weighted_score:.2f}",
                f"8.Probability: grade={probability_result.opportunity_grade}, buy={probability_result.buy_probability:.2f}, sell={probability_result.sell_probability:.2f}",
                f"9.Resolver: rule={resolver_result.triggered_rule}, decision={final_decision}",
            ),
        )

        # =====================================================
        # 11) NARRATIVE
        # =====================================================
        explanation = self.narrative.generate(
            final_decision,
            list(resolved_bundle.evidences),
            context,
            confluence_result.weighted_score,
        )

        # =====================================================
        # 12) INSTITUTIONAL SCORE
        # =====================================================
        risk = context.risk_assessment

        score_result = self.score_engine.calculate(
            probability_score=max(
                probability_result.buy_probability,
                probability_result.sell_probability,
            ),
            confluence_score=confluence_result.weighted_score,
            confidence_score=confidence_result.final_confidence,
            trade_quality_score=trade_filter_result.quality_score,
            resolved_quality_score=resolved_quality_score,
            risk_score=risk.institutional_risk_score,
            conflict_penalty=conflict_score,
        )

        logger.debug("")
        logger.debug("============= INSTITUTIONAL SCORE =============")
        logger.debug("Probability........: %.2f", score_result.probability_score)
        logger.debug("Confluence.........: %.2f", score_result.confluence_score)
        logger.debug("Confidence.........: %.2f", score_result.confidence_score)
        logger.debug("Trade Quality......: %.2f", score_result.trade_quality_score)
        logger.debug("Resolved Quality...: %.2f", score_result.resolved_quality_score)
        logger.debug("Risk...............: %.2f", score_result.risk_score)
        logger.debug("Conflict Penalty...: %.2f", score_result.conflict_penalty)
        logger.debug("FINAL SCORE........: %.2f", score_result.institutional_score)
        logger.debug("===============================================")

        # Atualiza o explainability com o institutional score real
        explainability = DecisionExplainability(
            decision=explainability.decision,
            reason=explainability.reason,
            dominant_direction=explainability.dominant_direction,
            opportunity_grade=explainability.opportunity_grade,
            conflicting_signals=explainability.conflicting_signals,
            institutional_score=score_result.institutional_score,
            confidence=explainability.confidence,
            triggered_rule=explainability.triggered_rule,
            contributions=explainability.contributions,
            decision_chain=explainability.decision_chain,
        )

        logger.debug("")
        logger.debug("================ FINAL ====================")
        logger.debug("Decision...........: %s", final_decision)
        logger.debug("Confidence.........: %.2f", confidence_result.final_confidence)
        logger.debug("BUY................: %.2f", probability_result.buy_probability)
        logger.debug("SELL...............: %.2f", probability_result.sell_probability)
        logger.debug("WAIT...............: %.2f", probability_result.neutral_probability)
        logger.debug("is_valid...........: %s", is_valid)
        logger.debug("===========================================")

        # =====================================================
        # 13) BUILD
        # =====================================================
        return self.builder.build(
            final_decision=final_decision,
            grade=probability_result.opportunity_grade,
            calibrated_confidence=confidence_result.final_confidence,
            confluence_result=confluence_result,
            risk_score=risk.institutional_risk_score,
            institutional_score=score_result.institutional_score,
            trade_quality_score=trade_filter_result.quality_score,
            ranked_result=ranked_result,
            buy_prob=probability_result.buy_probability,
            sell_prob=probability_result.sell_probability,
            wait_prob=probability_result.neutral_probability,
            expected_risk=risk.suggested_stop,
            expected_reward=risk.suggested_take_profit,
            expected_drawdown=risk.expected_drawdown,
            explanation=explanation,
            resolved_bundle=resolved_bundle,
            final_warnings=list(validation_warnings),
            confidence_result=confidence_result,
            explainability=explainability,
        )
    