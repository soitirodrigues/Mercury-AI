"""Ranking Top-3 — fórmula canônica única (Single Source of Truth).

Extraída de scripts/top3_scanner.py para reuso sem duplicação.
NÃO alterar pesos/fórmula sem revisão institucional.

Fórmula:
  ranking_score = confluence_weighted (0-100)
                + confidence_100 * 0.30
                + grade_bonus (A+25 / A20 / B15 / C10 / D5)
                + dominant_prob * 0.20
  tie-breaker: internal_symbol ASC, audit_id ASC
  eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL)
               AND trade_allowed==true AND prob_sum_ok==true
               AND confidence not None AND confluence not None
"""
from __future__ import annotations

from typing import List, Tuple, Dict, Any

GRADE_BONUS: Dict[str, float] = {"A+": 25, "A": 20, "B": 15, "C": 10, "D": 5, "N/A": 0, None: 0}  # type: ignore
FORMULA = (
    "ranking_score = confluence_weighted (0-100) + confidence_100*0.30 + "
    "grade_bonus(A+25/A20/B15/C10/D5) + dominant_prob*0.20 ; "
    "tie-breaker: internal_symbol ASC, audit_id ASC. "
    "Eligibility: status==REAL_SIGNAL AND decision in (BUY,SELL) AND "
    "trade_allowed==true AND prob_sum_ok==true AND confidence not None AND confluence not None"
)


def _confidence_100(record: Dict[str, Any]) -> float:
    c = record.get("confidence")
    if c is None:
        return 0.0
    # confidence stored 0-1 in DecisionResult, 0-100 in some legacy scans
    if 0 < float(c) <= 1.1:
        return float(c) * 100
    return float(c)


def _prob_dominant(record: Dict[str, Any]) -> float:
    dec = str(record.get("decision") or "").upper()
    if dec == "BUY":
        return float(record.get("buy_probability") or 0)
    if dec == "SELL":
        return float(record.get("sell_probability") or 0)
    return 0.0


def _grade_bonus(grade: Any) -> float:
    if grade is None:
        return 0
    g = str(grade).strip().upper()
    # handle "N/A " etc
    return GRADE_BONUS.get(g, GRADE_BONUS.get(grade, 0))  # try raw then upper


def is_eligible(record: Dict[str, Any]) -> bool:
    if record.get("status") != "REAL_SIGNAL":
        return False
    if record.get("decision") not in ("BUY", "SELL"):
        return False
    if not record.get("trade_allowed"):
        return False
    if not record.get("prob_sum_ok"):
        return False
    if record.get("confidence") is None:
        return False
    if record.get("confluence") is None:
        return False
    return True


def compute_score(record: Dict[str, Any]) -> float:
    confl = float(record.get("confluence") or 0)
    c100 = _confidence_100(record)
    gbon = _grade_bonus(record.get("grade"))
    pdom = _prob_dominant(record)
    return confl + c100 * 0.30 + gbon + pdom * 0.20


def rank_records(records: List[Dict[str, Any]]) -> List[Tuple[float, Dict[str, Any]]]:
    """Filtra elegíveis, computa score, ordena deterministicamente."""
    eligible: List[Tuple[float, Dict[str, Any]]] = []
    for r in records:
        if not is_eligible(r):
            continue
        score = compute_score(r)
        eligible.append((score, r))
    eligible.sort(key=lambda x: (-x[0], x[1].get("internal_symbol", ""), x[1].get("audit_id", "")))
    return eligible


def select_top3(records: List[Dict[str, Any]], n: int = 3) -> Tuple[List[Tuple[float, Dict[str, Any]]], List[Tuple[float, Dict[str, Any]]]]:
    """Retorna (top_n, all_ranked)."""
    ranked = rank_records(records)
    return ranked[:n], ranked


# Helpers for status classification (also canonical)
def classify_status(decision_str: Any, audit_id: Any) -> str:
    audit = str(audit_id) if audit_id is not None else ""
    dec = str(decision_str or "").upper()
    is_hash = len(audit) == 64 and all(c in "0123456789abcdefABCDEF" for c in audit)
    if audit == "DATA_PROVIDER_UNAVAILABLE":
        return "DATA_UNAVAILABLE"
    if audit == "PIPELINE_ERROR":
        return "SCAN_ERROR"
    if audit in ("DATA_QUALITY_FAIL", "INSUFFICIENT_DATA", "MARKET_CLOSED"):
        return "DATA_UNAVAILABLE"
    if dec in ("BUY", "SELL") and is_hash:
        return "REAL_SIGNAL"
    if dec == "WAIT" and is_hash:
        return "WAIT_LEGITIMATE"
    if dec == "WAIT":
        return "WAIT_LEGITIMATE" if audit not in ("DATA_PROVIDER_UNAVAILABLE", "PIPELINE_ERROR", "DATA_QUALITY_FAIL", "INSUFFICIENT_DATA", "MARKET_CLOSED") else "DATA_UNAVAILABLE"
    return "ERROR"


def confidence_100_public(record: Dict[str, Any]) -> float:
    return _confidence_100(record)


def prob_dominant_public(record: Dict[str, Any]) -> float:
    return _prob_dominant(record)
