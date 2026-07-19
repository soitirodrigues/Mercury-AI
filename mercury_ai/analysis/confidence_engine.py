from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.confidence_result import ConfidenceResult
from mercury_ai.analysis.evidence_query import EvidenceQuery
from mercury_ai.models.market_state_enum import MarketStateEnum
from mercury_ai.analysis.conflict_resolution_engine import ConflictResolutionEngine

class ConfidenceEngine:
    """
    Motor central para cálculo determinístico de confiança da tese técnica.
    """

    def calculate(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> ConfidenceResult:
        evidences = list(evidence_bundle.evidences)
        if not evidences:
            raise ValueError("ConfidenceEngine requires at least one evidence to calculate a score.")
            
        # 1. Evidence Quality Factor (0.0 to 1.0)
        avg_quality = sum(e.quality_score for e in evidences) / len(evidences) / 100.0
        quality_factor = avg_quality
        
        # 2. Conflict & Consensus Factor (0.0 to 1.0)
        resolver = ConflictResolutionEngine()
        resolved, conflict_score = resolver.resolve(evidences, context)
        
        # Number of independent confirmations (unique engines producing non-neutral signals)
        active_engines = {e.engine_name for e in evidences if e.direction in ("BULLISH", "BEARISH")}
        n_confirmations = len(active_engines)
        
        if n_confirmations == 0:
            confirmation_mult = 0.0
        elif n_confirmations == 1:
            confirmation_mult = 0.5
        elif n_confirmations == 2:
            confirmation_mult = 0.8
        else:
            confirmation_mult = 1.0
            
        consensus_factor = conflict_score * confirmation_mult
        
        # 3. Market Conditions Factor (0.0 to 1.0)
        market_score = 0.5 # Default starting point
        
        # Trend Strength
        if EvidenceQuery.has_strong_trend(context.trend):
            market_score += 0.2
            
        # MTF Agreement
        if context.mtf_consensus:
            mtf_align = context.mtf_consensus.alignment_score / 100.0
            market_score += (mtf_align * 0.2)
            
        # Volatility & Liquidity via MarketStateEnum
        if context.market_state:
            if context.market_state.state == MarketStateEnum.LOW_LIQUIDITY:
                market_score -= 0.15
            elif context.market_state.state == MarketStateEnum.HIGH_VOLATILITY:
                market_score -= 0.05
            elif context.market_state.state == MarketStateEnum.OPEN:
                market_score += 0.1
                
        # Institutional risk penalty
        risk_penalty = 0.0
        if context.risk_assessment:
            risk_penalty = context.risk_assessment.institutional_risk_score
            if risk_penalty > 1.0:
                risk_penalty /= 100.0
        
        market_score -= (risk_penalty * 0.15)
            
        market_factor = max(0.0, min(1.0, market_score))
        
        # 4. Calibration: Calibrated Confidence is a non-linear combination of the three factors
        score = 100.0 * (0.3 * quality_factor + 0.3 * consensus_factor + 0.4 * market_factor)
        
        score = max(0.0, min(100.0, score))
        grade = self._get_grade(score)
        
        return ConfidenceResult(
            confidence_score=score,
            confidence_grade=grade,
            is_high=score > 70
        )

    def _get_grade(self, score: float) -> str:
        if score > 80: return "A"
        if score > 60: return "B"
        if score > 40: return "C"
        return "D"
