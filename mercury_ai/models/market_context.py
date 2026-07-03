from dataclasses import dataclass

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.trend import TrendAnalysis
from mercury_ai.models.price_action import PriceActionAnalysis
from mercury_ai.models.support_resistance import SupportResistanceAnalysis
from mercury_ai.models.smart_money import SmartMoneyAnalysis


@dataclass
class MarketContext:

    market: MarketData

    trend: TrendAnalysis

    price_action: PriceActionAnalysis

    support_resistance: SupportResistanceAnalysis

    smart_money: SmartMoneyAnalysis