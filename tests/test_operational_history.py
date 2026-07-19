from mercury_ai.analysis.operational_history import OperationalHistory

def test_operational_history_query():
    history = OperationalHistory()
    results = history.query()
    
    # Should not crash even if empty
    assert isinstance(results, list)
    
    if results:
        # Check required fields
        item = results[0]
        assert 'timestamp' in item
        assert 'asset' in item
        assert 'decision' in item
        assert 'narrative' in item
        assert 'probability' in item
        assert 'buy' in item['probability']
        assert 'result' in item
