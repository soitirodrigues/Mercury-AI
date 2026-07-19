from unittest.mock import MagicMock
from mercury_ai.brain.explainability_engine import ExplainabilityEngine
from mercury_ai.models.analysis_result import AnalysisDirection
from mercury_ai.models.confluence_result import ConfluenceResult
from mercury_ai.models.probability_result import ProbabilityResult

def test_explainability_engine_analysis():
    engine = ExplainabilityEngine()
    
    prob = ProbabilityResult(72.0, 5.0, 0.1, "EXECUTE", 90.0, "HIGH")
    conf = ConfluenceResult(80.0, 70.0, 0.0, 50.0, True, 2, 80.0, 80.0, AnalysisDirection.BUY, (), ())
    
    # Mocking analysis results to fulfill the engine's expected interface
    mock_res_1 = MagicMock()
    mock_res_1.engine_name = "EngineA"
    mock_res_1.direction = AnalysisDirection.BUY
    mock_res_1.confidence = 0.9
    
    mock_res_2 = MagicMock()
    mock_res_2.engine_name = "EngineB"
    mock_res_2.direction = AnalysisDirection.SELL
    mock_res_2.confidence = 0.7
    
    analyses = (mock_res_1, mock_res_2)
    
    explanation = engine.analyze(prob, conf, analyses)
    
    assert "BUY" in explanation.exec_summary
    assert len(explanation.bullish_factors) == 1
    assert len(explanation.bearish_factors) == 1
    assert len(explanation.conflicts) == 1
    assert explanation.risk_analysis == "Risk factor: 0.10. Class: HIGH."
