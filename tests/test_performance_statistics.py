from mercury_ai.analysis.performance_statistics import PerformanceStatistics

def test_performance_statistics():
    stats = PerformanceStatistics()
    results = stats.calculate()
    
    # Should not crash
    assert isinstance(results, dict)
    
    if 'win_rate' in results:
        assert 0 <= results['win_rate'] <= 100
        assert isinstance(results['profit_factor'], (float, int))
