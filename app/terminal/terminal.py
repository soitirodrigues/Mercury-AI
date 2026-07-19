import streamlit as st
from app.ui_utils import apply_design_system, display_status, display_card
from mercury_ai.config import settings
from mercury_ai.analysis.health_checker import HealthChecker

st.set_page_config(page_title="Mercury Terminal", layout="wide", page_icon="🛡️")
apply_design_system()

st.title("🛡️ Mercury AI | Terminal Operacional")
st.markdown("---")

# Status Panel
health = HealthChecker().check()

col1, col2, col3 = st.columns(3)
col1.metric("Status do Sistema", "🟢 OPERACIONAL" if health.system_ready else "🔴 FALHA")
col2.metric("Versão", settings.VERSION)
col3.metric("Modo Demo", "ATIVO" if settings.READ_ONLY else "INATIVO")

st.markdown("---")

# Navigation Hub
st.subheader("Navegação Institucional")
c1, c2, c3 = st.columns(3)

with c1:
    display_card("📊 Análise", "Gerencie o Scanner e Dashboard")
    st.page_link("pages/01_Scanner.py", label="Scanner Institucional", icon="🔍")
    st.page_link("pages/02_Dashboard.py", label="Dashboard Operacional", icon="📈")

with c2:
    display_card("⚙️ Auditoria e Saúde", "Auditoria e Configurações")
    st.page_link("pages/04_Auditoria_Configuracoes.py", label="Auditoria e Configurações", icon="🛡️")

with c3:
    display_card("📝 Histórico", "Trading Journal e Performance")
    st.page_link("pages/03_Historico_Estatisticas.py", label="Histórico e Performance", icon="📋")

st.markdown("---")
st.info("Mercury AI V1 | Modo Read-Only Ativado por Segurança.")
