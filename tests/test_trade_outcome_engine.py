from mercury_ai.analysis.trade_outcome_engine import TradeOutcomeEngine

def test_trade_outcome_engine():
    # Mock snapshot
    snapshot = {
        'decision_result': {
            'decision': 'BUY',
            'explanation': {
                'suggested_stop': 90.0,
                'suggested_targets': [110.0]
            }
        }
    }
    
    # Test WIN
    assert TradeOutcomeEngine.determine_outcome(snapshot, 115.0) == "WIN"
    # Test LOSS
    assert TradeOutcomeEngine.determine_outcome(snapshot, 85.0) == "LOSS"
    # Test OPEN
    assert TradeOutcomeEngine.determine_outcome(snapshot, 100.0) == "OPEN"
    
    # Test SELL WIN
    snapshot['decision_result']['decision'] = 'SELL'
    snapshot['decision_result']['explanation']['suggested_stop'] = 110.0
    snapshot['decision_result']['explanation']['suggested_targets'] = [90.0]
    
    assert TradeOutcomeEngine.determine_outcome(snapshot, 85.0) == "WIN"
    assert TradeOutcomeEngine.determine_outcome(snapshot, 115.0) == "LOSS"
