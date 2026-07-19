from mercury_ai.analysis.performance_center import PerformanceCenter

def test_performance_center():
    center = PerformanceCenter()
    report = center.get_report()
    
    assert isinstance(report, dict)
    assert "Win Rate" in report
    assert "Profit Factor" in report
    assert "Drawdown" in report
    assert "Média Confidence" in report
    assert "Distribuição BUY" in report
