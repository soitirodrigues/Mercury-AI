from typing import Dict
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_regime_enum import MarketRegimeEnum

class AdaptiveWeightEngine:
    """
    Motor institucional para cálculo adaptativo e determinístico de pesos.
    """

    def calculate_weights(self, context: MarketContext) -> Dict[str, float]:
        """
        Calcula pesos baseados em regime, volatilidade e contexto.
        """
        # Pesos Base
        weights = {
            "Trend": 1.0,
            "Liquidity": 1.0,
            "Volatility": 1.0,
            "Structure": 1.0,
            "SmartMoney": 1.0
        }
        
        # Ajustes baseados em Regime
        market_regime = context.market_regime if context and context.market_regime else MarketRegimeEnum.UNKNOWN
        
        if hasattr(market_regime, 'regime'):
            regime = market_regime.regime
        else:
            regime = market_regime
        
        if regime in [MarketRegimeEnum.STRONG_UPTREND, MarketRegimeEnum.WEAK_UPTREND, 
                      MarketRegimeEnum.STRONG_DOWNTREND, MarketRegimeEnum.WEAK_DOWNTREND]:
            weights["Trend"] *= 1.5
            weights["Structure"] *= 1.2
        elif regime in [MarketRegimeEnum.CONSOLIDATION, MarketRegimeEnum.ACCUMULATION, MarketRegimeEnum.DISTRIBUTION]:
            weights["Liquidity"] *= 1.5
            weights["SmartMoney"] *= 1.3
        elif regime == MarketRegimeEnum.EXPANSION:
            weights["Volatility"] *= 1.8
            weights["Trend"] *= 0.5
            
        # Ajustes baseados em Sessão (Ex: Alta liquidez em NY/London)
        # O contexto precisa ter informação de sessão.
        
        return weights
