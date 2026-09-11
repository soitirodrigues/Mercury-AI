"""M5 widgets — relogio + countdown + cards Top-3 (apresentacao, sem inteligencia).

Encaixe direto em app/terminal/pages/01_Scanner.py e app/dashboard/dashboard.py:
    from app.dashboard.m5_widgets import render_m5_clock, render_signal_cards

Regras: nunca recalcula, nunca inventa. Consome ScanReport dict / top3 ja filtrado.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

try:
    import streamlit as st
except ImportError:  # pragma: no cover
    st = None

from mercury_ai.signals.m5_timing import compute_next_m5, parse_utc


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def render_m5_clock(last_m5_ts: Optional[str]) -> None:
    """Relogio servidor/corretora + contagem regressiva p/ proxima vela M5."""
    if st is None:
        return
    nxt = compute_next_m5(last_m5_ts)
    now = _now_utc()
    st.subheader("⏱ Relógio M5 (UTC)")
    st.caption(f"Servidor: {now.isoformat(timespec='seconds')}")
    if not nxt:
        st.warning("Relógio M5 indisponível — sem vela fechada (timing nunca inferido).")
        return
    secs = max(0.0, (parse_utc(nxt) - now).total_seconds())
    mm, ss = int(secs // 60), int(secs % 60)
    st.metric("Tempo para a próxima vela", f"{mm:02d}:{ss:02d}")
    st.caption(f"Entrada sugerida: vela das {nxt} (UTC, market-on-open)")


def render_signal_cards(signals: List[Dict[str, Any]]) -> None:
    """Cards Top-3: ativo, direcao, entry/SL/TP, RR>=2, score, setup."""
    if st is None:
        return
    st.subheader("🎯 Top-3 Sinais Consistentes")
    if not signals:
        st.info("Sem setup válido neste ciclo — 0 sinais (nenhum inventado).")
        return
    cols = st.columns(min(3, len(signals)))
    for col, entry in zip(cols, signals[:3]):
        sig = entry.get("signal", entry) if isinstance(entry, dict) else {}
        with col:
            sym = entry.get("symbol") or sig.get("symbol") or "?"
            dec = entry.get("decision") or sig.get("decision") or "WAIT"
            color = "🟢" if dec == "BUY" else ("🔴" if dec == "SELL" else "⚪")
            st.markdown(f"### {color} {sym} — {dec}")
            st.write(
                f"**Entrada:** {sig.get('entry_price')} | "
                f"**SL:** {sig.get('stop_loss')} | **TP:** {sig.get('take_profit')}"
            )
            try:
                rr = float(sig.get("risk_reward", 0) or 0)
            except (TypeError, ValueError):
                rr = 0.0
            st.write(
                f"**R/R:** {rr:.1f} | **Score:** {entry.get('score', sig.get('score', 0))} | "
                f"**Conf:** {entry.get('confidence', sig.get('confidence', 0))}"
            )
            st.caption(f"Setup: {entry.get('setup_label', sig.get('setup', 'Confluence'))}")
            st.caption(
                f"Entrada sugerida: {sig.get('next_m5_ts')} UTC | "
                f"{sig.get('entry_timing_state')} ({sig.get('entry_window_seconds', 0)}s)"
            )
            reason = (sig.get("reason") or "")[:220]
            if reason:
                st.caption(reason)
