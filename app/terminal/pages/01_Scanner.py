import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import time
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.config import settings

st.set_page_config(page_title="Scanner Institucional", layout="wide")
st.title("🔍 Scanner Institucional")

# Load data (Cached)
@st.cache_data(ttl=60)
def load_data():
    return MercuryScanner().scan()

analyses = load_data()

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
