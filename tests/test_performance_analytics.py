from mercury_ai.analysis.performance_analytics import PerformanceAnalytics

def test_performance_analytics():
    analytics = PerformanceAnalytics()
    report = analytics.analyze_performance()
    
    # Valida estrutura do relatório
    assert isinstance(report, list)
    
    if report:
        item = report[0]
        assert 'timestamp' in item
        assert 'asset' in item
        assert 'decision' in item
        assert 'result' in item
        assert 'mae' in item
        assert 'mfe' in item
        assert 'duration_hours' in item
        assert item['result'] in ["GAIN", "LOSS", "OPEN"]
