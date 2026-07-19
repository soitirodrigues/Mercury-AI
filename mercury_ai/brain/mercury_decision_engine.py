from typing import Optional, List
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.version_metadata import VersionMetadata
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler

# Existing engines
from mercury_ai.analysis.validation_engine import ValidationEngine
from mercury_ai.analysis.evidence_quality_engine import EvidenceQualityEngine
from mercury_ai.analysis.evidence_ranking_engine import EvidenceRankingEngine
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine
from mercury_ai.analysis.confidence_engine import ConfidenceEngine
from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.institutional_memory_engine import InstitutionalMemoryEngine
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.analysis.narrative_engine import NarrativeEngine

class MercuryDecisionEngine:
    def __init__(self, executor: PipelineExecutor, profiler: Optional[PipelineProfiler] = None):
        self.executor = executor
        self.profiler = profiler
        self.validation = ValidationEngine()
        self.quality = EvidenceQualityEngine()
        self.ranking = EvidenceRankingEngine()
        self.conflict_resolver = ConflictResolutionEngine()
        self.confidence = ConfidenceEngine()
        self.confluence = ConfluenceEngine()
        self.memory = InstitutionalMemoryEngine()
        self.probability_engine = ProbabilityEngine(weights={"trend": 0.4, "structure": 0.3, "liquidity": 0.2, "volatility": 0.1})
        self.narrative = NarrativeEngine()

    def analyze(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle, trade_allowed: bool, block_reasons: List[str], quality_score: float, quality_level: str) -> DecisionResult:
        """
        Orchestrates the decision process via executor.
        """
        return self.executor.execute("AnalyzeDecision", self._analyze_logic, DecisionResult, context, evidence_bundle, trade_allowed, block_reasons, quality_score, quality_level)

    def _analyze_logic(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle, trade_allowed: bool, block_reasons: List[str], quality_score: float, quality_level: str) -> DecisionResult:
        # 1. Institutional Validation Layer
        is_valid, validation_warnings = self.validation.validate_all(context, evidence_bundle)
        
        # Apply trade filter result
        if not trade_allowed:
            is_valid = False
            validation_warnings.extend(block_reasons)

        # 2. Data Quality & Evidence Ranking
        quality_res = self.quality.evaluate(list(evidence_bundle.evidences))

        # 3. Conflict Resolution
        resolved_evidences, conflict_score = self.conflict_resolver.resolve(quality_res, context)
        
        # 4. Institutional Memory Adjustment
        consistency_score = self.memory.get_consistency_score(context.market.symbol, tuple(resolved_evidences))

        # 5. Market Regime Influence (Confidence Calibration)
        regime_factor = 1.0
        # Assume MarketRegime is always present in MarketContext
        from mercury_ai.models.market_regime_enum import MarketRegimeEnum
        if context.market_regime.regime in (MarketRegimeEnum.STRONG_UPTREND, MarketRegimeEnum.STRONG_DOWNTREND):
            regime_factor = 1.2
        elif context.market_regime.regime in (MarketRegimeEnum.CONSOLIDATION, MarketRegimeEnum.CONSOLIDATION):
            regime_factor = 0.8
        
        ranked_res = self.ranking.rank(resolved_evidences)
        
        # 6. Confidence and Confluence
        # Use resolved evidences for more accurate analysis
        resolved_bundle = MarketEvidenceBundle(evidences=tuple(resolved_evidences), timestamp=evidence_bundle.timestamp, asset=evidence_bundle.asset, timeframe=evidence_bundle.timeframe)
        conf_res = self.confidence.calculate(context, resolved_bundle)
        
        # Adjust confidence with institutional consistency AND regime factor
        calibrated_confidence = (conf_res.confidence_score + (consistency_score * 10.0)) * regime_factor
        calibrated_confidence = max(0.0, min(100.0, calibrated_confidence))
        
        confluence_res = self.confluence.analyze(context, resolved_bundle)
        
        # 6. Probability Estimation (Institutional calibrated)
        prob_res = self.probability_engine.analyze(
            context, 
            evidence_bundle, 
            confluence_res.weighted_score, 
            calibrated_confidence,
            dominant_direction=confluence_res.dominant_direction.value
        )
        
        buy_prob = prob_res.buy_probability
        sell_prob = prob_res.sell_probability
        wait_prob = prob_res.neutral_probability
        
        if buy_prob > sell_prob and buy_prob > wait_prob:
            decision = "BUY"
            grade = prob_res.opportunity_grade
        elif sell_prob > buy_prob and sell_prob > wait_prob:
            decision = "SELL"
            grade = prob_res.opportunity_grade
        else:
            decision = "WAIT"
            grade = "C"

        # Apply Validation result
        final_decision = decision
        final_confidence = calibrated_confidence
        final_warnings = validation_warnings
        
        if not is_valid:
            final_decision = "WAIT"
            final_confidence = 0.0
        
        # Direct access to risk assessment institutional score
        risk_score = context.risk_assessment.institutional_risk_score

        # Institutional Metrics Derivation (Deterministic)
        # Risk: Distance to Liquidity/OB (approximated from evidence)
        expected_risk = next((e.strength for e in evidence_bundle.evidences if e.engine_name == "RiskEngine"), 10.0)
        # Reward: Distance to next structure point
        expected_reward = next((e.strength for e in evidence_bundle.evidences if e.engine_name == "StructureEngine"), 20.0)
        # Drawdown: Volatility-based
        expected_drawdown = next((e.strength for e in evidence_bundle.evidences if e.engine_name == "VolatilityEngine"), 5.0)

        # 7. Build Explanation
        explanation = self.narrative.generate(final_decision, list(evidence_bundle.evidences), context, confluence_res.weighted_score)
        
        # 8. Build DecisionResult
        import hashlib
        # Deterministic audit_id based on asset and input features, avoiding temporal dependence for replay integrity
        audit_input = f"{evidence_bundle.asset}{evidence_bundle.timeframe}{len(evidence_bundle.evidences)}"
        audit_id = hashlib.sha256(audit_input.encode()).hexdigest()

        # Quality score recalculated for the resolved bundle
        quality_score = sum(e.quality_score for e in resolved_evidences) / len(resolved_evidences) if resolved_evidences else 100.0

        return DecisionResult(
            decision=final_decision,
            grade=grade,
            confidence=final_confidence / 100.0,
            clarity=confluence_res.agreement_percentage,
            risk_score=risk_score,
            score=confluence_res.weighted_score * conflict_score, 
            quality=quality_score,
            expected_strength=ranked_res.total_weight,
            buy_probability=buy_prob,
            sell_probability=sell_prob,
            wait_probability=wait_prob,
            expected_risk=expected_risk,
            expected_reward=expected_reward,
            expected_drawdown=expected_drawdown,
            audit_id=audit_id,
            version_metadata=VersionMetadata(
                engine_version="1.0.4",
                pipeline_version="1.0.4",
                context_version="1.0.4",
                weights_version="1.0.4"
            ),
            explanation=explanation,
            summary=explanation.exec_summary,
            technical_reason=explanation.decision_rationale,
            warnings=tuple(list(explanation.warnings) + list(final_warnings)),
            weaknesses=tuple(f"{e.engine_name} low quality" for e in evidence_bundle.evidences if e.quality_score < 50),
            blockers=explanation.conflicts,
            institutional_alignment=conf_res.is_high,
            evidence_ranking=ranked_res
        )
