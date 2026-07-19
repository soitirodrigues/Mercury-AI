"""
SPRINT 1.7 — BLOCO 7/8: Decision Scenario Validation
Testa os 8 cenários obrigatórios diretamente contra o DecisionResolverEngine.

NÃO modifica código de produção.
Apenas testa o comportamento do resolver com entradas controladas.
"""

import sys
import os
import traceback

# Garante que o projeto está no path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mercury_ai.analysis.decision_resolver_engine import (
    DecisionResolverEngine,
    DecisionResolverResult,
)


# ============================================================
# DEFINIÇÃO DOS 8 CENÁRIOS
# ============================================================
# Cada cenário: (nome, dominant_direction, is_valid, opportunity_grade,
#                conflicting_signals, expected_decision, expected_rule,
#                expected_confidence_override)

SCENARIOS = [
    # 1. BUY FORTE
    {
        "id": 1,
        "name": "BUY FORTE",
        "dominant_direction": "BUY",
        "is_valid": True,
        "opportunity_grade": "B",
        "conflicting_signals": False,
        "expected_decision": "BUY",
        "expected_rule": 5,
        "expected_confidence_override": None,
    },
    # 2. BUY FRACO
    {
        "id": 2,
        "name": "BUY FRACO",
        "dominant_direction": "BUY",
        "is_valid": True,
        "opportunity_grade": "D",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 3,
        "expected_confidence_override": None,
    },
    # 3. SELL FORTE
    {
        "id": 3,
        "name": "SELL FORTE",
        "dominant_direction": "SELL",
        "is_valid": True,
        "opportunity_grade": "B",
        "conflicting_signals": False,
        "expected_decision": "SELL",
        "expected_rule": 6,
        "expected_confidence_override": None,
    },
    # 4. SELL FRACO
    {
        "id": 4,
        "name": "SELL FRACO",
        "dominant_direction": "SELL",
        "is_valid": True,
        "opportunity_grade": "D",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 3,
        "expected_confidence_override": None,
    },
    # 5. NEUTRAL
    {
        "id": 5,
        "name": "NEUTRAL",
        "dominant_direction": "NEUTRAL",
        "is_valid": True,
        "opportunity_grade": "B",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 2,
        "expected_confidence_override": None,
    },
    # 6. CONFLITO (BUY + grade C + conflicting_signals)
    {
        "id": 6,
        "name": "CONFLITO (BUY, grade C, conflict)",
        "dominant_direction": "BUY",
        "is_valid": True,
        "opportunity_grade": "C",
        "conflicting_signals": True,
        "expected_decision": "WAIT",
        "expected_rule": 4,
        "expected_confidence_override": None,
    },
    # 6b. CONFLITO (SELL + grade D + conflicting_signals)
    {
        "id": 7,
        "name": "CONFLITO (SELL, grade D, conflict)",
        "dominant_direction": "SELL",
        "is_valid": True,
        "opportunity_grade": "D",
        "conflicting_signals": True,
        "expected_decision": "WAIT",
        "expected_rule": 3,  # Regra 3 (grade D) tem prioridade sobre regra 4
        "expected_confidence_override": None,
    },
    # 7. DADOS INVÁLIDOS
    {
        "id": 8,
        "name": "DADOS INVÁLIDOS",
        "dominant_direction": "BUY",
        "is_valid": False,
        "opportunity_grade": "A+",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 1,
        "expected_confidence_override": 0.0,
    },
    # 8. GRADE D (BUY + grade D, sem conflito)
    {
        "id": 9,
        "name": "GRADE D (BUY, grade D, sem conflito)",
        "dominant_direction": "BUY",
        "is_valid": True,
        "opportunity_grade": "D",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 3,
        "expected_confidence_override": None,
    },
    # 8b. GRADE D (SELL + grade D, sem conflito)
    {
        "id": 10,
        "name": "GRADE D (SELL, grade D, sem conflito)",
        "dominant_direction": "SELL",
        "is_valid": True,
        "opportunity_grade": "D",
        "conflicting_signals": False,
        "expected_decision": "WAIT",
        "expected_rule": 3,
        "expected_confidence_override": None,
    },
]


