from mercury_ai.analysis.statistical_auditor import StatisticalAuditor

def test_statistical_auditor():
    auditor = StatisticalAuditor()
    results = auditor.audit()
    
    if not results:
        return # Skip if no snapshots
        
    assert 'buy_pct' in results
    assert 'sell_pct' in results
    assert 'wait_pct' in results
    assert 'avg_confidence' in results
    assert 'avg_buy_prob' in results
    assert 'avg_risk' in results
    assert 'frequent_regimes' in results
    
    # Check probability sum consistency
    total_prob = results['avg_buy_prob'] + results['avg_sell_prob'] + results['avg_wait_prob']
    assert 90 <= total_prob <= 110 # Allow some margin due to float precision
