import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.database.snapshot_logger import DecisionSnapshotLogger

st.set_page_config(page_title="Replay Institucional", layout="wide")
st.title("⏪ Replay Institucional")

logger = DecisionSnapshotLogger()
snapshots = logger.list_snapshots()

if not snapshots:
    st.warning("Nenhum snapshot encontrado para replay.")
    st.stop()

# State management
if 'replay_index' not in st.session_state:
    st.session_state.replay_index = 0

# Navigation
col1, col2, col3, col4 = st.columns(4)
if col1.button("◀ Anterior"):
    st.session_state.replay_index = max(0, st.session_state.replay_index - 1)
if col2.button("▶ Próximo"):
    st.session_state.replay_index = min(len(snapshots) - 1, st.session_state.replay_index + 1)
if col3.button("⏮ Primeiro"):
    st.session_state.replay_index = 0
if col4.button("⏭ Último"):
    st.session_state.replay_index = len(snapshots) - 1

# Load Snapshot
current_path = snapshots[st.session_state.replay_index]
data = logger.load_snapshot(current_path)

st.subheader(f"Snapshot: {current_path.name}")

# Metrics
dr = data['decision_result']
col_m1, col_m2, col_m3 = st.columns(3)
col_m1.metric("Decisão", dr['decision'])
col_m2.metric("Confiança", f"{dr['confidence']*100:.1f}%")
col_m3.metric("Regime", data.get('context', {}).get('market_regime', {}).get('regime', 'N/A'))

# Details
st.subheader("Narrativa")
st.info(dr.get('summary', 'Sem narrativa.'))

st.subheader("Probabilidades")
st.write(dr.get('buy_probability'), dr.get('sell_probability'), dr.get('wait_probability'))

st.subheader("Evidências e Ranking")
if data.get('evidence_ranking'):
    st.write(data['evidence_ranking'])
else:
    st.write("Sem ranking detalhado.")
