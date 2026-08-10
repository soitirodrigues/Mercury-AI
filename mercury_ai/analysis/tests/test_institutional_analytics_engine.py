# -*- coding: utf-8 -*-
"""B4-C5 - Testes R2: institutional_analytics_engine não perde timestamps aware.

Valida a correção R2 (B4-C5): `pd.to_datetime` com `format="mixed"` + `utc=True`
+ `.dt.tz_localize(None)` em `_load_data`:
- timestamps aware válidos NÃO viram NaT (preservando o instante, normalizados
  para naive UTC);
- timestamps inválidos continuam virando NaT (detectáveis, não mascarados).
"""
import json
import shutil
from pathlib import Path

import pandas as pd
import pytest

from mercury_ai.analysis.institutional_analytics_engine import (
    InstitutionalAnalyticsEngine,
)


def _write_snapshot(snap_dir: Path, audit_id: str, timestamp: str):
    """Cria um snapshot JSON mínimo aceito por _load_data."""
    data = {
        "timestamp": timestamp,
        "asset": "BTC-USD",
        "timeframe": "5m",
        "decision_result": {
            "audit_id": audit_id,
            "decision": "WAIT",
            "score": 60.0,
            "confidence": 0.6,
        },
        "evidence_bundle": {"evidences": []},
    }
    (snap_dir / f"{audit_id}.json").write_text(
        json.dumps(data), encoding="utf-8"
    )


def _write_replay_metric(replay_dir: Path, audit_id: str):
    """Cria um replay metric JSON mínimo (chave = audit_id)."""
    data = {"hit": True, "pl": 1.0, "return_pct": 0.01}
    (replay_dir / f"{audit_id}.json").write_text(
        json.dumps(data), encoding="utf-8"
    )


def _engine(tmp_path) -> InstitutionalAnalyticsEngine:
    snap_dir = tmp_path / "snapshots"
    replay_dir = tmp_path / "replay"
    snap_dir.mkdir(parents=True, exist_ok=True)
    replay_dir.mkdir(parents=True, exist_ok=True)
    return InstitutionalAnalyticsEngine(
        snapshot_dir=str(snap_dir),
        replay_dir=str(replay_dir),
    )


# ===================================================================== #
#  Caso 1-4: timestamps válidos (naive/aware) NÃO viram NaT              #
# ===================================================================== #
@pytest.mark.parametrize(
    "ts,expected_naive_utc",
    [
        # naive UTC: mesmo valor (contrato tempo real)
        ("2024-01-01T07:40:00", "2024-01-01 07:40:00"),
        # aware UTC: instante preservado, normalizado para naive UTC
        ("2024-01-01T07:40:00+00:00", "2024-01-01 07:40:00"),
        # aware Europe/London (+01:00): 07:40 London = 06:40 UTC
        ("2024-01-01T07:40:00+01:00", "2024-01-01 06:40:00"),
        # aware offset -03:00: 07:40 São Paulo = 10:40 UTC
        ("2024-01-01T07:40:00-03:00", "2024-01-01 10:40:00"),
    ],
    ids=["naive-utc", "aware-utc", "aware-london", "aware-offset"],
)
def test_valid_timestamp_not_lost(tmp_path, ts, expected_naive_utc):
    """Timestamp válido (naive ou aware) é preservado em _load_data."""
    eng = _engine(tmp_path)
    _write_snapshot(Path(eng.snapshot_dir), "A1", ts)
    _write_replay_metric(Path(eng.replay_dir), "A1")

    df = eng._load_data()
    assert not df.empty
    assert df.loc[0, "timestamp"] == pd.Timestamp(expected_naive_utc)
    assert pd.isna(df.loc[0, "timestamp"]) is False


# ===================================================================== #
#  Caso 5: timestamp inválido continua virando NaT (detectável)          #
# ===================================================================== #
def test_invalid_timestamp_becomes_nat(tmp_path):
    """Timestamp realmente inválido vira NaT (não aceito silenciosamente)."""
    eng = _engine(tmp_path)
    _write_snapshot(Path(eng.snapshot_dir), "A1", "nao-e-timestamp")
    _write_replay_metric(Path(eng.replay_dir), "A1")

    df = eng._load_data()
    assert not df.empty
    assert pd.isna(df.loc[0, "timestamp"])


