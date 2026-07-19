from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_thesis import MarketThesis
from mercury_ai.analysis.risk_engine import RiskEngine
from mercury_ai.analysis.confidence_engine import ConfidenceEngine
from mercury_ai.analysis.market_state_engine import MarketStateEngine
from mercury_ai.analysis.confluence_score_engine import ConfluenceScoreEngine

class MarketThesisBuilder:
    """
    Constrói a tese técnica institucional consolidando dados de todas as engines.

    As engines são injetadas via construtor (Dependency Injection), respeitando SRP:
    a responsabilidade de instanciar as engines é do chamador, não do builder.
    """

    def __init__(
        self,
        risk_engine: RiskEngine,
        confidence_engine: ConfidenceEngine,
        state_engine: MarketStateEngine,
        score_engine: ConfluenceScoreEngine,
    ):
        self.risk_engine = risk_engine
        self.confidence_engine = confidence_engine
        self.state_engine = state_engine
        self.score_engine = score_engine

    def build(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> MarketThesis:
        # Consolidação determinística
        score_data = self.score_engine.calculate(context)
        confidence_data = self.confidence_engine.calculate(context, evidence_bundle)
        risk_data = self.risk_engine.assess(context, evidence_bundle)
        state_data = context.market_state
        
        # Consolidação de Evidências/Conflitos (Exemplo)
        confirmations = []
        conflicts = []
        if score_data.bullish_score > 0: confirmations.append("Bullish Bias")
        
        return MarketThesis(
            market_bias="BUY_SIDE_DOMINANT" if score_data.bullish_score > score_data.bearish_score else "SELL_SIDE_DOMINANT",
            confluence_score=score_data.clarity_score,
            confidence=confidence_data,
            risk=risk_data,
            market_state=state_data,
            confirmations=confirmations,
            conflicts=conflicts,
            institutional_alignment=confidence_data.confidence_score > 60
        )
