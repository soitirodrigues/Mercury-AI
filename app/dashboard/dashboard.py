import sys
from pathlib import Path

# adiciona a raiz do projeto ao PYTHONPATH
ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd

from mercury_ai.brain.scanner import Scanner

st.set_page_config(
    page_title="Mercury AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Mercury AI")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Mercado", "ONLINE")

with col2:
    st.metric("Sessão", "Londres")

with col3:
    st.metric("Mercury Brain", "ATIVO")

st.markdown("---")

st.subheader("Scanner de Ativos")

scanner = Scanner()

dados = scanner.scan()

df = pd.DataFrame(dados)

st.dataframe(df, use_container_width=True)