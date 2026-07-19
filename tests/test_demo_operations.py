from mercury_ai.operations.demo_manager import DemoOperationsManager

def test_demo_simulation():
    manager = DemoOperationsManager()
    results = manager.run_simulation()
    
    # Valida se a simulação gerou registros
    assert isinstance(results, list)
    
    if results:
        entry = results[0]
        assert 'timestamp' in entry
        assert 'asset' in entry
        assert 'decision' in entry
        assert 'snapshot' in entry
        assert 'statistics' in entry
