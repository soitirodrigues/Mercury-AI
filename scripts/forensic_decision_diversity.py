#!/usr/bin/env python3
"""Provas determinísticas de diversidade de decisão sem depender de mercado real."""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.market_data import MarketData
from mercury_ai.models.risk_assessment import RiskAssessment
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle
from mercury_ai.models.evidence import Evidence
from mercury_ai.config.timeframes import DEFAULT_TIMEFRAME

resolver = DecisionResolverEngine()

def mk_ctx(risk=20.0):
    # Minimal placeholders that satisfy ProbabilityEngine (needs risk_assessment.institutional_risk_score)
    class Fake:
        pass
    # Use real objects where needed; otherwise stub with attribute fallback
    # Build minimal MarketContext via bypassing dataclass validation by using object.__new__
    ctx = MarketContext.__new__(MarketContext)
    object.__setattr__(ctx, 'market', MarketData(symbol="MOCK", timeframe=DEFAULT_TIMEFRAME, close=100, ema9=99, ema21=98, ema50=97, rsi=50, atr=1, adx=20, macd=0, macd_signal=0, bollinger_upper=101, bollinger_lower=99, volume=1000))
    object.__setattr__(ctx, 'trend', ())
    object.__setattr__(ctx, 'price_action', None)
    object.__setattr__(ctx, 'support_resistance', None)
    object.__setattr__(ctx, 'smart_money', None)
    object.__setattr__(ctx, 'liquidity', None)
    object.__setattr__(ctx, 'market_state', None)
    object.__setattr__(ctx, 'market_regime', None)
    object.__setattr__(ctx, 'mtf_consensus', None)
    object.__setattr__(ctx, 'risk_assessment', RiskAssessment(suggested_stop=99, suggested_take_profit=101, risk_reward_ratio=2, expected_drawdown=1, expected_volatility=0.01, trade_quality=50, max_exposure=0.02, invalidation_point=99, institutional_risk_score=risk))
    return ctx

def bundle(direction, n=5):
    evs=[]
    for i in range(n):
        evs.append(Evidence.create(engine_name=f"E{i}", evidence_name=f"ev{i}", direction=direction, strength=80, confidence=80, description="mock", weight=10))
    return MarketEvidenceBundle(evidences=tuple(evs), timestamp="2026-01-01T00:00:00", asset="MOCK", timeframe=DEFAULT_TIMEFRAME)

def assert_case(desc, dominant, is_valid, grade, conflict, confl, expected):
    res = resolver.resolve(dominant_direction=dominant, is_valid=is_valid, opportunity_grade=grade, conflicting_signals=conflict, confluence_score=confl)
    ok = res.decision == expected
    print(f"{'PASS' if ok else 'FAIL'} {desc}: got {res.decision} rule {res.triggered_rule} expected {expected}  (dom={dominant} valid={is_valid} grade={grade} conflict={conflict} confl={confl})")
    assert ok, f"{desc} expected {expected} got {res.decision}"

# BUY / SELL / WAIT deterministic
assert_case("BUY determinístico", "BUY", True, "B", False, 80.0, "BUY")
assert_case("SELL determinístico", "SELL", True, "B", False, 80.0, "SELL")
assert_case("WAIT por invalid", "BUY", False, "A", False, 80.0, "WAIT")
assert_case("WAIT por baixa confluência", "BUY", True, "A", False, 10.0, "WAIT")
assert_case("WAIT por conflito+grade D", "BUY", True, "D", True, 80.0, "WAIT")
assert_case("WAIT por conflito+grade C", "SELL", True, "C", True, 80.0, "WAIT")
assert_case("BUY com conflito mas grade B (passa)", "BUY", True, "B", True, 80.0, "BUY")
assert_case("WAIT por NEUTRAL", "NEUTRAL", True, "A", False, 80.0, "WAIT")

# Grade boundaries already proven; test probability diversity
prob = ProbabilityEngine()
for dir_val, exp_buy, exp_sell in [("BUY", ">40", "0"), ("SELL", "0", ">40"), ("NEUTRAL", ">20", ">20")]:
    ctx = mk_ctx(risk=0.0)
    b = bundle(dir_val if dir_val!="NEUTRAL" else "NEUTRAL", n=5)
    # confluence 80, confidence 80, director known
    res = prob.analyze(ctx, b, confluence_score=80, confidence_score=80, dominant_direction=dir_val)
    print(f"PROB {dir_val}: buy {res.buy_probability} sell {res.sell_probability} wait {res.neutral_probability} grade {res.opportunity_grade} sum {res.buy_probability+res.sell_probability+res.neutral_probability:.2f}")
    assert 99.9 <= res.buy_probability+res.sell_probability+res.neutral_probability <=100.1
    if dir_val=="BUY": assert res.buy_probability>40 and res.sell_probability==0
    if dir_val=="SELL": assert res.sell_probability>40 and res.buy_probability==0
    if dir_val=="NEUTRAL": assert res.buy_probability==res.sell_probability and res.buy_probability>15

print("DECISION DIVERSITY ALL PASS")
