from unittest.mock import MagicMock
from mercury_ai.analysis.market_regime_engine import MarketRegimeEngine
from mercury_ai.models.market_regime_enum import MarketRegimeEnum

def test_market_regime_compression():
    engine = MarketRegimeEngine()
    market = MagicMock()
    market.adx = 10.0
    market.atr = 0.001
    market.ema9 = 1.0
    
    smart_money = MagicMock()
    structure = MagicMock()
    volume = MagicMock()
    
    regime = engine.analyze(market, smart_money, structure, volume)
    assert regime == MarketRegimeEnum.COMPRESSION

def test_market_regime_strong_uptrend():
    engine = MarketRegimeEngine()
    market = MagicMock()
    market.adx = 35.0
    market.atr = 1.0
    market.ema9 = 1.0
    market.ema50 = 90.0
    market.close = 100.0
    
    smart_money = MagicMock()
    structure = MagicMock()
    structure.trend = "BULLISH"
    volume = MagicMock()
    
    regime = engine.analyze(market, smart_money, structure, volume)
    assert regime == MarketRegimeEnum.STRONG_UPTREND
