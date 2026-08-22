"""Testes do MercuryDataProvider sem acesso à rede.

O arquivo original fazia uma chamada de rede em nível de módulo
(``provider.get_data("GC=F")``), o que travava a coleta do pytest.
Estes testes usam mocks para validar o comportamento do provider
sem depender de ``yfinance``/rede.
"""
import pandas as pd
import pytest

from mercury_ai.providers.market_provider import MercuryDataProvider


def _make_provider():
    return MercuryDataProvider()


def test_registers_six_adapters():
    provider = _make_provider()
    assert len(provider._providers) == 6


def test_only_yahoo_is_implemented():
    provider = _make_provider()
    healthy = provider._healthy_providers()
    assert [p.name for p in healthy] == ["Yahoo"]


def test_get_data_returns_dataframe(monkeypatch):
    provider = _make_provider()

    def fake_get_data(self, symbol, interval="5m"):
        return pd.DataFrame({"open": [1.0], "close": [1.1]})

    monkeypatch.setattr(
        "mercury_ai.providers.data_adapters.YahooAdapter.get_data",
        fake_get_data,
    )
    data = provider.get_data("GC=F")
    assert isinstance(data, pd.DataFrame)
    assert not data.empty


def test_get_data_no_healthy_provider_raises(monkeypatch):
    provider = _make_provider()
    # Simula ausência de provider saudável.
    monkeypatch.setattr(provider, "_healthy_providers", lambda: [])
    with pytest.raises(RuntimeError):
        provider.get_data("GC=F")