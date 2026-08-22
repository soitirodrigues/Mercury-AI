from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine

engine = DecisionResolverEngine()

# Test 1: is_valid=False -> WAIT
result = engine.resolve(dominant_direction='BUY', is_valid=False)
print(f'Test 1 - is_valid=False: decision={result.decision}, rule={result.triggered_rule}')

# Test 2: dominant_direction=NEUTRAL -> WAIT
result = engine.resolve(dominant_direction='NEUTRAL', is_valid=True)
print(f'Test 2 - NEUTRAL: decision={result.decision}, rule={result.triggered_rule}')

# Test 3: BUY with no other conditions -> BUY
result = engine.resolve(dominant_direction='BUY', is_valid=True, opportunity_grade='C', conflicting_signals=False)
print(f'Test 3 - BUY C no conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 4: SELL with no other conditions -> SELL
result = engine.resolve(dominant_direction='SELL', is_valid=True, opportunity_grade='C', conflicting_signals=False)
print(f'Test 4 - SELL C no conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 5: BUY + Grade D no conflict -> what happens?
result = engine.resolve(dominant_direction='BUY', is_valid=True, opportunity_grade='D', conflicting_signals=False)
print(f'Test 5 - BUY D no conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 6: SELL + Grade D no conflict -> what happens?
result = engine.resolve(dominant_direction='SELL', is_valid=True, opportunity_grade='D', conflicting_signals=False)
print(f'Test 6 - SELL D no conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 7: BUY + Grade D + conflicting_signals -> WAIT?
result = engine.resolve(dominant_direction='BUY', is_valid=True, opportunity_grade='D', conflicting_signals=True)
print(f'Test 7 - BUY D with conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 8: SELL + Grade D + conflicting_signals -> WAIT?
result = engine.resolve(dominant_direction='SELL', is_valid=True, opportunity_grade='D', conflicting_signals=True)
print(f'Test 8 - SELL D with conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 9: conflict + Grade C -> WAIT?
result = engine.resolve(dominant_direction='BUY', is_valid=True, opportunity_grade='C', conflicting_signals=True)
print(f'Test 9 - BUY C with conflict: decision={result.decision}, rule={result.triggered_rule}')

# Test 10: Fallback case
result = engine.resolve(dominant_direction='UNKNOWN', is_valid=True, opportunity_grade='X', conflicting_signals=False)
print(f'Test 10 - Fallback: decision={result.decision}, rule={result.triggered_rule}')