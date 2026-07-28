import streamlit as st
import sys
import os
import hashlib
import hmac

st.set_page_config(page_title="Mercury Launcher", page_icon="🚀", layout="centered")

# ------------------------------------------------------------------ #
#  C4 — Autenticação por sessão (senha via variável de ambiente)
# ------------------------------------------------------------------ #
_MERCURY_AUTH_HASH = os.environ.get("MERCURY_AUTH_HASH", "")


def _hash_password(password: str) -> str:
    """Gera hash SHA-256 da senha."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _check_auth() -> bool:
    """Verifica se o usuário está autenticado nesta sessão."""
    return st.session_state.get("authenticated", False)


def _do_login(password: str) -> bool:
    """Valida a senha contra o hash configurado e marca a sessão."""
    if not _MERCURY_AUTH_HASH:
        # Se nenhuma senha configurada, exibe aviso e bloqueia acesso
        st.error(
            "⚠️ Nenhuma senha configurada. Defina a variável de ambiente "
            "`MERCURY_AUTH_HASH` com o hash SHA-256 da senha desejada."
        )
        return False
    computed = _hash_password(password)
    if hmac.compare_digest(computed, _MERCURY_AUTH_HASH):
        st.session_state["authenticated"] = True
        return True
    return False


def _do_logout():
    """Remove a autenticação da sessão."""
    st.session_state["authenticated"] = False
    st.rerun()


# Tela de login
if not _check_auth():
    st.title("🔒 Mercury AI Terminal — Autenticação")
    st.markdown("### Centro de Operações Institucional")
    st.markdown("---")
    password = st.text_input("Senha de acesso:", type="password")
    if st.button("Entrar"):
        if _do_login(password):
            st.success("Autenticado com sucesso!")
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()

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
if st.sidebar.button("🔒 Logout"):
    _do_logout()

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
