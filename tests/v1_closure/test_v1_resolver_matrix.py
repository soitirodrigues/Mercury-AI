"""
MERCURY-AI V1 — RESOLVER CLOSURE MATRIX

Prova exclusivamente a matriz de decisão do resolver.
Não deve ser confundido com prova do pipeline completo.
"""

import pytest

from mercury_ai.analysis.decision_resolver_engine import DecisionResolverEngine


def make_resolver():
    return DecisionResolverEngine()


@pytest.mark.parametrize(
    "case,direction,grade,is_valid,conflict,confluence,expected",
    [
        (
            "A",
            "BUY",
            "D",
            True,
            False,
            80.0,
            "BUY",
        ),
        (
            "B",
            "SELL",
            "D",
            True,
            False,
            80.0,
            "SELL",
        ),
        (
            "C",
            "BUY",
            "C",
            True,
            True,
            80.0,
            "WAIT",
        ),
        (
            "D",
            "SELL",
            "C",
            True,
            True,
            80.0,
            "WAIT",
        ),
        (
            "E",
            "BUY",
            "A",
            False,
            False,
            80.0,
            "WAIT",
        ),
        (
            "F",
            "NEUTRAL",
            "A",
            True,
            False,
            80.0,
            "WAIT",
        ),
        (
            "G",
            "BUY",
            "A",
            True,
            False,
            20.0,
            "WAIT",
        ),
        (
            "H",
            "SELL",
            "A",
            True,
            False,
            20.0,
            "WAIT",
        ),
    ],
)
def test_v1_resolver_matrix(
    case,
    direction,
    grade,
    is_valid,
    conflict,
    confluence,
    expected,
):
    resolver = make_resolver()

    result = resolver.resolve(
        dominant_direction=direction,
        opportunity_grade=grade,
        is_valid=is_valid,
        conflicting_signals=conflict,
        confluence_score=confluence,
    )

    actual = getattr(
        result,
        "decision",
        getattr(result, "final_decision", None),
    )

    assert str(actual).upper() == expected, (
        f"CASE {case}: "
        f"expected={expected}, "
        f"actual={actual}, "
        f"result={result!r}"
    )