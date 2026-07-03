from mercury_ai.config.settings import ASSET

from mercury_ai.data.market_data import MarketDataService
from mercury_ai.data.indicator_engine import IndicatorEngine

from mercury_ai.models.market_data import MarketData

from mercury_ai.analysis.market_context_builder import MarketContextBuilder
from mercury_ai.analysis.confluence_engine import ConfluenceEngine

from mercury_ai.brain.decision_engine import DecisionEngine


class MercuryBrain:

    def __init__(self):

        self.market_service = MarketDataService()
        self.indicator_engine = IndicatorEngine()
        self.context_builder = MarketContextBuilder()
        self.confluence_engine = ConfluenceEngine()
        self.decision_engine = DecisionEngine()

    def analyze(self):

        # ---------------------------------------
        # Baixa os candles
        # ---------------------------------------

        df = self.market_service.get_data(ASSET)

        if df is None or len(df) == 0:
            raise Exception("Não foi possível obter dados do mercado.")

        # ---------------------------------------
        # Calcula indicadores
        # ---------------------------------------

        indicators = self.indicator_engine.calculate(df)

        # ---------------------------------------
        # Cria objeto MarketData
        # ---------------------------------------

        market = MarketData(

            symbol=ASSET,
            timeframe="M5",

            **indicators

        )

        # ---------------------------------------
        # Monta contexto completo
        # ---------------------------------------

        context = self.context_builder.build(df, market)

        # ---------------------------------------
        # Confluência
        # ---------------------------------------

        result = self.confluence_engine.analyze(context)

        # ---------------------------------------
        # Último preço
        # ---------------------------------------

        current_price = market.close

        # ---------------------------------------
        # Recomendação
        # ---------------------------------------

        recommendation = result.to_recommendation()

        # ---------------------------------------
        # Gera sinal
        # ---------------------------------------

        signal = self.decision_engine.generate(

            asset=ASSET,

            recommendation=recommendation,

            current_price=current_price

        )

        return signal