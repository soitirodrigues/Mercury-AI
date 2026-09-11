"""Top-3 M5 API — FastAPI sidecar (transporte, sem inteligencia).

Roda ao lado do Streamlit (:8000):
  uvicorn mercury_ai.api.top3_api:app --port 8001
Ou monte no mesmo processo via --port 8000 se Streamlit for movido.

Contrato unico derivado de Signal.to_dict() + ScanReport.to_dict().
Nunca recalcula: le latest.json persistido por scan_service.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List

try:
    from fastapi import FastAPI, WebSocket
except ImportError:  # pragma: no cover
    FastAPI = None  # type: ignore
    WebSocket = None  # type: ignore

from mercury_ai.brain.scan_service import load_latest_scan_report
from mercury_ai.signals.m5_timing import compute_next_m5, parse_utc

if FastAPI is not None:
    app = FastAPI(title="Mercury AI — Top3 M5")
else:  # pragma: no cover
    app = None  # type: ignore


def _signals_of(rep: Dict[str, Any] | None) -> List[Dict[str, Any]]:
    if not isinstance(rep, dict):
        return []
    out = []
    for entry in list(rep.get("top3", []) or [])[:3]:
        sig = entry.get("signal", entry) if isinstance(entry, dict) else {}
        flat = dict(sig) if isinstance(sig, dict) else {}
        flat.setdefault("symbol", entry.get("symbol") if isinstance(entry, dict) else None)
        flat.setdefault("decision", entry.get("decision") if isinstance(entry, dict) else None)
        flat.setdefault("score", entry.get("score") if isinstance(entry, dict) else None)
        flat["entry_suggested_utc"] = flat.get("next_m5_ts")
        out.append(flat)
    return out


def clock_payload() -> Dict[str, Any]:
    rep = load_latest_scan_report()
    sigs = _signals_of(rep)
    last = sigs[0].get("last_m5_ts") if sigs else None
    nxt = compute_next_m5(last) if last else None
    now = datetime.now(timezone.utc)
    secs = None
    if nxt:
        try:
            secs = (parse_utc(nxt) - now).total_seconds()
        except Exception:
            secs = None
    return {
        "server_time_utc": now.isoformat(),
        "next_m5_utc": nxt,
        "seconds_to_next_m5": secs,
        "scan_id": (rep or {}).get("scan_id"),
        "status": (rep or {}).get("status"),
    }


def top3_payload() -> Dict[str, Any]:
    rep = load_latest_scan_report() or {}
    return {
        "scan_id": rep.get("scan_id"),
        "status": rep.get("status"),
        "server_time_utc": datetime.now(timezone.utc).isoformat(),
        "symbols_total": rep.get("symbols_total"),
        "symbols_completed": rep.get("symbols_completed"),
        "signals": _signals_of(rep),
    }


if app is not None:  # pragma: no cover

    @app.get("/api/clock/m5")
    def clock():
        return clock_payload()

    @app.get("/api/signals/top3")
    def top3():
        return top3_payload()

    @app.websocket("/ws/signals")
    async def ws_signals(ws: WebSocket):
        await ws.accept()
        import asyncio

        while True:
            await ws.send_json(top3_payload())
            await asyncio.sleep(10)
