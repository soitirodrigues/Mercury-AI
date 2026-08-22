"""M5 Operational Config — centralizada e explícita (Sprint 5).

Baseline validado Sprint 4 (promovido como oficial):
  - ProcessPool bounded workers=4 → ~105.47s completo (melhor geral)
  - ThreadPool bounded workers=4 → fallback estável (~173s)
  Default operacional: process_workers=4 (bounded ProcessPoolExecutor)

Não assumir que aumentar workers melhora — 16 degrada (thrashing).
Qualquer mudança de workers exige benchmark formal demonstrando superioridade.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any


@dataclass(frozen=True)
class M5OperationalConfig:
    # Workers
    process_workers: int = 4
    thread_workers: int = 4
    executor: str = "process"  # "process" | "thread"

    # Timeouts (segundos)
    worker_timeout_s: float = 90.0  # por ativo
    cycle_timeout_s: float = 290.0  # global do ciclo (M5 janela 300s)

    # Ciclo
    max_concurrent_cycles: int = 1  # nunca >1
    operational_universe: str = "ALL_SYMBOLS"  # ALL_SYMBOLS ou broker profile
    early_emission: bool = True
    freshness_policy: str = "strict"  # strict: never stale_as_fresh

    # Watchdog
    watchdog_interval_s: float = 5.0
    stall_threshold_s: float = 45.0  # sem progresso por X s = travado

    # Bounded queue
    bounded_queue_maxsize: int = 128

    # Retry/recovery
    max_retries_per_asset: int = 0  # 0 = sem retry automático (falha isolada)
    recreate_worker_on_error: bool = False  # future: process spawn recovery

    # Graceful shutdown
    shutdown_grace_s: float = 10.0

    # Rollback / feature flag
    use_operational_runner: bool = True  # False = rollback para MercuryScanner

    # Execution mode
    mode: str = "m5"  # m5 | manual | backtest

    @classmethod
    def from_env(cls) -> "M5OperationalConfig":
        """Override por env quando compatível (não altera defaults sem env set)."""
        def _int(k, default):
            v = os.environ.get(k)
            return int(v) if v is not None and v.strip() != "" else default

        def _float(k, default):
            v = os.environ.get(k)
            return float(v) if v is not None and v.strip() != "" else default

        def _bool(k, default):
            v = os.environ.get(k)
            if v is None:
                return default
            return v.strip().lower() in ("1", "true", "yes", "on")

        def _str(k, default):
            v = os.environ.get(k)
            return v.strip() if v is not None and v.strip() != "" else default

        return cls(
            process_workers=_int("M5_PROCESS_WORKERS", 4),
            thread_workers=_int("M5_THREAD_WORKERS", 4),
            executor=_str("M5_EXECUTOR", "process"),
            worker_timeout_s=_float("M5_WORKER_TIMEOUT_S", 90.0),
            cycle_timeout_s=_float("M5_CYCLE_TIMEOUT_S", 290.0),
            max_concurrent_cycles=_int("M5_MAX_CONCURRENT_CYCLES", 1),
            operational_universe=_str("M5_UNIVERSE", "ALL_SYMBOLS"),
            early_emission=_bool("M5_EARLY_EMISSION", True),
            freshness_policy=_str("M5_FRESHNESS_POLICY", "strict"),
            watchdog_interval_s=_float("M5_WATCHDOG_INTERVAL_S", 5.0),
            stall_threshold_s=_float("M5_STALL_THRESHOLD_S", 45.0),
            bounded_queue_maxsize=_int("M5_BOUNDED_QUEUE", 128),
            max_retries_per_asset=_int("M5_MAX_RETRIES", 0),
            recreate_worker_on_error=_bool("M5_RECREATE_WORKER", False),
            shutdown_grace_s=_float("M5_SHUTDOWN_GRACE_S", 10.0),
            use_operational_runner=_bool("M5_USE_OPERATIONAL_RUNNER", True),
            mode=_str("M5_MODE", "m5"),
        )

    def validate(self) -> None:
        assert 1 <= self.process_workers <= 16, "process_workers out of range"
        assert 1 <= self.thread_workers <= 16, "thread_workers out of range"
        assert self.executor in ("process", "thread"), "executor must be process|thread"
        assert self.max_concurrent_cycles == 1, "max_concurrent_cycles must be 1 (no overlap)"
        assert self.cycle_timeout_s <= 300, "cycle_timeout_s must be <= 300 (M5 window)"
        assert self.worker_timeout_s < self.cycle_timeout_s, "worker_timeout < cycle_timeout"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def workers_for_executor(self) -> int:
        return self.process_workers if self.executor == "process" else self.thread_workers


DEFAULT_M5_CONFIG = M5OperationalConfig()