def run_all_scenarios():
    """Executa todos os cenários e retorna resultados."""
    engine = DecisionResolverEngine()
    results = []
    passed = 0
    failed = 0

    print("=" * 72)
    print("  SPRINT 1.7 — BLOCO 7/8: DECISION SCENARIO VALIDATION")
    print("=" * 72)
    print()

    for scenario in SCENARIOS:
        sid = scenario["id"]
        name = scenario["name"]
        direction = scenario["dominant_direction"]
        is_valid = scenario["is_valid"]
        grade = scenario["opportunity_grade"]
        conflict = scenario["conflicting_signals"]
        expected_decision = scenario["expected_decision"]
        expected_rule = scenario["expected_rule"]
        expected_override = scenario["expected_confidence_override"]

        try:
            result: DecisionResolverResult = engine.resolve(
                dominant_direction=direction,
                is_valid=is_valid,
                opportunity_grade=grade,
                conflicting_signals=conflict,
            )
        except Exception as e:
            print(f"  [{sid}] {name}")
            print(f"       EXCEPTION: {type(e).__name__}: {e}")
            print(f"       RESULT: FAIL")
            print()
            results.append({
                "scenario": scenario,
                "result": None,
                "exception": str(e),
                "passed": False,
            })
            failed += 1
            continue

        # Validações
        checks = []
        all_ok = True

        # Check decision
        if result.decision != expected_decision:
            checks.append(
                f"DECISION: esperado={expected_decision}, obtido={result.decision}"
            )
            all_ok = False

        # Check triggered_rule
        if result.triggered_rule != expected_rule:
            checks.append(
                f"TRIGGERED_RULE: esperado={expected_rule}, obtido={result.triggered_rule}"
            )
            all_ok = False

        # Check confidence_override
        if result.confidence_override != expected_override:
            checks.append(
                f"CONFIDENCE_OVERRIDE: esperado={expected_override}, obtido={result.confidence_override}"
            )
            all_ok = False

        # Check: se decision é WAIT e is_valid=False, confidence_override deve ser 0.0
        if not is_valid and result.confidence_override != 0.0:
            checks.append(
                f"REGRA 1: is_valid=False mas confidence_override={result.confidence_override} (deveria ser 0.0)"
            )
            all_ok = False

        # Check: se decision é BUY, triggered_rule deve ser 5
        if result.decision == "BUY" and result.triggered_rule != 5:
            checks.append(
                f"BUY com triggered_rule={result.triggered_rule} (deveria ser 5)"
            )
            all_ok = False

        # Check: se decision é SELL, triggered_rule deve ser 6
        if result.decision == "SELL" and result.triggered_rule != 6:
            checks.append(
                f"SELL com triggered_rule={result.triggered_rule} (deveria ser 6)"
            )
            all_ok = False

        # Check: se decision é WAIT, triggered_rule deve ser 1, 2, 3, 4 ou 7
        if result.decision == "WAIT" and result.triggered_rule not in (1, 2, 3, 4, 7):
            checks.append(
                f"WAIT com triggered_rule={result.triggered_rule} (deveria ser 1,2,3,4 ou 7)"
            )
            all_ok = False

        status_str = "PASS" if all_ok else "FAIL"
        if all_ok:
            passed += 1
        else:
            failed += 1

        print(f"  [{sid}] {name}")
        print(f"    Input:  direction={direction}, is_valid={is_valid}, "
              f"grade={grade}, conflict={conflict}")
        print(f"    Output: decision={result.decision}, "
              f"triggered_rule={result.triggered_rule}, "
              f"confidence_override={result.confidence_override}")
        if checks:
            for c in checks:
                print(f"    ❌ {c}")
        print(f"    Result: {status_str}")
        print()

        results.append({
            "scenario": scenario,
            "result": result,
            "checks": checks,
            "passed": all_ok,
        })

    return results, passed, failed


def validate_consistency(results):
    """Valida consistência entre decisão e regras do Modelo C."""
    print("-" * 72)
    print("  CONSISTENCY VALIDATION (Modelo C)")
    print("-" * 72)
    print()

    consistency_checks = []
    all_consistent = True

    for r in results:
        if "exception" in r:
            continue
        scenario = r["scenario"]
        result = r["result"]

        # 1. dominant_direction vs decision
        # Se direction=NEUTRAL, decision deve ser WAIT
        if scenario["dominant_direction"] == "NEUTRAL" and result.decision != "WAIT":
            consistency_checks.append(
                f"[{scenario['id']}] NEUTRAL produziu decision={result.decision}"
            )
            all_consistent = False

        # 2. opportunity_grade vs decision
        # Se grade=D, decision deve ser WAIT
        if scenario["opportunity_grade"] == "D" and result.decision not in ("WAIT",):
            consistency_checks.append(
                f"[{scenario['id']}] grade=D produziu decision={result.decision}"
            )
            all_consistent = False

        # 3. conflicting_signals vs decision
        # Se conflict=True e grade in (C,D), decision deve ser WAIT
        if (scenario["conflicting_signals"]
                and scenario["opportunity_grade"] in ("C", "D")
                and result.decision not in ("WAIT",)):
            consistency_checks.append(
                f"[{scenario['id']}] conflict+grade C/D produziu decision={result.decision}"
            )
            all_consistent = False

        # 4. is_valid vs decision
        if not scenario["is_valid"] and result.decision != "WAIT":
            consistency_checks.append(
                f"[{scenario['id']}] is_valid=False produziu decision={result.decision}"
            )
            all_consistent = False

        # 5. triggered_rule vs decision
        if result.decision == "BUY" and result.triggered_rule != 5:
            consistency_checks.append(
                f"[{scenario['id']}] BUY com rule={result.triggered_rule}"
            )
            all_consistent = False
        if result.decision == "SELL" and result.triggered_rule != 6:
            consistency_checks.append(
                f"[{scenario['id']}] SELL com rule={result.triggered_rule}"
            )
            all_consistent = False

    if consistency_checks:
        for c in consistency_checks:
            print(f"  ❌ {c}")
    else:
        print("  ✅ Todas as verificações de consistência passaram.")
    print()

    return all_consistent


def main():
    print()
    results, passed, failed = run_all_scenarios()

    print("=" * 72)
    print("  SUMMARY")
    print("=" * 72)
    print(f"  Total scenarios tested: {len(SCENARIOS)}")
    print(f"  Passed:  {passed}")
    print(f"  Failed:  {failed}")
    print()

    consistent = validate_consistency(results)

    print("=" * 72)
    print("  VERDICT")
    print("=" * 72)

    if failed == 0 and consistent:
        print("  ✅ ALL SCENARIOS PASSED")
        print("  ✅ CONSISTENCY VALIDATION PASSED")
        print("  STATUS: BLOCO 7/8 UNIT TESTS — APROVADO")
        return 0
    else:
        if failed > 0:
            print(f"  ❌ {failed} SCENARIO(S) FAILED")
        if not consistent:
            print("  ❌ CONSISTENCY VALIDATION FAILED")
        print("  STATUS: BLOCO 7/8 UNIT TESTS — REPROVADO")
        return 1


if __name__ == "__main__":
    sys.exit(main())