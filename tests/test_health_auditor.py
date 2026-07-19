from mercury_ai.analysis.health_auditor import HealthAuditor

def test_health_auditor():
    auditor = HealthAuditor()
    report = auditor.generate_report()
    
    assert isinstance(report, dict)
    assert report["Pipeline"] == "OK"
    assert report["Persistência"] == "OK"
    assert "Snapshot Logger" in report
