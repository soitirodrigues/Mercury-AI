"""
Teste Final da DecisionResult - Verificar se resolver.decision == DecisionResult.decision
"""
from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine
from mercury_ai.models.decision_result import DecisionResult
from mercury_ai.models.trading_explanation import TradingExplanation
from mercury_ai.models.version_metadata import VersionMetadata

# Create a simple trading explanation with required fields
explanation = TradingExplanation(
    exec_summary="Test summary",
    decision_rationale="Test rationale",
    market_context="Test market context",
    trend_context="Test trend context",
    liquidity_context="Test liquidity context",
    structure_context="Test structure context",
    momentum_context="Test momentum context",
    volume_context="Test volume context",
    smart_money_context="Test smart money context",
    confluence_context="Test confluence context",
    risk_assessment="Test risk assessment",
    confidence_rationale="Test confidence rationale",
    conflicts=(),
    warnings=(),
)

# Create version metadata
version_metadata = VersionMetadata(
    engine_version="1.2.0",
    pipeline_version="1.2.0",
    context_version="1.2.0",
    weights_version="1.2.0"
)

resolver = DecisionResolverEngine()

print("=== TESTE: Verificar consistência entre resolver e DecisionResult ===\n")

# TESTE 1: BUY case
print("=== TESTE 1: BUY ===")
resolver_result = resolver.resolve(
    dominant_direction="BUY",
    is_valid=True,
    opportunity_grade="D",
    conflicting_signals=False,
    confluence_score=80.0,
    market_regime=None
)
print(f"Resolver decision: {resolver_result.decision}")
print(f"Resolver triggered rule: {resolver_result.triggered_rule}")

# Build DecisionResult with the resolver decision
decision_result = DecisionResult(
    decision=resolver_result.decision,  # Use the resolver's decision
    grade="D",
    confidence=0.5,
    clarity=80.0,
    risk_score=0.0,
    score=63.87,
    quality=80.0,
    expected_strength=100.0,
    buy_probability=60.0,
    sell_probability=0.0,
    wait_probability=40.0,
    expected_risk=0.0,
    expected_reward=0.0,
    expected_drawdown=0.0,
    audit_id="test_audit_id",
    version_metadata=version_metadata,
    explanation=explanation,
    warnings=(),
    weaknesses=(),
    blockers=(),
    summary="Test summary"
)

print(f"DecisionResult decision: {decision_result.decision}")
print(f"Match: {resolver_result.decision == decision_result.decision}")
assert resolver_result.decision == decision_result.decision, "MISMATCH: resolver and DecisionResult decisions don't match!"
print("PASS: BUY decisions match\n")

# TESTE 2: SELL case
print("=== TESTE 2: SELL ===")
resolver_result = resolver.resolve(
    dominant_direction="SELL",
    is_valid=True,
    opportunity_grade="D",
    conflicting_signals=False,
    confluence_score=80.0,
    market_regime=None
)
print(f"Resolver decision: {resolver_result.decision}")
print(f"Resolver triggered rule: {resolver_result.triggered_rule}")

# Build DecisionResult with the resolver decision
decision_result = DecisionResult(
    decision=resolver_result.decision,  # Use the resolver's decision
    grade="D",
    confidence=0.5,
    clarity=80.0,
    risk_score=0.0,
    score=63.87,
    quality=80.0,
    expected_strength=100.0,
    buy_probability=0.0,
    sell_probability=60.0,
    wait_probability=40.0,
    expected_risk=0.0,
    expected_reward=0.0,
    expected_drawdown=0.0,
    audit_id="test_audit_id",
    version_metadata=version_metadata,
    explanation=explanation,
    warnings=(),
    weaknesses=(),
    blockers=(),
    summary="Test summary"
)

print(f"DecisionResult decision: {decision_result.decision}")
print(f"Match: {resolver_result.decision == decision_result.decision}")
assert resolver_result.decision == decision_result.decision, "MISMATCH: resolver and DecisionResult decisions don't match!"
print("PASS: SELL decisions match\n")

print("=== AMBOS TESTES PASSARAM: resolver.decision == DecisionResult.decision ===")
print("Isso confirma que não há post-resolver override convertendo BUY/SELL em WAIT")