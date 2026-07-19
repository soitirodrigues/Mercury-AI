from typing import List, Tuple
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.market_regime_enum import MarketRegimeEnum

class InstitutionalTradeFilterEngine:
    """
    Motor institucional de filtragem de trades.
    """

    def evaluate(self, context: MarketContext, evidence_bundle: MarketEvidenceBundle) -> Tuple[bool, List[str], float, str]:
        """
        Avalia se o trade é permitido.
        Retorna (allowed, block_reasons, quality_score, quality_level).
        """
        reasons = []
        
        # 1. Regime Filtering
        if context.market_regime and context.market_regime.regime == MarketRegimeEnum.COMPRESSION:
            reasons.append("Compression Regime")
            
        # 2. Confidence Filtering
        # Assuming the evidence bundle doesn't have a direct confidence, using ranking/confluence as proxy
        # Placeholder: logic based on internal evidence count
        if len(evidence_bundle.evidences) < 3:
            reasons.append("Insufficient Confluence")
            
        # 3. Liquidity/Volatility/ATR (Stub: implement logic based on context data)
        # Placeholder: logic for low ATR
        if context.market.atr < 0.0001:
            reasons.append("Low ATR")
            
        # Calculation
        allowed = len(reasons) == 0
        quality_score = max(0.0, 100.0 - (len(reasons) * 20.0))
        quality_level = "A" if quality_score >= 80 else "B" if quality_score >= 60 else "C"
        
        return allowed, reasons, quality_score, quality_level
