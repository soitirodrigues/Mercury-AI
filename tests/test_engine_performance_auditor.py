from mercury_ai.analysis.engine_performance_auditor import EnginePerformanceAuditor

def test_engine_performance_auditor():
    auditor = EnginePerformanceAuditor()
    report = auditor.audit_engines()
    
    assert isinstance(report, dict)
    
    if report:
        # Check an arbitrary engine if present
        engine_name = next(iter(report))
        stats = report[engine_name]
        
        assert 'activations' in stats
        assert 'win_rate' in stats
        assert 0 <= stats['win_rate'] <= 100
        assert 'avg_contribution' in stats
