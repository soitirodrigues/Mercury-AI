"""Top-3 selector M5 — SIGNAL-ONLY (filtra, nunca pontua).

Regras absolutas:
- NUNCA recalcula score, confluencia, risco ou ranking base.
- Consome exclusivamente ScanReport.to_dict() (top3 + ranked, ordem preservada).
- Emite 0..3 sinais: nunca completa com sintetico.
- Gate: decision BUY/SELL + entry_timing_state VALID + risk_reward>=2.0 + score>=70
  + forward_state CONFIRMED (F7: sem continuação p/ a próxima vela = sem Top-3).
- Dedup por simbolo (maior score vence).
- Ordena: (score, confidence, confluence, risk_reward) desc.
- EXPIRED / WAIT / SKIPPED / ERROR jamais entram.
"""
from __future__ import annotations

from typing import Any, Dict, List


MIN_SCORE = 70.0
MIN_RR = 2.0
VALID_STATE = "VALID"
FORWARD_OK = "CONFIRMED"


def _sig(entry: Dict[str, Any]) -> Dict[str, Any]:
    s = entry.get("signal")
    return s if isinstance(s, dict) else {}


def _is_eligible(entry: Dict[str, Any]) -> bool:
    if not isinstance(entry, dict):
        return False
    if entry.get("outcome", "RANKED") not in ("RANKED", None) and "signal" not in entry:
        # per_asset rows: so RANKED elegivel
        if entry.get("outcome") != "RANKED":
            return False
    dec = entry.get("decision") or _sig(entry).get("decision") or _sig(entry).get("action")
    if dec not in ("BUY", "SELL"):
        return False
    sig = _sig(entry)
    if sig.get("entry_timing_state", VALID_STATE) != VALID_STATE:
        return False
    # CORREÇÃO F7 (falso positivo): forward-bias CONFIRMED obrigatório.
    # Sinal cuja direção não sobrevive até a próxima vela (WEAK/EXPIRED)
    # nunca entra no Top-3 — operador Hezilex só vê continuação real.
    if str(sig.get("forward_state", FORWARD_OK)).upper() != FORWARD_OK:
        return False
    try:
        rr = float(sig.get("risk_reward", 0) or 0)
    except (TypeError, ValueError):
        rr = 0.0
    if rr < MIN_RR:
        return False
    try:
        score = float(entry.get("score", sig.get("score", 0)) or 0)
    except (TypeError, ValueError):
        score = 0.0
    if score < MIN_SCORE:
        return False
    sym = entry.get("symbol") or sig.get("symbol") or sig.get("asset")
    if not sym:
        return False
    return True


def _sort_key(entry: Dict[str, Any]):
    sig = _sig(entry)
    def _f(v, d=0.0):
        try:
            return float(v if v is not None else d)
        except (TypeError, ValueError):
            return d
    score = _f(entry.get("score", sig.get("score")))
    conf = _f(entry.get("confidence", sig.get("confidence")))
    confl = _f(sig.get("confluence"))
    rr = _f(sig.get("risk_reward"))
    return (score, conf, confl, rr)


def select_top3(scan_report: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Filtra Top-3 elegivel de ScanReport dict. Retorna 0..3 dicts (verbatim)."""
    if not isinstance(scan_report, dict):
        return []
    pool = list(scan_report.get("top3", []) or []) + list(scan_report.get("ranked", []) or [])
    best: Dict[str, Dict[str, Any]] = {}
    for entry in pool:
        if not _is_eligible(entry):
            continue
        sig = _sig(entry)
        sym = entry.get("symbol") or sig.get("symbol") or sig.get("asset")
        prev = best.get(sym)
        if prev is None or _sort_key(entry) > _sort_key(prev):
            best[sym] = entry
    ranked = sorted(best.values(), key=_sort_key, reverse=True)
    return ranked[:3]


def setup_label(entry: Dict[str, Any]) -> str:
    """Rotulo de confluencia para o card (propagacao de evidencias reais)."""
    sig = _sig(entry)
    evs = sig.get("evidences") or entry.get("evidences") or []
    parts = []
    mtf = sig.get("mtf_summary") or {}
    if isinstance(mtf, dict) and mtf.get("status") == "present":
        parts.append("H1/M5 Alignment" if float(mtf.get("alignment_score", 0) or 0) >= 60 else "MTF")
    for e in list(evs)[:3]:
        s = str(e)
        if "sweep" in s.lower() or "liquidity" in s.lower():
            parts.append("Sweep")
        elif "fvg" in s.lower():
            parts.append("FVG")
        elif "order block" in s.lower() or "ob " in s.lower():
            parts.append("OB")
        elif "choch" in s.lower() or "bos" in s.lower() or "msb" in s.lower():
            parts.append("CHoCH/BOS")
    seen, uniq = set(), []
    for p in parts:
        if p not in seen:
            seen.add(p)
            uniq.append(p)
    return " + ".join(uniq) if uniq else "Confluence"
