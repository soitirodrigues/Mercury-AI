"""Sprint 6 — Definição formal de deadline M5 (Sprint 6 §3-§4, §8).

Define SEM AMBIGUIDADE:
  - ciclo M5 referenciado a target_candle
  - metricas decision_latency / deadline_margin
  - predicado PASS/FAIL next_candle_ready
  - agregacoes p50/p95/min/max

CONTRATO CANONICO (§3):
  CANDLE_N = target_candle (open da vela que acabou de fechar; floor M5 UTC)
  processamento usa dados ate / incluindo CANDLE_N
  resultado deve estar DECISION READY antes de CANDLE_{N+1}
    CANDLE_{N+1} = target_candle + 5min = next_candle_start

METRICAS (§4):
  target_candle_close = target_candle           (definicao Sprint 6: close = open da vela fechada)
  next_candle_start   = target_candle + 5min
  decision_ready_timestamp = primeira decisao FRESH do ciclo (cycle wall)
                           ou ciclo completo quando nao ha fresh (medido, mas nao qualificavel)
  decision_latency    = decision_ready - target_candle_close  (s)
  deadline_margin     = next_candle_start - decision_ready     (s)
  PASS  se deadline_margin > 0   (decision_ready < next_candle_start)
  FAIL  se deadline_margin <= 0  (perdeu janela operacional)

NÃO considerar simplesmente <300s suficiente — verificar candle N+1 real.

Nao duplica ranking/decisao.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Optional, List, Dict, Any
import statistics

from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5, _ensure_utc


M5_SECONDS = 300


def target_candle_close_for(target_candle: datetime) -> datetime:
    """Sprint 6 §4: target_candle_close = target_candle (open da vela fechada)."""
    return floor_m5(_ensure_utc(target_candle))


def next_candle_start_for(target_candle: datetime) -> datetime:
    return floor_m5(_ensure_utc(target_candle)) + timedelta(minutes=5)


def decision_latency_s(target_candle_close: datetime, decision_ready_ts: datetime) -> float:
    a = _ensure_utc(target_candle_close)
    b = _ensure_utc(decision_ready_ts)
    return (b - a).total_seconds()


def deadline_margin_s(next_candle_start: datetime, decision_ready_ts: datetime) -> float:
    a = _ensure_utc(next_candle_start)
    b = _ensure_utc(decision_ready_ts)
    return (a - b).total_seconds()


@dataclass(frozen=True)
class DeadlineResult:
    target_candle: datetime
    target_candle_close: datetime
    next_candle_start: datetime
    decision_ready: Optional[datetime]
    decision_latency_s: Optional[float]
    deadline_margin_s: Optional[float]
    next_candle_ready: Optional[bool]  # None = sem decisao fresh qualificavel
    reason: str


def evaluate_deadline(
    target_candle: datetime,
    decision_ready: Optional[datetime],
) -> DeadlineResult:
    """Avalia PASS/FAIL para um ciclo (Sprint 6 §8)."""
    tc = floor_m5(_ensure_utc(target_candle))
    tcc = target_candle_close_for(tc)
    ncs = next_candle_start_for(tc)
    if decision_ready is None:
        return DeadlineResult(
            target_candle=tc,
            target_candle_close=tcc,
            next_candle_start=ncs,
            decision_ready=None,
            decision_latency_s=None,
            deadline_margin_s=None,
            next_candle_ready=None,
            reason="sem decision_ready (nenhuma decisao fresh no ciclo) — nao qualificavel para next_candle_ready",
        )
    dr = _ensure_utc(decision_ready)
    dlat = decision_latency_s(tcc, dr)
    dmar = deadline_margin_s(ncs, dr)
    ok = dmar > 0
    return DeadlineResult(
        target_candle=tc,
        target_candle_close=tcc,
        next_candle_start=ncs,
        decision_ready=dr,
        decision_latency_s=dlat,
        deadline_margin_s=dmar,
        next_candle_ready=ok,
        reason=f"deadline_margin={dmar:.2f}s -> {'PASS' if ok else 'FAIL'}  (decision_latency={dlat:.2f}s)",
    )


def percentile(values: List[float], p: float) -> Optional[float]:
    if not values:
        return None
    s = sorted(values)
    # linear interpolation (numpy-like)
    k = (len(s) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(s) - 1)
    if f == c:
        return float(s[f])
    d0 = k - f
    return float(s[f] * (1 - d0) + s[c] * d0)


def aggregate_deadlines(results: List[DeadlineResult]) -> Dict[str, Any]:
    margins = [r.deadline_margin_s for r in results if r.deadline_margin_s is not None]
    latencies = [r.decision_latency_s for r in results if r.decision_latency_s is not None]
    passes = sum(1 for r in results if r.next_candle_ready is True)
    fails = sum(1 for r in results if r.next_candle_ready is False)
    nonqual = sum(1 for r in results if r.next_candle_ready is None)
    return {
        "cycles": len(results),
        "pass": passes,
        "fail": fails,
        "non_qualifying": nonqual,
        "pass_rate": (passes / (passes + fails)) if (passes + fails) else None,
        "deadline_margin_min": min(margins) if margins else None,
        "deadline_margin_max": max(margins) if margins else None,
        "deadline_margin_mean": (sum(margins) / len(margins)) if margins else None,
        "deadline_margin_p50": percentile(margins, 50) if margins else None,
        "deadline_margin_p95": percentile(margins, 95) if margins else None,
        "decision_latency_p50": percentile(latencies, 50) if latencies else None,
        "decision_latency_p95": percentile(latencies, 95) if latencies else None,
        "decision_latency_max": max(latencies) if latencies else None,
        "worst_margin": min(margins) if margins else None,
    }
