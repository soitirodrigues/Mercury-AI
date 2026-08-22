from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine

resolver = DecisionResolverEngine()

print("=== CASE A: BUY, Grade D, valid, no conflicts ===")
result = resolver.resolve(dominant_direction="BUY", is_valid=True, opportunity_grade="D", conflicting_signals=False)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "BUY", f"Expected BUY, got {result.decision}"
print("PASS")

print("\n=== CASE B: SELL, Grade D, valid, no conflicts ===")
result = resolver.resolve(dominant_direction="SELL", is_valid=True, opportunity_grade="D", conflicting_signals=False)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "SELL", f"Expected SELL, got {result.decision}"
print("PASS")

print("\n=== CASE C: BUY, Grade C, valid, WITH conflicts ===")
result = resolver.resolve(dominant_direction="BUY", is_valid=True, opportunity_grade="C", conflicting_signals=True)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n=== CASE D: SELL, Grade C, valid, WITH conflicts ===")
result = resolver.resolve(dominant_direction="SELL", is_valid=True, opportunity_grade="C", conflicting_signals=True)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n=== CASE E: BUY, is_valid=False ===")
result = resolver.resolve(dominant_direction="BUY", is_valid=False)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n=== CASE F: NEUTRAL, is_valid=True ===")
result = resolver.resolve(dominant_direction="NEUTRAL", is_valid=True)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n=== CASE G: BUY, confluence below threshold ===")
result = resolver.resolve(dominant_direction="BUY", is_valid=True, opportunity_grade="D", confluence_score=30.0)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n=== CASE H: SELL, confluence below threshold ===")
result = resolver.resolve(dominant_direction="SELL", is_valid=True, opportunity_grade="D", confluence_score=30.0)
print(f"Result: decision={result.decision}, rule={result.triggered_rule}")
assert result.decision == "WAIT", f"Expected WAIT, got {result.decision}"
print("PASS")

print("\n\n=== ALL TESTS PASSED ===")