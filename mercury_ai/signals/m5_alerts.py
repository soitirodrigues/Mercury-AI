"""M5 alert window — janela habil 3m50s~4m05s (pura, sem rede).

Regra: elapsed = 300 - seconds_to_next_m5.
EMITIR pre-alerta sse 230 <= elapsed <= 245  =>  lead 55..70s ate next_m5_ts.
Entrada sugerida = next_m5_ts (market-on-open da proxima vela).
Sem wall-clock para definir fronteira (fronteira vem de m5_timing).
"""
from __future__ import annotations

from typing import Any, Dict, Optional

CYCLE_S = 300.0
ALERT_MIN_ELAPSED = 230.0
ALERT_MAX_ELAPSED = 245.0


def alert_state(seconds_to_next_m5: Optional[float]) -> Dict[str, Any]:
    """Estado da janela de alerta a partir de seconds_to_next_m5."""
    if seconds_to_next_m5 is None:
        return {"in_window": False, "elapsed_s": None, "lead_s": None, "state": "UNKNOWN"}
    try:
        s = float(seconds_to_next_m5)
    except (TypeError, ValueError):
        return {"in_window": False, "elapsed_s": None, "lead_s": None, "state": "UNKNOWN"}
    elapsed = CYCLE_S - s
    in_window = ALERT_MIN_ELAPSED <= elapsed <= ALERT_MAX_ELAPSED and s > 0
    return {
        "in_window": bool(in_window),
        "elapsed_s": round(elapsed, 1),
        "lead_s": round(s, 1) if s > 0 else 0.0,
        "state": "EMIT" if in_window else ("WAIT" if s > 0 else "EXPIRED"),
    }
