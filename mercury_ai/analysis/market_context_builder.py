from mercury_ai.analysis.trend_analyzer import TrendAnalyzer
from mercury_ai.analysis.support_resistance_analyzer import SupportResistanceAnalyzer
from mercury_ai.analysis.price_action_analyzer import PriceActionAnalyzer

from mercury_ai.models.market_context import MarketContext


class MarketContextBuilder:

    def __init__(self):
        self.trend = TrendAnalyzer()
        self.support_resistance = SupportResistanceAnalyzer()
        self.price_action = PriceActionAnalyzer()

    def build(self, dataframe, market, smart_money):

        return MarketContext(
            market=market,
            trend=self.trend.analyze(market),
            support_resistance=self.support_resistance.analyze(dataframe),
            price_action=self.price_action.analyze(dataframe),
            smart_money=smart_money
        )