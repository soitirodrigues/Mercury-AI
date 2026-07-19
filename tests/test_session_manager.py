from mercury_ai.core.session_manager import SessionManager

def test_session_manager():
    sm = SessionManager(operator="Test_Admin")
    info = sm.get_info()
    
    assert 'session_id' in info
    assert info['operator'] == "Test_Admin"
    assert info['version'] == "0.1"
    assert info['environment'] == "DEMO"
    assert 'timestamp' in info
