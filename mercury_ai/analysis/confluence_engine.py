from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.analysis_result import AnalysisDirection
from mercury_ai.models.market_context import MarketContext
from mercury_ai.analysis.market_thesis_builder import MarketThesisBuilder
from mercury_ai.analysis.decision_trace_engine import DecisionTraceEngine

# Institutional Weights
INSTITUTIONAL_WEIGHTS = {
    "LiquidityEngine": 25.0,
    "SmartMoneyEngine": 20.0,
    "MarketStructureIntelligenceEngine": 15.0,
    "VolumeIntelligenceEngine": 10.0,
    "TrendAnalyzer": 10.0,
    "CandlestickEngine": 10.0,
    "VolatilityEngine": 5.0,
    "ConfluenceEngine": 5.0,
}

class ConfluenceEngine:

    def __init__(self):
        self.thesis_builder_engine = MarketThesisBuilder()
        self.trace_engine = DecisionTraceEngine()

    def analyze(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> ConfluenceResult:
        bullish_score = 0.0
        bearish_score = 0.0
        conflicting_signals = False
        
        # Weighted Aggregation
        for evidence in evidence_bundle.evidences:
            weight = INSTITUTIONAL_WEIGHTS.get(evidence.engine_name, 1.0)
            contribution = (evidence.strength / 100.0) * weight
            
            if evidence.direction == "BULLISH":
                bullish_score += contribution
            elif evidence.direction == "BEARISH":
                bearish_score += contribution
        
        # Risk & Conflict Penalty
        risk_penalty = context.risk_assessment.institutional_risk_score * 0.5
        conflict_penalty = 0.0
        if bullish_score > 0 and bearish_score > 0:
            conflicting_signals = True
            conflict_penalty = max(bullish_score, bearish_score) * 0.8
            
        total_weighted_score = max(bullish_score, bearish_score)
        net_score = max(total_weighted_score - risk_penalty - conflict_penalty, 0.0)
        
        # Determine dominant direction
        if bullish_score > bearish_score * 1.2:
            direction = AnalysisDirection.BUY
        elif bearish_score > bullish_score * 1.2:
            direction = AnalysisDirection.SELL
        else:
            direction = AnalysisDirection.NEUTRAL
        
        # Construção da tese
        thesis = self.thesis_builder_engine.build(context, evidence_bundle)
        
        return ConfluenceResult(
            buy_score=bullish_score,
            sell_score=bearish_score,
            neutral_score=0.0,
            agreement_percentage=(net_score / sum(INSTITUTIONAL_WEIGHTS.values())) * 100.0,
            conflicting_signals=conflicting_signals,
            independent_confirmations=len(evidence_bundle.evidences),
            weighted_score=net_score,
            confidence=thesis.confidence.confidence_score,
            dominant_direction=direction,
            evidences=tuple(thesis.confirmations),
            warnings=()
        )
