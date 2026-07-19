from mercury_ai.core.analysis_pipeline import AnalysisPipeline
from mercury_ai.data.market_data import MarketDataService
from mercury_ai.providers.mercury_data_provider import MercuryDataProvider

from mercury_ai.presentation.signal_formatter import SignalFormatter



provider = MercuryDataProvider()


service = MarketDataService(
    provider_manager=provider
)


pipeline = AnalysisPipeline(
    service,
    [provider]
)



result = pipeline.analyze(
    "GC=F"
)



formatter = SignalFormatter()


formatter.format(
    result,
    "OURO"
)