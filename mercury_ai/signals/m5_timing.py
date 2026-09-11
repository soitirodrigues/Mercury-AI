"""S33-E.6 — Matematica temporal M5 (pura, stdlib-only, SIGNAL-ONLY).

ENTRY WINDOW RULE (deterministica, documentada aqui e so aqui):

    last_m5_ts -> next_m5_ts = strict ceil para a proxima fronteira de
                5 minutos em UTC. Se last_m5_ts ja estiver exatamente sobre
                uma fronteira, next = +5min.
                Exemplo: 10:14:xx -> 10:15:00 ; 10:10:00 -> 10:15:00.
    signal_ts  -> timestamp de emissao da decisao/sinal. Quando o timestamp
                da ultima vela conhecida existe, ele e a unica fonte para
                next_m5_ts — NUNCA o relogio da maquina.
    seconds_to_next_m5 = (next_m5_ts - signal_ts) em segundos (pode ser <= 0).
    VALID   sse signal_ts < next_m5_ts -> janela [signal_ts, next_m5_ts),
                                          entry_window_seconds = seconds_to_next_m5 (> 0).
    EXPIRED sse signal_ts >= next_m5_ts -> janela 0, estado explicito
                                          "EXPIRED" (protecao contra falso timing).

Sem rede, sem broker, sem ordens. Nao toca engines, pesos ou thresholds.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Optional, Union

M5_MINUTES = 5
VALID_STATE = "VALID"
EXPIRED_STATE = "EXPIRED"

TimestampLike = Union[str, datetime]


def parse_utc(value: TimestampLike | None) -> Optional[datetime]:
    """Parseia str ISO-8601 ou datetime para aware-UTC. Naive assume UTC."""
    if value is None:
        return None
    if isinstance(value, datetime):
        dt = value
    elif isinstance(value, str):
        text = value.strip()
        if not text:
            return None
        if text.endswith(("Z", "z")):
            text = text[:-1] + "+00:00"
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return None
    else:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def to_iso_utc(dt: datetime) -> str:
    """Serializa datetime como ISO-8601 aware-UTC."""
    return parse_utc(dt).isoformat()


def floor_m5(dt: TimestampLike) -> datetime:
    """Trunca para a fronteira M5 anterior (inclusive). Ex: 10:07:23 -> 10:05:00."""
    parsed = parse_utc(dt)
    if parsed is None:
        raise ValueError(f"timestamp M5 invalido: {dt!r}")
    minute = (parsed.minute // M5_MINUTES) * M5_MINUTES
    return parsed.replace(minute=minute, second=0, microsecond=0)


def compute_next_m5(last_m5_ts: TimestampLike | None) -> Optional[str]:
    """Proxima fronteira M5 estritamente apos last_m5_ts (ISO aware-UTC).

    Retorna None quando last_m5_ts e desconhecido — o chamador deve marcar
    o sinal como EXPIRED em vez de inferir pelo relogio da maquina.
    """
    parsed = parse_utc(last_m5_ts)
    if parsed is None:
        return None
    return to_iso_utc(floor_m5(parsed) + timedelta(minutes=M5_MINUTES))


def compute_entry_window(
    signal_ts: TimestampLike | None,
    next_m5_ts: TimestampLike | None,
) -> dict:
    """Janela operacional [signal_ts, next_m5_ts) + estado VALID/EXPIRED."""
    sig = parse_utc(signal_ts)
    nxt = parse_utc(next_m5_ts)
    if sig is None or nxt is None:
        return {
            "start": to_iso_utc(sig) if sig is not None else None,
            "end": to_iso_utc(nxt) if nxt is not None else None,
            "seconds": 0.0,
            "seconds_to_next_m5": None,
            "valid": False,
            "state": EXPIRED_STATE,
        }
    delta = (nxt - sig).total_seconds()
    valid = delta > 0
    return {
        "start": to_iso_utc(sig),
        "end": to_iso_utc(nxt),
        "seconds": float(delta) if valid else 0.0,
        "seconds_to_next_m5": float(delta),
        "valid": valid,
        "state": VALID_STATE if valid else EXPIRED_STATE,
    }
