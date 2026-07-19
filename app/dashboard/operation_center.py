import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
from mercury_ai.brain.scanner import MercuryScanner
from mercury_ai.analysis.operational_history import OperationalHistory
from mercury_ai.analysis.performance_statistics import PerformanceStatistics
from mercury_ai.analysis.integrity_checker import IntegrityChecker
from mercury_ai.analysis.health_checker import HealthChecker
from mercury_ai.config import settings

st.set_page_config(page_title="Mercury Operation Center", layout="wide")

st.title("🛡️ Mercury AI | Operation Center")

# Sidebar - Demo Mode Status
st.sidebar.subheader("Modo de Operação")
st.sidebar.write(f"**Demo Mode:** {'ATIVO' if settings.READ_ONLY else 'DESATIVADO'}")
st.sidebar.write(f"**Versão:** {settings.VERSION}")

# 1. Scanner & Market
st.header("1. Scanner & Mercado")
analyses = MercuryScanner().scan()
if analyses:
    analysis = analyses[0] # Mostrando o primeiro por conveniência
    st.metric("Ativo", analysis.market.symbol)
    st.metric("Regime", str(analysis.market_regime.regime) if analysis.market_regime else "N/A")
else:
    st.warning("Scanner vazio.")

# 2. Última Decisão & Snapshot
st.header("2. Última Decisão")
if analyses:
    st.write(f"**Decisão:** {analysis.decision.decision}")
    st.write(f"**Confidence:** {analysis.decision.confidence*100:.1f}%")
    st.write(f"**Timestamp:** {analysis.timestamp[:19]}")

# 3. Histórico e Replay
st.header("3. Histórico e Replay")
history = OperationalHistory().query()
st.dataframe(pd.DataFrame(history))

# 4. Performance e Estatísticas
st.header("4. Performance e Estatísticas")
stats = PerformanceStatistics().calculate()
st.json(stats)

# 5. Auditoria e Logs
st.header("5. Auditoria e Logs")
col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Integridade")
    st.write(IntegrityChecker().check_all())
with col_b:
    st.subheader("Logs")
    log_path = Path("logs")
    if list(log_path.glob("*.log")):
        st.write("Logs disponíveis.")
    else:
        st.write("Nenhum log disponível.")

# 6. Monitoramento
st.header("6. Monitoramento")
st.json(HealthChecker().check().components)
