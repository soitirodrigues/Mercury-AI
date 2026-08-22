"""replay_fingerprint — dataset/config fingerprint para auditoria S7.1 (RISK-006).

Fornece hashes determinísticos para provar que dois replays rodaram sobre
exatamente os mesmos dados e pesos.

- dataset_hash: sha256 do conteúdo OHLCV normalizado (CSV com float_format fixo)
- config_hash : sha256 de INSTITUTIONAL_WEIGHTS + VersionMetadata

Contrato: ambos são opcionais em DecisionSnapshot/ReplayStorage (dict.get),
portanto snapshots antigos sem campo continuam válidos.
"""

from __future__ import annotations

import hashlib
import json
from typing import Dict, Any, Optional

import pandas as pd


def compute_dataset_hash(df: pd.DataFrame) -> str:
    """Hash determinístico do DataFrame OHLCV.

    Normaliza:
    - index serializado via to_csv (inclui timestamps ISO)
    - colunas na ordem canônica open/high/low/close/volume quando presentes,
      senão ordem sortada para determinismo
    - float_format='%.10f' para estabilidade cross-platform
    - line_terminator='\\n'

    Retorna hex sha256 (64 chars). DataFrame vazio retorna sha256(b"").
    """
    if df is None or df.empty:
        return hashlib.sha256(b"").hexdigest()
    # Ordem canônica para OHLCV; fallback sorted para DFs arbitrários
    canonical = ["open", "high", "low", "close", "volume"]
    cols = [c for c in canonical if c in df.columns]
    remaining = sorted([c for c in df.columns if c not in cols])
    ordered_cols = cols + remaining
    df_ordered = df[ordered_cols] if ordered_cols else df
    # to_csv é determinístico quando fixamos float_format e line_terminator
    try:
        csv_str = df_ordered.to_csv(index=True, float_format="%.10f", lineterminator="\n")
    except TypeError:
        # pandas < compat fallback
        csv_str = df_ordered.to_csv(index=True, float_format="%.10f")
    return hashlib.sha256(csv_str.encode("utf-8")).hexdigest()


def compute_config_hash(
    weights: Optional[Dict[str, Any]] = None,
    version_metadata: Optional[Any] = None,
) -> str:
    """Hash determinístico da configuração de pesos + versão.

    Se weights/version_metadata forem None, lê dos singletons canônicos:
    - mercury_ai.config.institutional_weights.INSTITUTIONAL_WEIGHTS
    - mercury_ai.models.version_metadata.VersionMetadata (ou settings.VERSION)

    Serializa via json.dumps(sort_keys=True, separators=(',', ':')) para
    determinismo.
    """
    if weights is None:
        try:
            from mercury_ai.config.institutional_weights import INSTITUTIONAL_WEIGHTS
            weights = INSTITUTIONAL_WEIGHTS
        except Exception:
            weights = {}
    if version_metadata is None:
        try:
            from mercury_ai.config import settings
            version_metadata = {"version": getattr(settings, "VERSION", "unknown")}
        except Exception:
            version_metadata = {"version": "unknown"}
    else:
        # Se for dataclass, converte para dict
        if hasattr(version_metadata, "__dataclass_fields__"):
            import dataclasses
            version_metadata = dataclasses.asdict(version_metadata)
        elif not isinstance(version_metadata, dict):
            version_metadata = {"version": str(version_metadata)}

    payload = {
        "weights": weights,
        "version_metadata": version_metadata,
    }
    # sort_keys garante ordem determinística; separators remove whitespace variável
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def compute_fingerprints(
    df: pd.DataFrame,
    weights: Optional[Dict[str, Any]] = None,
    version_metadata: Optional[Any] = None,
) -> Dict[str, str]:
    """Conveniência: retorna {dataset_hash, config_hash}."""
    return {
        "dataset_hash": compute_dataset_hash(df),
        "config_hash": compute_config_hash(weights, version_metadata),
    }
