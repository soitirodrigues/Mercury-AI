"""Horario de entrada p/ Opportunity Dashboard (puro, sem rede, sem motores).

Regra: entrada = strict ceil M5 apos a referencia temporal, onde
referencia = last_m5_ts (vela fechada) > hora_do_sinal > fim_do_scan.
NUNCA usa wall-clock p/ definir fronteira; wall-clock so p/ countdown.

Reuso: mercury_ai.signals.m5_timing (strict ceil ja auditado).
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from mercury_ai.signals.m5_timing import compute_next_m5, parse_utc


def next_entry_utc(last_m5_ts: Any = None, signal_ts: Any = None,
                   scan_finished_ts: Any = None) -> Optional[str]:
    """Proxima vela M5 (ISO UTC). Prioridade: last_m5 > signal > scan_finished."""
    for cand in (last_m5_ts, signal_ts, scan_finished_ts):
        nxt = compute_next_m5(cand)
        if nxt:
            # Se referencia for signal/scan (intra-vela), ceil estrito da
            # propria referencia ja e a proxima fronteira. Como compute_next_m5
            # faz floor+5min, para signal 02:52:22 -> 02:55:00. Correto.
            return nxt
    return None


def format_br(iso_utc: Optional[str]) -> str:
    """'2026-09-13T02:55:00+00:00' -> '13/09 02:55:00 UTC' (nunca inventa)."""
    if not iso_utc:
        return "--"
    dt = parse_utc(iso_utc)
    if dt is None:
        return "--"
    return dt.strftime("%d/%m %H:%M:%S UTC")


def countdown_s(next_iso: Optional[str], now: Optional[datetime] = None) -> Optional[float]:
    """Segundos ate a entrada (p/ countdown). None se sem fronteira."""
    from datetime import timezone
    nxt = parse_utc(next_iso)
    if nxt is None:
        return None
    base = now or datetime.now(timezone.utc)
    return (nxt - base).total_seconds()


def enrich_top3_oportunidades(oportunidades: List[Dict[str, Any]],
                              scan_finished_ts: Any = None) -> List[Dict[str, Any]]:
    """Anexa entrada_sugerida a cada item do TOP 3 OPORTUNIDADES (verbatim + campo novo).

    Cada item pode ter: symbol, hora_do_sinal/signal_ts, last_m5_ts, signal{...}.
    Retorna copias rasas; nunca recalcula score/decisao.
    """
    out = []
    for op in oportunidades or []:
        sig = op.get("signal") if isinstance(op, dict) else None
        sig = sig if isinstance(sig, dict) else {}
        last = op.get("last_m5_ts", sig.get("last_m5_ts"))
        hsig = op.get("hora_do_sinal", op.get("signal_ts", sig.get("signal_ts")))
        nxt = next_entry_utc(last, hsig, scan_finished_ts)
        cp = dict(op)
        cp["entrada_sugerida_utc"] = nxt
        cp["entrada_sugerida_br"] = format_br(nxt)
        out.append(cp)
    return out
