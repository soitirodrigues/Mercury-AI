import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time
from mercury_ai.brain.scan_service import run_dashboard_scan
from app.dashboard.scan_presentation import (
    present_scan,
    status_banner,
    counters_line,
)
from mercury_ai.config import settings
from mercury_ai.signals.top3_selector import select_top3
from app.dashboard.m5_widgets import render_m5_clock, render_signal_cards
from app.dashboard.scan_alerts import render_scan_progress, render_scan_done_sound

st.set_page_config(page_title="Scanner Institucional", layout="wide")
st.title("🔍 Scanner Institucional")

# Load data (Cached) — S33-E.5: UMA execucao workers=4 + ScanReport real.
# S33-E.6: APENAS apresentacao do envelope (TOP3/status/contadores verbatim).
@st.cache_data(ttl=60)
def load_data():
    ranked, report = run_dashboard_scan()
    return ranked, report.to_dict()

analyses, scan_report = load_data()
view = present_scan(scan_report)
# Alerta sonoro 1x por scan_id + banner gigante (ver outra tela).
render_scan_done_sound(view)
# Andamento REAL completed/total + contadores + ultimos concluidos.
render_scan_progress(view)
st.caption(
    f"scan_id={view.get('scan_id')} "
    f"status={view.get('status')} "
    f"completed={view.get('progress_text')} "
    f"ranqueados={view.get('ranked_count')} "
    f"workers={view.get('workers')}"
)
st.caption(counters_line(view))
st.caption(status_banner(view))

# M5-SMC: relógio servidor + countdown (fronteira de last_m5_ts do Top-3).
_top3_raw = view.get("top3") or []
_last_m5 = None
try:
    _first = _top3_raw[0] if _top3_raw else None
    _sig0 = (_first.get("signal") if isinstance(_first, dict) else None) or {}
    _last_m5 = _sig0.get("last_m5_ts")
except Exception:
    _last_m5 = None
render_m5_clock(_last_m5)

# M5-SMC: Top-3 filtrado (BUY/SELL + VALID + RR>=2 + score>=70, 0..3).
# O ScanReport bruto permanece exibido abaixo, verbatim, sem recálculo.
_top3 = select_top3(scan_report)
render_signal_cards(_top3)

st.subheader("TOP 3 — ScanReport (bruto, sem recálculo)")
if view.get("has_top3"):
    st.dataframe(pd.DataFrame(view.get("top3")), use_container_width=True)
else:
    st.info(
        "TOP 3 vazio neste ciclo — nenhum item inventado. "
        f"(status={view.get('status')} completed={view.get('progress_text')})"
    )

# Controls
col_ctrl1, col_ctrl2 = st.columns([1, 4])
with col_ctrl1:
    if st.button("Atualizar"):
        st.cache_data.clear()
        st.rerun()
with col_ctrl2:
    auto_refresh = st.checkbox("Atualização Automática")

if auto_refresh:
    time.sleep(settings.MONITORING_INTERVAL)
    st.rerun()

# Filtering
available_assets = [a.market.symbol for a in analyses]
available_decisions = list(set([a.decision.decision for a in analyses]))

filter_asset = st.multiselect("Filtrar Ativo", available_assets)
filter_decision = st.multiselect("Filtrar Decisão", available_decisions)

# Process Data
scan_data = []
for a in analyses:
    if filter_asset and a.market.symbol not in filter_asset: continue
    if filter_decision and a.decision.decision not in filter_decision: continue
    
    scan_data.append({
        "Ativo": a.market.symbol,
        "Decisão": a.decision.decision,
        "Confiança": f"{a.decision.confidence*100:.1f}%",
        "Prob. Buy": f"{a.decision.buy_probability:.1f}%",
        "Prob. Sell": f"{a.decision.sell_probability:.1f}%",
        "Prob. Wait": f"{a.decision.wait_probability:.1f}%",
        "Regime": str(a.market_regime.regime) if a.market_regime else "N/A",
        "Score": a.decision.score,
        "Confluência": f"{a.decision.clarity:.1f}%",
        "Timestamp": a.timestamp[:19]
    })

st.dataframe(pd.DataFrame(scan_data), use_container_width=True)
