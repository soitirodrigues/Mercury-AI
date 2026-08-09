import streamlit as st
import sys

from app.auth import require_auth, render_logout_button

st.set_page_config(page_title="Mercury Launcher", page_icon="🚀", layout="centered")

# ------------------------------------------------------------------ #
#  C4 — Gate de autenticação
# ------------------------------------------------------------------ #
require_auth()

# ------------------------------------------------------------------ #
#  Aplicação principal (após autenticação)
# ------------------------------------------------------------------ #
st.title("🚀 Mercury AI Terminal")
st.markdown("### Centro de Operações Institucional")

st.sidebar.markdown("### Navegação")
if st.sidebar.button("Dashboard Institucional"):
    st.switch_page("app/dashboard/dashboard.py")
if st.sidebar.button("Scanner Institucional"):
    st.switch_page("app/terminal/pages/01_Scanner.py")
if st.sidebar.button("Histórico e Estatísticas"):
    st.switch_page("app/terminal/pages/03_Historico_Estatisticas.py")
if st.sidebar.button("Auditoria e Configurações"):
    st.switch_page("app/terminal/pages/04_Auditoria_Configuracoes.py")

st.sidebar.markdown("---")
render_logout_button()

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    st.write("### Auditoria Rápida")
    from mercury_ai.analysis.health_checker import HealthChecker
    health = HealthChecker().check()
    st.write(f"**Sistema:** {'🟢 OK' if health.system_ready else '🔴 FALHA'}")

with col2:
    st.write("### Ações")
    if st.button("Sair"):
        st.write("Encerrando...")
        sys.exit(0)
