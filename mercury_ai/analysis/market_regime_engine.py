from mercury_ai.models.market_regime import MarketRegime
from mercury_ai.models.market_regime_enum import MarketRegimeEnum


class MarketRegimeEngine:
    """
    Motor institucional responsável por classificar o regime do mercado.

    Regra arquitetural Mercury AI:

        Engines retornam Domain Models.

    Nunca retornam Enum, dict ou tuple.
    """

    def analyze(
        self,
        market,
        smart_money,
        structure,
        volume
    ) -> MarketRegime:

        adx = market.adx
        atr = market.atr
        ema9 = market.ema9

        regime = MarketRegimeEnum.UNKNOWN
        confidence = 0.50

        # ---------------------------------
        # Compressão
        # ---------------------------------

        if atr < (ema9 * 0.005):

            regime = MarketRegimeEnum.COMPRESSION
            confidence = 0.85

        # ---------------------------------
        # Tendência
        # ---------------------------------

        elif structure is not None:

            trend = structure.trend

            if trend == "BULLISH":

                if adx > 30:

                    regime = MarketRegimeEnum.STRONG_UPTREND
                    confidence = 0.95

                elif adx > 20:

                    regime = MarketRegimeEnum.WEAK_UPTREND
                    confidence = 0.75

            elif trend == "BEARISH":

                if adx > 30:

                    regime = MarketRegimeEnum.STRONG_DOWNTREND
                    confidence = 0.95

                elif adx > 20:

                    regime = MarketRegimeEnum.WEAK_DOWNTREND
                    confidence = 0.75

        # ---------------------------------
        # Smart Money
        # ---------------------------------

        if (
            smart_money is not None
            and smart_money.structure is not None
            and (
                (smart_money.structure.higher_high and smart_money.structure.lower_low)
                or (smart_money.structure.lower_high and smart_money.structure.higher_low)
            )
        ):

            regime = MarketRegimeEnum.REVERSAL_TRANSITION
            confidence = max(confidence, 0.90)

        # ---------------------------------
        # Volume
        # ---------------------------------

        if volume is not None:

            absorption = getattr(volume, 'absorption', False)
            buying_climax = getattr(volume, 'buying_climax', False)
            selling_climax = getattr(volume, 'selling_climax', False)
            dry_volume = getattr(volume, 'dry_volume', False)

            if (isinstance(absorption, bool) and absorption) or (isinstance(buying_climax, bool) and buying_climax):

                regime = MarketRegimeEnum.ACCUMULATION
                confidence = max(confidence, 0.80)

            elif (isinstance(selling_climax, bool) and selling_climax) or (isinstance(dry_volume, bool) and dry_volume):

                regime = MarketRegimeEnum.DISTRIBUTION
                confidence = max(confidence, 0.80)

        # ---------------------------------
        # Consolidação
        # ---------------------------------

        if regime == MarketRegimeEnum.UNKNOWN:

            if adx < 15:

                regime = MarketRegimeEnum.CONSOLIDATION
                confidence = 0.70

            elif atr > (ema9 * 0.02):

                regime = MarketRegimeEnum.EXPANSION
                confidence = 0.70

        return MarketRegime(
            regime=regime,
            confidence=confidence,
            supporting_evidences=[]
        )
