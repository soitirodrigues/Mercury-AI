"""S33-E.6 — Signal operational building blocks (SIGNAL-ONLY, SEM inteligencia).

Re-exporta o contrato formal (Signal), a matematica temporal M5 pura e o
builder AnalysisResult -> Signal (propagacao, sem recalculo).
+S33-M5: seletor Top-3 (filtra, nunca pontua) e janela de alerta 3m50s~4m05s.
"""
from mercury_ai.models.signal import Signal
from mercury_ai.signals.m5_timing import (
    EXPIRED_STATE,
    VALID_STATE,
    compute_entry_window,
    compute_next_m5,
    floor_m5,
    parse_utc,
    to_iso_utc,
)
from mercury_ai.signals.signal_builder import build_signal_from_analysis
from mercury_ai.signals.top3_selector import select_top3, setup_label
from mercury_ai.signals.m5_alerts import alert_state
from mercury_ai.signals.entry_time import (
    countdown_s,
    enrich_top3_oportunidades,
    format_br,
    next_entry_utc,
)

__all__ = [
    "Signal",
    "VALID_STATE",
    "EXPIRED_STATE",
    "build_signal_from_analysis",
    "compute_entry_window",
    "compute_next_m5",
    "floor_m5",
    "parse_utc",
    "to_iso_utc",
    "select_top3",
    "setup_label",
    "alert_state",
    "next_entry_utc",
    "format_br",
    "countdown_s",
    "enrich_top3_oportunidades",
]
