"""C4 — Autenticação por sessão (senha via variável de ambiente).

Módulo compartilhado de autenticação para todos os apps Streamlit.
A senha é validada contra o hash SHA-256 configurado na variável de
ambiente ``MERCURY_AUTH_HASH`` usando comparação timing-safe.
"""

import hashlib
import hmac
import os

import streamlit as st

_MERCURY_AUTH_HASH = os.environ.get("MERCURY_AUTH_HASH", "")


def hash_password(password: str) -> str:
    """Gera hash SHA-256 da senha."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def check_auth() -> bool:
    """Verifica se o usuário está autenticado nesta sessão."""
    return st.session_state.get("authenticated", False)


def do_login(password: str) -> bool:
    """Valida a senha contra o hash configurado e marca a sessão."""
    if not _MERCURY_AUTH_HASH:
        st.error(
            "⚠️ Nenhuma senha configurada. Defina a variável de ambiente "
            "`MERCURY_AUTH_HASH` com o hash SHA-256 da senha desejada."
        )
        return False
    computed = hash_password(password)
    if hmac.compare_digest(computed, _MERCURY_AUTH_HASH):
        st.session_state["authenticated"] = True
        return True
    return False


def do_logout() -> None:
    """Remove a autenticação da sessão."""
    st.session_state["authenticated"] = False
    st.rerun()


def require_auth() -> None:
    """Gate de autenticação — exibe tela de login e para execução se não autenticado.

    Deve ser chamado no início de cada app Streamlit, após ``st.set_page_config``.
    """
    if check_auth():
        return

    st.title("🔒 Mercury AI Terminal — Autenticação")
    st.markdown("### Centro de Operações Institucional")
    st.markdown("---")
    password = st.text_input("Senha de acesso:", type="password")
    if st.button("Entrar"):
        if do_login(password):
            st.success("Autenticado com sucesso!")
            st.rerun()
        else:
            st.error("Senha incorreta.")
    st.stop()


def render_logout_button() -> None:
    """Exibe botão de logout no sidebar (chamar após auth)."""
    if st.sidebar.button("🔒 Logout"):
        do_logout()
