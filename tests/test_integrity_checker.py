from mercury_ai.analysis.integrity_checker import IntegrityChecker

def test_integrity_checker():
    checker = IntegrityChecker()
    issues = checker.check_all()
    
    # Should not crash. Report should be a list.
    assert isinstance(issues, list)
    
    # If issues were found, they would be printed or handled. 
    # For now, check if the system returns a list without crashing.
    if issues:
        print(f"Integrity issues found: {issues}")
