import pytest
from mercury_ai.core.security_center import SecurityCenter

def test_security_center_functionality():
    sc = SecurityCenter()
    
    # Log events
    sc.log_event("admin", "LOGIN", "System", "INFO")
    sc.log_event("scanner", "SCAN", "Provider", "INFO")
    sc.log_event("admin", "DELETE", "Snapshot", "CRITICAL")
    
    # Audit Trail check
    trail = sc.generate_audit_trail()
    assert len(trail) == 3
    assert trail[2]["severity"] == "CRITICAL"
    
    # Security Report check
    report = sc.generate_security_report()
    assert report["total_events"] == 3
    assert report["critical_events"] == 1
    assert report["status"] == "WARNING"
