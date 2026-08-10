"""Probe B5 — ReplayStorage integrity tests (non-destructive, uses temp output_dir).

Cria replays sintéticos e usa `ReplayStorage.save` para verificar colisões,
sobrescrita e contagem de audit_ids.

Não altera código de produção. Artefatos escritos em `tmp/b5_replay`.
"""
from __future__ import annotations

import hashlib
import json
import os
import random
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from mercury_ai.database.replay_storage import ReplayStorage, ReplayMetrics


def compute_audit_id(asset: str, timeframe: str, evidences_count: int) -> str:
    s = f"{asset}{timeframe}{evidences_count}"
    return hashlib.sha256(s.encode()).hexdigest()


@dataclass
class FakeDecisionResult:
    decision: str
    confidence: float
    audit_id: str


@dataclass
class FakeSnapshot:
    decision_result: FakeDecisionResult
    timestamp: str


def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)


def read_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def controlled_collision_test(out_dir: str) -> Tuple[bool, str]:
    """Salva duas entradas com mesmo audit_id mas conteúdo diferente.
    Retorna (colisao_confirmada, mensagem).
    """
    storage = ReplayStorage(output_dir=out_dir)
    asset = "BTC-USD"
    timeframe = "M15"
    evidences_count = 10
    aid = compute_audit_id(asset, timeframe, evidences_count)

    snap_a = FakeSnapshot(
        decision_result=FakeDecisionResult(decision="BUY", confidence=0.8, audit_id=aid),
        timestamp="2026-08-10T00:00:00",
    )
    metrics_a = ReplayMetrics(mae=0.01, mfe=0.05, pl=0.02, hit=True)

    snap_b = FakeSnapshot(
        decision_result=FakeDecisionResult(decision="SELL", confidence=0.4, audit_id=aid),
        timestamp="2026-08-10T01:00:00",
    )
    metrics_b = ReplayMetrics(mae=-0.02, mfe=0.03, pl=-0.015, hit=False)

    # Save A then B
    storage.save(aid, snap_a, metrics_a)
    storage.save(aid, snap_b, metrics_b)

    path = os.path.join(out_dir, f"{aid}.json")
    if not os.path.exists(path):
        return False, f"Arquivo esperado não encontrado: {path}"

    data = read_json(path)
    # If file reflects B, overwrite occurred
    if data.get("decision") == snap_b.decision_result.decision and data.get("timestamp") == snap_b.timestamp:
        return True, "Sobrescrita detectada: último save prevaleceu (B sobre A)."
    else:
        return False, "Arquivo não reflete último save — comportamento inesperado (talvez versioning presente)."


def bulk_replays_test(out_dir: str, N: int) -> Dict[str, int]:
    storage = ReplayStorage(output_dir=out_dir)
    assets = ["BTC-USD", "ETH-USD", "XRP-USD", "TEST-1"]
    timeframes = ["M1", "M5", "M15", "H1"]

    audit_counts: Dict[str, int] = {}

    for i in range(N):
        asset = random.choice(assets)
        tf = random.choice(timeframes)
        evidences_count = random.randint(5, 15)
        aid = compute_audit_id(asset, tf, evidences_count)

        snap = FakeSnapshot(
            decision_result=FakeDecisionResult(decision=random.choice(["BUY","SELL","WAIT"]), confidence=random.random(), audit_id=aid),
            timestamp=f"2026-08-10T00:00:{i:02d}",
        )
        metrics = ReplayMetrics(mae=random.uniform(-0.1, 0.1), mfe=random.uniform(-0.1, 0.1), pl=random.uniform(-0.2, 0.2), hit=bool(random.getrandbits(1)))
        storage.save(aid, snap, metrics)
        audit_counts[aid] = audit_counts.get(aid, 0) + 1

    return audit_counts


def targeted_collision(out_dir: str) -> Tuple[bool, str]:
    # Deliberadamente cria A e B com mesmo asset/timeframe/len(evidences)
    storage = ReplayStorage(output_dir=out_dir)
    asset = "BTC-USD"
    timeframe = "M15"
    evidences_count = 10
    aid = compute_audit_id(asset, timeframe, evidences_count)

    # dataset A
    snap_a = FakeSnapshot(
        decision_result=FakeDecisionResult(decision="BUY", confidence=0.9, audit_id=aid),
        timestamp="2026-08-10T10:00:00",
    )
    metrics_a = ReplayMetrics(mae=0.01, mfe=0.05, pl=0.03, hit=True)

    # dataset B (completamente diferente internamente)
    snap_b = FakeSnapshot(
        decision_result=FakeDecisionResult(decision="WAIT", confidence=0.1, audit_id=aid),
        timestamp="2026-08-11T15:00:00",
    )
    metrics_b = ReplayMetrics(mae=-0.2, mfe=0.3, pl=-0.1, hit=False)

    storage.save(aid, snap_a, metrics_a)
    storage.save(aid, snap_b, metrics_b)

    path = os.path.join(out_dir, f"{aid}.json")
    data = read_json(path)
    collided = data.get("timestamp") == snap_b.timestamp and data.get("decision") == snap_b.decision_result.decision
    return collided, f"audit_id={aid} file at {path}"


def main():
    out_dir = os.path.join("tmp", "b5_replay")
    ensure_dir(out_dir)

    print("[B5] OUT_DIR:", out_dir)

    print("\n[1] Teste de colisão controlada")
    col, msg = controlled_collision_test(out_dir)
    print("   Resultado:", col, "-", msg)

    print("\n[2] Teste direcionado de colisão")
    c2, info = targeted_collision(out_dir)
    print("   Colisão deliberada detectada:", c2, "-", info)

    for N in (100, 500, 1000):
        print(f"\n[3] Teste bulk: N={N}")
        counts = bulk_replays_test(out_dir, N)
        total = sum(counts.values())
        uniques = len(counts)
        duplicates = total - uniques
        print(f"   total={total} unique_audit_ids={uniques} duplicates={duplicates}")
        # write summary
        with open(os.path.join(out_dir, f"summary_{N}.json"), "w", encoding="utf-8") as f:
            json.dump({"total": total, "unique": uniques, "duplicates": duplicates}, f, indent=2)

    print("\n[B5] Probe finalizado. Artefatos em:", out_dir)


if __name__ == "__main__":
    main()
