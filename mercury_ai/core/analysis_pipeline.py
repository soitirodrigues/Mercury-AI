from mercury_ai.data.market_data import MarketDataService
from mercury_ai.data.indicator_engine import IndicatorEngine

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.analysis_result import AnalysisResult

from mercury_ai.analysis.market_context_builder import MarketContextBuilder
from mercury_ai.analysis.confluence_engine import ConfluenceEngine
from mercury_ai.analysis.smart_money.smart_money_engine import SmartMoneyEngine
from mercury_ai.analysis.trend_analyzer import TrendAnalyzer


class AnalysisPipeline:

    def __init__(self):

        self.market_service = MarketDataService()
        self.indicators = IndicatorEngine()

        self.trend = TrendAnalyzer()
        self.context_builder = MarketContextBuilder()
        self.smart_money = SmartMoneyEngine()
        self.confluence = ConfluenceEngine()

    def analyze(self, symbol="GC=F"):

        # Dados do mercado
        df = self.market_service.get_data(symbol)

        # Indicadores
        indicator_data = self.indicators.calculate(df)

        market = MarketData(
            symbol=symbol,
            timeframe="M5",
            **indicator_data
        )

        # Análises
        trend = self.trend.analyze(market)

        smart_money = self.smart_money.analyze(df)

        context = self.context_builder.build(
            dataframe=df,
            market=market,
            smart_money=smart_money
        )

        confluence = self.confluence.analyze(context)

        # Resultado final
        return AnalysisResult(
            market=market,
            context=context,
            trend=trend,
            smart_money=smart_money,
            confluence=confluence
        )