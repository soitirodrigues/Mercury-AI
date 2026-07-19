from mercury_ai.models.market_regime_enum import MarketRegimeEnum

class MarketRegimeEngine:
    """
    Motor institucional de classificação de regime de mercado.
    """

    def analyze(self, market, smart_money, structure, volume) -> MarketRegimeEnum:
        """
        Classifica o regime de mercado de forma determinística baseada em evidências institucionais.
        """
        adx = market.adx or 0
        atr = market.atr or 0
        ema9 = market.ema9 or 1
        
        # Estrutura de classificação hierárquica
        # 1. Volatilidade e Compression
        if atr < (ema9 * 0.005):
            return MarketRegimeEnum.COMPRESSION
        
        # 2. Smart Money e Estrutura
        if structure.trend == "BULLISH":
            if adx > 30: return MarketRegimeEnum.STRONG_UPTREND
            if adx > 20: return MarketRegimeEnum.WEAK_UPTREND
        elif structure.trend == "BEARISH":
            if adx > 30: return MarketRegimeEnum.STRONG_DOWNTREND
            if adx > 20: return MarketRegimeEnum.WEAK_DOWNTREND
        
        # 3. Transições e Regimes de Volume
        if smart_money.is_choch_detected:
            return MarketRegimeEnum.REVERSAL_TRANSITION
            
        if volume.is_accumulating:
            return MarketRegimeEnum.ACCUMULATION
        if volume.is_distributing:
            return MarketRegimeEnum.DISTRIBUTION
            
        # 4. Falha de tendência e volatilidade
        if adx < 15:
            return MarketRegimeEnum.CONSOLIDATION
        
        if atr > (ema9 * 0.02):
            return MarketRegimeEnum.EXPANSION
            
        return MarketRegimeEnum.UNKNOWN
