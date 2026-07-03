from dataclasses import dataclass

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.trend import TrendAnalysis
from mercury_ai.models.smart_money import SmartMoneyAnalysis
from mercury_ai.models.confluence import ConfluenceResult


@dataclass
class AnalysisResult:

    market: MarketData

    context: MarketContext

    trend: TrendAnalysis

    smart_money: SmartMoneyAnalysis

    confluence: ConfluenceResult