"""
Testes para o gap classification do Data Quality Engine (data/data_quality_engine.py).

Sprint A — testes direcionados para gap-aware validation.
"""
import pandas as pd
import numpy as np
import pytest
from mercury_ai.data.data_quality_engine import DataQualityEngine


def make_df(dates, close=None):
    """Helper: cria DataFrame com colunas OHLCV lowercase."""
    n = len(dates)
    if close is None:
        close = np.random.RandomState(42).randn(n) * 100 + 100
    close = np.abs(close) + 10  # garante valores positivos
    df = pd.DataFrame({
        'open': close,
        'high': close + 10,
        'low': close - 5,
        'close': close,
        'volume': np.random.RandomState(42).randint(100, 1000, n),
    }, index=pd.DatetimeIndex(dates, tz='UTC'))
    return df


def test_continuous_data_passes():
    """TESTE A: Candles contínuos durante sessão válida → PASS."""
    engine = DataQualityEngine()
    dates = pd.date_range("2025-01-01 09:30:00", periods=20, freq="5min", tz="UTC")
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is True
    assert score == 1.0


def test_legitimate_non_trading_gap_allowed():
    """TESTE B: Gap legítimo (crosses UTC day boundary, 45min) → PASS with reservation."""
    engine = DataQualityEngine()
    # 10 candles at 23:00-23:45 UTC, then 45min gap to 00:30 next day (crosses UTC midnight)
    dates1 = pd.date_range("2026-08-11 23:00:00", periods=10, freq="5min", tz="UTC")
    dates2 = pd.date_range("2026-08-12 00:30:00", periods=10, freq="5min", tz="UTC")
    dates = list(dates1) + list(dates2)
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is True, f"Gap legítimo deveria passar: {reason}"
    assert score < 1.0, "Score deve ser degradado para gap não-trading"


def test_unexpected_data_gap_rejected():
    """TESTE C: Gap artificial dentro da sessão → FAIL / GAP DETECTED."""
    engine = DataQualityEngine()
    # Gap de 2 horas dentro da mesma sessão (sem crossing day boundary)
    dates1 = pd.date_range("2025-01-01 09:30:00", periods=10, freq="5min", tz="UTC")
    # 2 hour gap
    dates2 = pd.date_range("2025-01-01 12:00:00", periods=10, freq="5min", tz="UTC")
    dates = dates1.append(dates2)
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is False, f"Gap inesperado deveria ser rejeitado: {reason}"
    assert "gap" in reason.lower()


def test_duplicate_timestamps_rejected():
    """TESTE D: Timestamps duplicados → rejeição conforme contrato existente."""
    engine = DataQualityEngine()
    dates = pd.to_datetime([
        "2025-01-01 09:30:00",
        "2025-01-01 09:35:00",
        "2025-01-01 09:35:00",  # duplicate
    ]).tz_localize("UTC")
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is False
    assert "duplicate" in reason.lower()


def test_out_of_order_timestamps_rejected():
    """TESTE E: Timestamps fora de ordem → rejeição conforme contrato existente."""
    engine = DataQualityEngine()
    dates = pd.to_datetime([
        "2025-01-01 09:30:00",
        "2025-01-01 09:35:00",
        "2025-01-01 09:32:00",  # out of order
    ]).tz_localize("UTC")
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is False
    assert "gap" in reason.lower() or "order" in reason.lower() or "duplicate" in reason.lower()


def test_invalid_timestamp_nat_rejected():
    """TESTE F: Timestamp inválido / NaT → falha explícita, não mascarada."""
    engine = DataQualityEngine()
    dates = pd.to_datetime([
        "2025-01-01 09:30:00",
        "NaT",
        "2025-01-01 09:40:00",
    ]).tz_localize("UTC")
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is False, "NaT deve ser rejeitado explicitamente"


def test_timezone_consistency():
    """TESTE G: Timezone consistente → resultado determinístico."""
    engine = DataQualityEngine()
    dates1 = pd.date_range("2025-01-01 09:30:00", periods=20, freq="5min", tz="UTC")
    df1 = make_df(dates1)
    is_valid1, score1, reason1 = engine.validate(df1)

    dates2 = pd.date_range("2025-01-02 09:30:00", periods=20, freq="5min", tz="UTC")
    df2 = make_df(dates2)
    is_valid2, score2, reason2 = engine.validate(df2)

    assert is_valid1 == is_valid2
    assert score1 == score2  # determinismo (mesmos valores de close)


def test_real_yahoo_gap_pattern():
    """Teste com padrão real observado no Yahoo Finance crypto (45min gap no meia-noite UTC)."""
    engine = DataQualityEngine()
    dates1 = pd.date_range("2026-08-11 23:00:00", periods=5, freq="5min", tz="UTC")
    dates2 = pd.DatetimeIndex(["2026-08-12 00:00:00"], tz="UTC")
    dates3 = pd.date_range("2026-08-12 00:05:00", periods=5, freq="5min", tz="UTC")
    dates = dates1.append(dates2).append(dates3)
    df = make_df(dates)
    is_valid, score, reason = engine.validate(df)
    assert is_valid is True, f"Yahoo crypto gap (45min midnight UTC) deve ser EXPECTED_NON_TRADING: {reason}"