# ===================================================================== #
#  Caso 6: valor ausente (string vazia) vira NaT                         #
# ===================================================================== #
def test_missing_timestamp_becomes_nat(tmp_path):
    """Timestamp ausente (string vazia, do snapshot.get default) vira NaT."""
    eng = _engine(tmp_path)
    _write_snapshot(Path(eng.snapshot_dir), "A1", "")
    _write_replay_metric(Path(eng.replay_dir), "A1")

    df = eng._load_data()
    assert not df.empty
    assert pd.isna(df.loc[0, "timestamp"])


# ===================================================================== #
#  Caso 7: dataframe vazio (sem snapshots/replay) não dá erro            #
# ===================================================================== #
def test_empty_dataframe_no_error(tmp_path):
    """Sem snapshots com replay correspondente -> df vazio, sem exceção."""
    eng = _engine(tmp_path)
    df = eng._load_data()
    assert df.empty


# ===================================================================== #
#  Caso 8: mistura naive + aware (cenário replay+real) NÃO perde nada    #
# ===================================================================== #
def test_mixed_timestamps_all_preserved(tmp_path):
    """Cenário do B4-C4: mistura naive + aware -> nenhum válido vira NaT."""
    eng = _engine(tmp_path)
    mix = [
        ("2024-01-01T07:40:00", "2024-01-01 07:40:00"),       # naive UTC
        ("2024-01-01T07:45:00+01:00", "2024-01-01 06:45:00"),  # aware London
        ("2024-01-01T07:50:00", "2024-01-01 07:50:00"),       # naive UTC
        ("2024-01-01T07:55:00+00:00", "2024-01-01 07:55:00"),  # aware UTC
        ("2024-01-01T07:35:00-03:00", "2024-01-01 10:35:00"),  # aware SP
    ]
    for i, (ts, _exp) in enumerate(mix):
        aid = f"ID{i}"
        _write_snapshot(Path(eng.snapshot_dir), aid, ts)
        _write_replay_metric(Path(eng.replay_dir), aid)

    df = eng._load_data()
    assert len(df) == len(mix)
    # Nenhum timestamp válido perdido.
    assert df["timestamp"].isna().sum() == 0

    # Ordenação por instante correto: 06:45 (London) é o mais antigo, etc.
    expected_order = sorted(pd.Timestamp(e) for _t, e in mix)
    assert df["timestamp"].tolist() == expected_order

    # O instante de cada um é preservado (epoch igual ao do input).
    # Comparação por CONJUNTO de epochs (a df está ordenada por instante,
    # então a posição i não corresponde a mix[i]).
    epochs_in = {pd.Timestamp(ts).timestamp() for ts, _exp in mix}
    epochs_out = {pd.Timestamp(t).timestamp() for t in df["timestamp"]}
    assert epochs_in == epochs_out


# ===================================================================== #
#  Não-regressão: downstream (.dt accessors / relatório) continua ok      #
# ===================================================================== #
def test_downstream_temporal_analysis_works(tmp_path):
    """Com timestamps mistos, _temporal_analysis funciona (dropna + .dt)."""
    eng = _engine(tmp_path)
    mix = [
        ("2024-01-01T07:40:00", "A"),
        ("2024-02-01T07:45:00+01:00", "B"),
        ("2024-03-01T07:50:00", "C"),
    ]
    for i, (ts, _a) in enumerate(mix):
        aid = f"T{i}"
        _write_snapshot(Path(eng.snapshot_dir), aid, ts)
        _write_replay_metric(Path(eng.replay_dir), aid)

    df = eng._load_data()
    temporal = eng._temporal_analysis(df)
    assert "monthly" in temporal
    assert len(temporal["monthly"]) == 3  # 3 meses distintos preservados

    # Relatório completo não quebra com timestamps mistos.
    report = eng.generate_quality_report()
    assert report["status"] == "success"
    assert report["overview"]["date_range"]["start"] != ""
