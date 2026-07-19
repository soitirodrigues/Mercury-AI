from unittest.mock import Mock
from mercury_ai.analysis.context_engine import ContextEngine
from mercury_ai.models.evidence import Evidence
from mercury_ai.core.pipeline_executor import PipelineExecutor
from mercury_ai.core.pipeline_profiler import PipelineProfiler
from mercury_ai.models.market_data import MarketData

def test_context_engine_aggregation():
    executor = PipelineExecutor()
    profiler = Mock(spec=PipelineProfiler)
    engine = ContextEngine(executor, profiler)
    
    evidences = [
        Evidence("Engine1", "E1", "BULLISH", 10.0, 10.0, "Desc", 1.0),
        Evidence("Engine1", "E1", "BULLISH", 10.0, 10.0, "Desc", 1.0), # Duplicate
        Evidence("Engine2", "E2", "BEARISH", 20.0, 20.0, "Desc", 1.0)
    ]
    
    market_data = Mock(spec=MarketData)
    
    context = engine.analyze(evidences, market_data, symbol="EURUSD", timeframe="1H")
    
    assert len(context.trend) == 2
    assert context.market == market_data
