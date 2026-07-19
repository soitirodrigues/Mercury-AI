from mercury_ai.analysis.health_checker import HealthChecker

def test_health_checker():
    checker = HealthChecker()
    status = checker.check()
    
    assert status.system_ready is True
    assert "Data Providers" in status.components
    assert status.components["AnalysisPipeline"] == "OK"
    assert status.components["Demo Mode"] == "ACTIVE"
