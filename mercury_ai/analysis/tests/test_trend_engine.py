import pytest
from mercury_ai.analysis.trend_analyzer import TrendAnalyzer
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.evidence import Evidence

@pytest.fixture
def trend_engine():
    return TrendAnalyzer()

def test_trend_engine_bullish_structure(trend_engine):
    market_data = MarketData(
        symbol="EURUSD",
        timeframe="H1",
        close=1.1000,
        ema9=1.0990,
        ema21=1.0980,
        ema50=1.0970,
        rsi=55.0,
        atr=0.0010,
        adx=35.0,
        macd=0.0001,
        macd_signal=0.0000,
        bollinger_upper=1.1020,
        bollinger_lower=1.0980,
        volume=1000.0
    )
    evidences = trend_engine.analyze(market_data)
    
    assert any(e.direction == "BULLISH" for e in evidences)
    assert any(e.evidence_name == "EMA Alignment" for e in evidences)

def test_trend_engine_bearish_structure(trend_engine):
    market_data = MarketData(
        symbol="EURUSD",
        timeframe="H1",
        close=1.0900,
        ema9=1.0910,
        ema21=1.0920,
        ema50=1.0930,
        rsi=45.0,
        atr=0.0010,
        adx=35.0,
        macd=-0.0001,
        macd_signal=0.0000,
        bollinger_upper=1.0920,
        bollinger_lower=1.0880,
        volume=1000.0
    )
    evidences = trend_engine.analyze(market_data)
    
    assert any(e.direction == "BEARISH" for e in evidences)
    assert any(e.evidence_name == "EMA Alignment" for e in evidences)
