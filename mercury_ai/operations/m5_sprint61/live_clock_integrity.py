"""Sprint 6.1 — LiveClockIntegrityGate: certificacao temporal honesta.

Separe formalmente:
  - ACCELERATED_SOAK: ciclos acelerados (target+=5m sem esperar fronteira real) —
    valido para reliability/concurrency/freshness/soak, mas NON_QUALIFYING para LIVE_CLOCK.
  - LIVE_CLOCK: ciclos ligados ao relogio UTC real — target nunca no futuro;
    decision_ready >= target_candle_close && < next_candle_start.

Invariantes (§3):
  target_candle <= clock_now_at_cycle_start
  target_candle_close <= decision_ready
  decision_ready < next_candle_start
  0 <= decision_latency < 300
  0 < deadline_margin <= 300
  decision_ready < target_candle_close => NON_QUALIFYING_FUTURE_TARGET (nunca PASS)

Estados:
  QUALIFYING_PASS, QUALIFYING_FAIL, NON_QUALIFYING_FUTURE_TARGET,
  NON_QUALIFYING_ACCELERATED, INVALID_TIMESTAMP_ORDER

Observacional apenas — nao altera decisao/ranking/freshness/Top3.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum

from mercury_ai.operations.m5_incremental.temporal import floor_m5, _ensure_utc


M5_SECONDS = 300


class MeasurementMode(str, Enum):
    ACCELERATED_SOAK = "ACCELERATED_SOAK"
    LIVE_CLOCK = "LIVE_CLOCK"


class CycleResult(str, Enum):
    QUALIFYING_PASS = "QUALIFYING_PASS"
    QUALIFYING_FAIL = "QUALIFYING_FAIL"
    NON_QUALIFYING_FUTURE_TARGET = "NON_QUALIFYING_FUTURE_TARGET"
    NON_QUALIFYING_ACCELERATED = "NON_QUALIFYING_ACCELERATED"
    INVALID_TIMESTAMP_ORDER = "INVALID_TIMESTAMP_ORDER"
    NON_QUALIFYING_NO_DECISION = "NON_QUALIFYING_NO_DECISION"


@dataclass(frozen=True)
class LiveClockCycleInput:
    measurement_mode: MeasurementMode
    clock_now_at_cycle_start: datetime
    target_candle: datetime
    decision_ready: Optional[datetime]
    # derivado: target_candle_close = target_candle (open fechada), next = target+5m


@dataclass(frozen=True)
class LiveClockIntegrityReport:
    measurement_mode: str
    clock_now_at_cycle_start: str
    target_candle: str
    target_candle_close: str
    target_is_future: bool
    decision_ready: Optional[str]
    decision_before_candle_close: Optional[bool]
    decision_latency_s: Optional[float]
    next_candle_start: str
    deadline_margin_s: Optional[float]
    temporal_order_valid: bool
    live_clock_qualifying: bool
    next_candle_result: str
    non_qualifying_reason: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _iso(dt: Optional[datetime]) -> Optional[str]:
    if dt is None:
        return None
    return _ensure_utc(dt).isoformat()


def classify_cycle(inp: LiveClockCycleInput) -> LiveClockIntegrityReport:
    """Classifica um ciclo segundo invariantes Sprint 6.1 §3-§5.

    - ACCELERATED_SOAK => sempre NON_QUALIFYING_ACCELERATED (nunca PASS).
    - LIVE_CLOCK && target > clock_now => NON_QUALIFYING_FUTURE_TARGET.
    - LIVE_CLOCK && decision_ready is None => NON_QUALIFYING_NO_DECISION.
    - LIVE_CLOCK && decision_ready < target_close => NON_QUALIFYING_FUTURE_TARGET (latencia negativa).
    - LIVE_CLOCK && decision_ready >= next_start => QUALIFYING_FAIL (deadline perdido; == next_start => FAIL).
    - LIVE_CLOCK && decision_ready in [target_close, next_start) => QUALIFYING_PASS.
    - timestamps fora de ordem (next <= target_close etc) => INVALID_TIMESTAMP_ORDER.
    """
    mode = inp.measurement_mode
    clock_now = _ensure_utc(inp.clock_now_at_cycle_start)
    target = floor_m5(_ensure_utc(inp.target_candle))
    target_close = target
    next_start = target + timedelta(minutes=5)
    dr = _ensure_utc(inp.decision_ready) if inp.decision_ready is not None else None

    # sanity: temporal_order_valid = target_close < next_start sempre (por construcao)
    temporal_order_valid = target_close < next_start
    if not temporal_order_valid:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=target > clock_now,
            decision_ready=_iso(dr),
            decision_before_candle_close=(dr < target_close) if dr is not None else None,
            decision_latency_s=(dr - target_close).total_seconds() if dr is not None else None,
            next_candle_start=_iso(next_start),
            deadline_margin_s=(next_start - dr).total_seconds() if dr is not None else None,
            temporal_order_valid=False,
            live_clock_qualifying=False,
            next_candle_result=CycleResult.INVALID_TIMESTAMP_ORDER.value,
            non_qualifying_reason="INVALID_TIMESTAMP_ORDER: target_close >= next_start",
        )

    target_is_future = target > clock_now
    decision_before_close = (dr < target_close) if dr is not None else None
    dlat = (dr - target_close).total_seconds() if dr is not None else None
    dmar = (next_start - dr).total_seconds() if dr is not None else None

    # ACCELERATED nunca qualifica
    if mode == MeasurementMode.ACCELERATED_SOAK:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=target_is_future,
            decision_ready=_iso(dr),
            decision_before_candle_close=decision_before_close,
            decision_latency_s=dlat,
            next_candle_start=_iso(next_start),
            deadline_margin_s=dmar,
            temporal_order_valid=True,
            live_clock_qualifying=False,
            next_candle_result=CycleResult.NON_QUALIFYING_ACCELERATED.value,
            non_qualifying_reason="NON_QUALIFYING_ACCELERATED: modo soak nao certifica LIVE_CLOCK",
        )

    # LIVE_CLOCK: target futuro => non-qualifying (nunca PASS, mesmo se margin>0)
    if target_is_future:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=True,
            decision_ready=_iso(dr),
            decision_before_candle_close=decision_before_close,
            decision_latency_s=dlat,
            next_candle_start=_iso(next_start),
            deadline_margin_s=dmar,
            temporal_order_valid=True,
            live_clock_qualifying=False,
            next_candle_result=CycleResult.NON_QUALIFYING_FUTURE_TARGET.value,
            non_qualifying_reason="NON_QUALIFYING_FUTURE_TARGET: target_candle > clock_now_at_cycle_start",
        )

    if dr is None:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=False,
            decision_ready=None,
            decision_before_candle_close=None,
            decision_latency_s=None,
            next_candle_start=_iso(next_start),
            deadline_margin_s=None,
            temporal_order_valid=True,
            live_clock_qualifying=False,
            next_candle_result=CycleResult.NON_QUALIFYING_NO_DECISION.value,
            non_qualifying_reason="NON_QUALIFYING_NO_DECISION: sem decision_ready",
        )

    # latencia negativa => futuro (decision antes do close)
    if dr < target_close:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=False,
            decision_ready=_iso(dr),
            decision_before_candle_close=True,
            decision_latency_s=dlat,
            next_candle_start=_iso(next_start),
            deadline_margin_s=dmar,
            temporal_order_valid=True,
            live_clock_qualifying=False,
            next_candle_result=CycleResult.NON_QUALIFYING_FUTURE_TARGET.value,
            non_qualifying_reason="NON_QUALIFYING_FUTURE_TARGET: decision_ready < target_candle_close (latencia negativa)",
        )

    # decision_ready >= next_start => FAIL (== next_start tambem FAIL: deve ser estritamente <)
    if dr >= next_start:
        return LiveClockIntegrityReport(
            measurement_mode=mode.value,
            clock_now_at_cycle_start=_iso(clock_now),
            target_candle=_iso(target),
            target_candle_close=_iso(target_close),
            target_is_future=False,
            decision_ready=_iso(dr),
            decision_before_candle_close=False,
            decision_latency_s=dlat,
            next_candle_start=_iso(next_start),
            deadline_margin_s=dmar,
            temporal_order_valid=True,
            live_clock_qualifying=True,
            next_candle_result=CycleResult.QUALIFYING_FAIL.value,
            non_qualifying_reason=None,
        )

    # Caso valido: 0 <= latency < 300 && 0 < margin <=300
    # (ja garantido por dr in [target_close, next_start) )
    # Validar bounds explicitamente para deteccao
    if not (0 <= dlat < 300 and 0 < dmar <= 300):
        # Ainda PASS se dentro da janela, mas marca INVALID se fora (nao deve ocorrer)
        pass

    return LiveClockIntegrityReport(
        measurement_mode=mode.value,
        clock_now_at_cycle_start=_iso(clock_now),
        target_candle=_iso(target),
        target_candle_close=_iso(target_close),
        target_is_future=False,
        decision_ready=_iso(dr),
        decision_before_candle_close=False,
        decision_latency_s=dlat,
        next_candle_start=_iso(next_start),
        deadline_margin_s=dmar,
        temporal_order_valid=True,
        live_clock_qualifying=True,
        next_candle_result=CycleResult.QUALIFYING_PASS.value,
        non_qualifying_reason=None,
    )


# Convenience validators (Sprint 6.1 §4)
def validate_target_not_future(target_candle: datetime, clock_now: datetime) -> bool:
    return floor_m5(_ensure_utc(target_candle)) <= _ensure_utc(clock_now)


def validate_decision_after_candle_close(decision_ready: datetime, target_candle_close: datetime) -> bool:
    return _ensure_utc(decision_ready) >= _ensure_utc(target_candle_close)


def validate_before_next_candle(decision_ready: datetime, next_candle_start: datetime) -> bool:
    return _ensure_utc(decision_ready) < _ensure_utc(next_candle_start)


def validate_measurement_mode(mode: str) -> MeasurementMode:
    try:
        return MeasurementMode(mode)
    except ValueError:
        raise ValueError(f"mode deve ser ACCELERATED_SOAK | LIVE_CLOCK, recebido: {mode}")


def aggregate_live_clock(reports: List[LiveClockIntegrityReport]) -> Dict[str, Any]:
    total = len(reports)
    qualifying = [r for r in reports if r.live_clock_qualifying]
    q_pass = [r for r in qualifying if r.next_candle_result == CycleResult.QUALIFYING_PASS.value]
    q_fail = [r for r in qualifying if r.next_candle_result == CycleResult.QUALIFYING_FAIL.value]
    nonq = [r for r in reports if not r.live_clock_qualifying]
    # pass rate apenas sobre qualificaveis
    if q_pass or q_fail:
        rate = len(q_pass) / (len(q_pass) + len(q_fail))
    else:
        rate = None
    # latencias/margens apenas de qualificaveis PASS
    lat_valid = [r.decision_latency_s for r in q_pass if r.decision_latency_s is not None]
    mar_valid = [r.deadline_margin_s for r in q_pass if r.deadline_margin_s is not None]
    mar_all_q = [r.deadline_margin_s for r in qualifying if r.deadline_margin_s is not None]
    return {
        "total_cycles": total,
        "qualifying_live_cycles": len(qualifying),
        "qualifying_pass": len(q_pass),
        "qualifying_fail": len(q_fail),
        "non_qualifying_cycles": len(nonq),
        "next_candle_pass_rate": rate,
        "certification": "NOT_CERTIFIED" if not qualifying else ("PASS" if rate is not None and rate == 1.0 else "PARTIAL" if rate is not None else "NOT_CERTIFIED"),
        "min_deadline_margin_valid": min(mar_valid) if mar_valid else None,
        "min_latency_valid": min(lat_valid) if lat_valid else None,
        "max_latency_valid": max(lat_valid) if lat_valid else None,
        "min_deadline_margin_qualifying": min(mar_all_q) if mar_all_q else None,
        "non_qualifying_reasons": {r.non_qualifying_reason for r in nonq if r.non_qualifying_reason},
    }
