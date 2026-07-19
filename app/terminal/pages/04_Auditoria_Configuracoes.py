import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))

import streamlit as st
from mercury_ai.analysis.integrity_checker import IntegrityChecker
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.config import settings

st.title("Auditoria e Configurações")

st.subheader("Integridade")
st.write(IntegrityChecker().check_all())

st.subheader("Configurações")
st.write(f"Versão: {settings.VERSION}")
st.write(f"Read Only: {settings.READ_ONLY}")
