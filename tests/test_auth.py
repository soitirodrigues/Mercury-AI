"""Testes para o módulo de autenticação (C4)."""

import hashlib
import importlib
import os

import pytest

import app.auth as auth_module


@pytest.fixture(autouse=True)
def _reset_auth_env(monkeypatch):
    """Garante ambiente limpo antes de cada teste."""
    monkeypatch.delenv("MERCURY_AUTH_HASH", raising=False)
    yield
    monkeypatch.delenv("MERCURY_AUTH_HASH", raising=False)


def _set_hash(monkeypatch, password: str):
    """Configura o hash SHA-256 da senha no ambiente e recarrega o módulo."""
    h = hashlib.sha256(password.encode("utf-8")).hexdigest()
    monkeypatch.setenv("MERCURY_AUTH_HASH", h)
    importlib.reload(auth_module)


def test_hash_password():
    """hash_password deve gerar SHA-256 correto."""
    result = auth_module.hash_password("minhaSenha123")
    expected = hashlib.sha256("minhaSenha123".encode("utf-8")).hexdigest()
    assert result == expected
    assert len(result) == 64


def test_hash_password_unicode():
    """hash_password deve lidar com caracteres Unicode."""
    result = auth_module.hash_password("senhação@123")
    expected = hashlib.sha256("senhação@123".encode("utf-8")).hexdigest()
    assert result == expected


def test_check_auth_default_false():
    """check_auth deve retornar False quando não autenticado."""
    # Simula session_state vazio
    class FakeSessionState(dict):
        def get(self, key, default=None):
            return super().get(key, default)

    # Monkeypatch st.session_state
    original = auth_module.st.session_state
    auth_module.st.session_state = FakeSessionState()
    try:
        assert auth_module.check_auth() is False
    finally:
        auth_module.st.session_state = original


def test_check_auth_true_when_authenticated():
    """check_auth deve retornar True quando authenticated=True."""
    class FakeSessionState(dict):
        def get(self, key, default=None):
            return super().get(key, default)

    fake = FakeSessionState()
    fake["authenticated"] = True
    original = auth_module.st.session_state
    auth_module.st.session_state = fake
    try:
        assert auth_module.check_auth() is True
    finally:
        auth_module.st.session_state = original


def test_do_login_success(monkeypatch):
    """do_login deve autenticar com senha correta."""
    _set_hash(monkeypatch, "senhaCorreta")
    fake_session = {}
    original = auth_module.st.session_state
    auth_module.st.session_state = fake_session
    try:
        result = auth_module.do_login("senhaCorreta")
        assert result is True
        assert fake_session.get("authenticated") is True
    finally:
        auth_module.st.session_state = original


def test_do_login_wrong_password(monkeypatch):
    """do_login deve rejeitar senha incorreta."""
    _set_hash(monkeypatch, "senhaCorreta")
    fake_session = {}
    original = auth_module.st.session_state
    auth_module.st.session_state = fake_session
    try:
        result = auth_module.do_login("senhaErrada")
        assert result is False
        assert fake_session.get("authenticated") is not True
    finally:
        auth_module.st.session_state = original


def test_do_login_no_hash_configured(monkeypatch):
    """do_login deve falhar quando MERCURY_AUTH_HASH não está configurado."""
    monkeypatch.delenv("MERCURY_AUTH_HASH", raising=False)
    importlib.reload(auth_module)
    fake_session = {}
    original = auth_module.st.session_state
    auth_module.st.session_state = fake_session
    try:
        result = auth_module.do_login("qualquerSenha")
        assert result is False
        assert "authenticated" not in fake_session
    finally:
        auth_module.st.session_state = original


def test_do_logout(monkeypatch):
    """do_logout deve remover autenticação e chamar st.rerun."""
    fake_session = {"authenticated": True}
    rerun_called = []
    original_session = auth_module.st.session_state
    original_rerun = auth_module.st.rerun

    auth_module.st.session_state = fake_session
    auth_module.st.rerun = lambda: rerun_called.append(True)
    try:
        auth_module.do_logout()
        assert fake_session.get("authenticated") is False
        assert len(rerun_called) == 1
    finally:
        auth_module.st.session_state = original_session
        auth_module.st.rerun = original_rerun


def test_require_auth_already_authenticated(monkeypatch):
    """require_auth deve retornar imediatamente se já autenticado."""
    fake_session = {"authenticated": True}
    original = auth_module.st.session_state
    auth_module.st.session_state = fake_session
    try:
        # Não deve chamar st.stop()
        auth_module.require_auth()
    finally:
        auth_module.st.session_state = original


def test_require_auth_not_authenticated_calls_stop(monkeypatch):
    """require_auth deve chamar st.stop() quando não autenticado."""
    fake_session = {}
    stop_called = []
    original_session = auth_module.st.session_state
    original_stop = auth_module.st.stop

    auth_module.st.session_state = fake_session
    auth_module.st.stop = lambda: stop_called.append(True)
    try:
        auth_module.require_auth()
        assert len(stop_called) == 1
    finally:
        auth_module.st.session_state = original_session
        auth_module.st.stop = original_stop
