import pytest
import pandas as pd
from mercury_ai.analysis.candlestick_engine import CandlestickEngine

from mercury_ai.models.market_data import MarketData
from mercury_ai.models.market_condition import MarketCondition

def test_candlestick_engine_doji():
    engine = CandlestickEngine()
    df = pd.DataFrame({
        'Open': [100.0, 100.01],
        'High': [102.0, 100.2],
        'Low': [99.0, 99.9],
        'Close': [100.0, 100.01]
    })
    market = MarketData(
        symbol="TEST", timeframe="5m", close=100.0, ema9=100.0, ema21=100.0, ema50=100.0,
        rsi=50.0, atr=1.0, adx=20.0, macd=0.0, macd_signal=0.0,
        bollinger_upper=105.0, bollinger_lower=95.0, volume=1000.0
    )
    trend = []
    mc = MarketCondition(trend="SIDEWAYS", trend_strength=50.0, market_state="RANGING", explanation="")
    
    analysis, engine_result = engine.analyze(df, market, trend, mc)
    
    assert analysis.pattern == "DOJI"
    assert engine_result.execution_time > 0
    assert len(engine_result.evidences) > 0

def test_candlestick_engine_insufficient_data():
    engine = CandlestickEngine()
    df = pd.DataFrame({'Open': [100.0], 'High': [102.0], 'Low': [99.0], 'Close': [100.0]})
    market = MarketData(
        symbol="TEST", timeframe="5m", close=100.0, ema9=100.0, ema21=100.0, ema50=100.0,
        rsi=50.0, atr=1.0, adx=20.0, macd=0.0, macd_signal=0.0,
        bollinger_upper=105.0, bollinger_lower=95.0, volume=1000.0
    )
    trend = []
    mc = MarketCondition(trend="SIDEWAYS", trend_strength=50.0, market_state="RANGING", explanation="")
    
    analysis, engine_result = engine.analyze(df, market, trend, mc)
    
    assert analysis.pattern == "NONE"
    assert "Dados insuficientes" in engine_result.warnings
