"""
Sistema unificado de classificação institucional de grades.

Escala padrão usada em toda a plataforma Mercury-AI:
    A+  >= 80
    A   >= 70
    B   >= 60
    C   >= 50
    D   <  50
"""

from __future__ import annotations


def calculate_grade(score: float) -> str:
    """
    Converte um score numérico (0-100) em grade institucional.

    Parameters
    ----------
    score : float
        Score entre 0 e 100.

    Returns
    -------
    str
        Uma das grades: "A+", "A", "B", "C", "D".
    """
    if score >= 80:
        return "A+"
    if score >= 70:
        return "A"
    if score >= 60:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def is_passing_grade(grade: str) -> bool:
    """Retorna True se o grade permite operação (C ou melhor)."""
    return grade in ("A+", "A", "B", "C")


def grade_to_numeric(grade: str) -> float:
    """Converte grade em valor numérico mínimo representativo."""
    mapping = {
        "A+": 80.0,
        "A": 70.0,
        "B": 60.0,
        "C": 50.0,
        "D": 0.0,
    }
    return mapping.get(grade, 0.0)
