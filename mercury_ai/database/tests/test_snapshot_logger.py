# -*- coding: utf-8 -*-
"""B4-C5 - Testes R1: SnapshotLogger aceita timestamps timezone-aware.

Valida a correção R1 (B4-C5): timestamp aware válido não pode causar crash
no salvamento de snapshot. O sanitizador agora normaliza o sinal '+' de
offset ISO 8601 ('+01:00') para '_', preservando o instante no conteúdo JSON.
"""
import json
import re
from pathlib import Path
from unittest.mock import MagicMock

import pandas as pd
import pytest

from mercury_ai.database.snapshot_logger import (
    _sanitize_filename_component,
    DecisionSnapshotLogger,
)
from mercury_ai.models.decision_snapshot import DecisionSnapshot

# Whitelist de nome de arquivo (mesmo do módulo) — usado para validar a saída.
_SAFE_SYMBOL_RE = re.compile(r"^[A-Za-z0-9._\-]+$")

# Casos A-E do requisito B4-C5 (seção 6).
# (input, rótulo, descrição)
CASES = [
    ("2024-01-01T07:40:00", "A-naive-utc", "naive UTC (contrato tempo real)"),
    ("2024-01-01T07:40:00+00:00", "B-aware-utc", "aware UTC (Yahoo iso)"),
    ("2024-01-01T07:40:00+01:00", "C-aware-london", "aware Europe/London (replay parquet)"),
    ("2024-01-01T07:40:00-03:00", "D-aware-offset", "aware offset diferente (America/Sao_Paulo)"),
    ("2026-03-29T01:30:00+00:00", "E-dst-transition", "próximo de transição de offset (DST)"),
]


def _make_snapshot(timestamp_str: str, asset: str = "BTC-USD") -> DecisionSnapshot:
    return DecisionSnapshot(
        timestamp=timestamp_str,
        asset=asset,
        timeframe="5m",
        context=MagicMock(),
        evidence_bundle=MagicMock(),
        decision_result=MagicMock(),
        version_metadata=MagicMock(),
        audit_events=(),
        session_id="b4c5-test",
    )


def _epoch(iso_str: str) -> float:
    """Epoch (segundos) de uma string ISO 8601 (naive ou aware)."""
    return pd.Timestamp(iso_str).timestamp()


# ===================================================================== #
#  A-E: NENHUM timestamp válido pode causar crash + instante preservado  #
# ===================================================================== #
@pytest.mark.parametrize(
    "input_ts,label,description", CASES, ids=[c[1] for c in CASES]
)
def test_sanitizer_accepts_valid_timestamp(tmp_path, input_ts, label, description):
    """O sanitizador aceita o timestamp (naive ou aware) sem exceção."""
    try:
        out = _sanitize_filename_component(input_ts)
    except ValueError as e:
        pytest.fail(f"sanitizer rejeitou timestamp válido {input_ts!r}: {e}")
    # Nome de arquivo resultante deve estar dentro do whitelist seguro.
    assert _SAFE_SYMBOL_RE.match(out), f"saída fora do whitelist: {out!r}"


@pytest.mark.parametrize(
    "input_ts,label,description", CASES, ids=[c[1] for c in CASES]
)
def test_save_no_crash_and_instant_preserved(tmp_path, input_ts, label, description):
    """O caminho real de save não crasha e o instante é preservado.

    epoch_before == epoch_after (não aceitamos apenas igualdade textual).
    """
    logger = DecisionSnapshotLogger(base_path=str(tmp_path))
    snap = _make_snapshot(input_ts)
    logger.save(snap)

    files = sorted(tmp_path.glob("*.json"))
    assert len(files) == 1, f"esperado 1 snapshot salvo, obtido {len(files)}"
    assert files[0].name.count("+") == 0, f"filename contém '+' não sanitizado: {files[0].name}"

    with open(files[0], "r", encoding="utf-8") as f:
        data = json.load(f)

    saved_ts = data["timestamp"]
    assert saved_ts == input_ts, (
        f"conteúdo JSON do timestamp alterado: {saved_ts!r} != {input_ts!r}"
    )

    epoch_before = _epoch(input_ts)
    epoch_after = _epoch(saved_ts)
    assert epoch_before == epoch_after, (
        f"instante NÃO preservado: {epoch_before} != {epoch_after} ({label})"
    )


@pytest.mark.parametrize(
    "input_ts,label,description", CASES, ids=[c[1] for c in CASES]
)
def test_snapshot_roundtrip_load(tmp_path, input_ts, label, description):
    """Snapshot salvo pode ser relido via load_snapshot (consumidor)."""
    logger = DecisionSnapshotLogger(base_path=str(tmp_path))
    logger.save(_make_snapshot(input_ts))
    paths = logger.list_snapshots()
    assert len(paths) == 1
    data = logger.load_snapshot(paths[0])
    assert data["timestamp"] == input_ts


# ===================================================================== #
#  Compatibilidade: timestamps naive existentes NÃO quebram              #
# ===================================================================== #
def test_existing_naive_filename_unchanged(tmp_path):
    """Naive continua gerando o mesmo nome de arquivo de antes."""
    out = _sanitize_filename_component("2024-01-01T07:40:00")
    assert out == "2024-01-01T07-40-00"


def test_yahoo_symbol_sanitized(tmp_path):
    """Símbolos Yahoo com '=' continuam normalizados (EURUSD=X)."""
    out = _sanitize_filename_component("EURUSD=X")
    assert out == "EURUSD_X"


# ===================================================================== #
#  Segurança: sanitizador continua rejeitando path traversal / vazio     #
# ===================================================================== #
@pytest.mark.parametrize("bad", ["", "../etc/passwd", "a/b", "a\\b", "..", "a..b"])
def test_sanitizer_still_rejects_unsafe(bad):
    """Path traversal / vazio / barras continuam rejeitados (segurança)."""
    with pytest.raises(ValueError):
        _sanitize_filename_component(bad)


# ===================================================================== #
#  Crash real do B4-C4: aware +01:00 reproduzido e agora salva           #
# ===================================================================== #
def test_b4c4_crash_scenario_now_saves(tmp_path):
    """Cenário exato do B4-C4 (Europe/London +01:00) agora salva sem crash."""
    logger = DecisionSnapshotLogger(base_path=str(tmp_path))
    snap = _make_snapshot("2024-01-01T07:40:00+01:00", asset="EURUSD=X")
    result = logger.save(snap)
    assert result is snap
    files = sorted(tmp_path.glob("*.json"))
    assert len(files) == 1
    assert files[0].name == "EURUSD_X_2024-01-01T07-40-00_01-00.json"
