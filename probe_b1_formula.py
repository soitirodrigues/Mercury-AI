"""
Probe de validacao da FORMULA CANONICA do ProbabilityEngine (Bloco B1).
Cenarios A-F: prova matematica dos coeficientes 0.50/0.35/0.15.

Uso: python probe_b1_formula.py
"""
from unittest.mock import MagicMock
from mercury_ai.brain.probability_engine import ProbabilityEngine
from mercury_ai.models.market_context import MarketContext
from mercury_ai.models.evidence import Evidence
from mercury_ai.models.market_evidence_bundle import MarketEvidenceBundle


def make_context(risk: float):
    ctx = MagicMock(spec=MarketContext)
    ctx.risk_assessment = MagicMock()
    ctx.risk_assessment.institutional_risk_score = risk
    return ctx


def make_bundle(n_evidences: int):
    evs = [
        Evidence(
            "TrendAnalyzer", "Trend", "BULLISH", 80.0, 90.0,
            "Desc", 1.0, contribution_score=80.0,
        )
        for _ in range(n_evidences)
    ]
    return MarketEvidenceBundle(
        evidences=tuple(evs), timestamp="now",
        asset="EURUSD", timeframe="1H",
    )


def expected_strength(confluence, confidence, n_ev, risk):
    """Formula canonica restaurada."""
    ev_bonus = min(n_ev * 4.0, 20.0)
    strength = confluence * 0.50 + confidence * 0.35 + ev_bonus * 0.15
    strength *= (1.0 - (risk / 100.0) * 0.50)
    return max(0.0, min(strength, 100.0))


def grade_of(strength):
    if strength >= 80:
        return "A+"
    if strength >= 70:
        return "A"
    if strength >= 60:
        return "B"
    if strength >= 50:
        return "C"
    return "D"


ENGINE = ProbabilityEngine(weights={
    "trend": 0.4, "structure": 0.3,
    "liquidity": 0.2, "volatility": 0.1,
})

SCENARIOS = [
    # (nome, confluence, confidence, n_ev, risk, direction)
    ("A - Forte",    100.0, 100.0, 6, 0.0, "BUY"),
    ("B - Bom",      90.0,  80.0,  4, 0.0, "BUY"),
    ("C - Medio",    60.0,  60.0,  3, 0.0, "BUY"),
    ("D - Fraco",    40.0,  40.0,  1, 0.0, "BUY"),
    ("E - RiscoAlto", 90.0,  80.0,  4, 50.0, "BUY"),
    ("F - Sell",     90.0,  80.0,  4, 0.0, "SELL"),
]

ok = True
print("=" * 100)
print("PROBE FORMULA CANONICA B1  (confluence*0.50 + confidence*0.35 + evidence*0.15)")
print("=" * 100)
for name, conf, confi, n_ev, risk, direction in SCENARIOS:
    res = ENGINE.analyze(
        make_context(risk), make_bundle(n_ev),
        confluence_score=conf, confidence_score=confi,
        dominant_direction=direction,
    )
    exp = expected_strength(conf, confi, n_ev, risk)
    exp_grade = grade_of(exp)

    # buy_probability = 100 - wait (para BUY/SELL direcionais)
    wait = max(5.0, min(max(5.0, 100.0 - exp), 60.0))
    exp_buy = (100.0 - wait) if direction in ("BUY", "BULLISH") else 0.0
    exp_sell = (100.0 - wait) if direction in ("SELL", "BEARISH") else 0.0

    match_grade = res.opportunity_grade == exp_grade
    match_buy = abs(res.buy_probability - round(exp_buy, 2)) < 0.01
    match_sell = abs(res.sell_probability - round(exp_sell, 2)) < 0.01

    scenario_ok = match_grade and match_buy and match_sell
    ok = ok and scenario_ok

    print(f"[{name}] confluence={conf:.0f} confidence={confi:.0f} "
          f"n_ev={n_ev} risk={risk} dir={direction}")
    print(f"   esperado: strength={exp:.2f} grade={exp_grade} "
          f"buy={exp_buy:.2f} sell={exp_sell:.2f}")
    print(f"   obtido  : grade={res.opportunity_grade} "
          f"buy={res.buy_probability} sell={res.sell_probability} "
          f"wait={res.neutral_probability}")
    print(f"   match: grade={match_grade} buy={match_buy} sell={match_sell} "
          f"=> {'OK' if scenario_ok else 'FALHOU'}")

# Prova do desbloqueio do B1: com forca institucional > 50, grade != D
print("-" * 100)
print("PROVA DO DESBLOQUEIO: institutional_strength maximo alcançavel agora")
max_ev = make_bundle(6)  # evidence_bonus = 20
res_max = ENGINE.analyze(
    make_context(0.0), max_ev,
    confluence_score=100.0, confidence_score=100.0,
    dominant_direction="BUY",
)
print(f"   Maximo (confluence=100, conf=100, ev=20, risk=0): "
      f"buy={res_max.buy_probability} grade={res_max.opportunity_grade}")
# BTC auditado: confluence=100, confidence=69.49, evidence=20
res_btc = ENGINE.analyze(
    make_context(0.0), make_bundle(6),
    confluence_score=100.0, confidence_score=69.49,
    dominant_direction="BUY",
)
print(f"   BTC auditado (conf=100, confi=69.49, ev=20): "
      f"buy={res_btc.buy_probability} grade={res_btc.opportunity_grade}")

print("-" * 100)
print(f"RESULTADO: {'TODOS OS CENARIOS OK' if ok else 'HA FALHAS'}")
print("=" * 100)
