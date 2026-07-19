from mercury_ai.analysis.weight_simulator import WeightSimulator

def test_weight_simulator():
    simulator = WeightSimulator()
    report = simulator.simulate()
    
    assert isinstance(report, dict)
    
    # Check if a known engine exists and has required fields
    if report:
        engine = next(iter(report))
        data = report[engine]
        assert 'current_weight' in data
        assert 'suggested_weight' in data
        assert 'reason' in data
        assert 'statistical_confidence' in data
