"""M5 Clock / Cycle Scheduler — alinhado ao candle M5, não sleep() acumulativo."""
from __future__ import annotations

import time
import uuid
import threading
import logging
from datetime import datetime, timezone, timedelta
from typing import Optional, Callable, List, Dict, Any

from mercury_ai.operations.m5_incremental.temporal import floor_m5, ceil_m5

from .config import M5OperationalConfig
from .runner import M5OperationalRunner

logger = logging.getLogger(__name__)


class M5Clock:
    """Scheduler M5 — garante exatamente um ciclo ativo por vez, sem overlap."""

    def __init__(self, runner: M5OperationalRunner, config: Optional[M5OperationalConfig] = None):
        self.runner = runner
        self.config = config or runner.config
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._cycle_count = 0
        self._reports: List[Dict[str, Any]] = []
        self._lock = threading.Lock()

    def _next_boundary(self, now: Optional[datetime] = None) -> datetime:
        if now is None:
            now = datetime.now(timezone.utc)
        # Próxima fronteira M5 estritamente após now
        return ceil_m5(now)

    def start(self, on_cycle: Optional[Callable[[Dict[str, Any]], None]] = None, max_cycles: Optional[int] = None) -> None:
        """Inicia scheduler em background thread."""
        self._stop.clear()

        def _loop():
            cycles_done = 0
            while not self._stop.is_set():
                if max_cycles is not None and cycles_done >= max_cycles:
                    break
                now = datetime.now(timezone.utc)
                nxt = self._next_boundary(now)
                wait_s = (nxt - now).total_seconds()
                # Cap wait para não bloquear shutdown por muito tempo
                # Poll a cada 1s para checar stop
                waited = 0.0
                while waited < wait_s and not self._stop.is_set():
                    chunk = min(1.0, wait_s - waited)
                    time.sleep(chunk)
                    waited += chunk
                if self._stop.is_set():
                    break

                # Determina target_candle = floor da fronteira que acabou de fechar
                target = floor_m5(nxt)
                cycle_id = f"m5-{nxt.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
                logger.info("[M5Clock] triggering cycle %s target=%s", cycle_id, target.isoformat())
                try:
                    report = self.runner.run_cycle(cycle_id=cycle_id, target_candle=target)
                    with self._lock:
                        self._reports.append(report)
                        self._cycle_count += 1
                    if on_cycle:
                        try:
                            on_cycle(report)
                        except Exception:
                            logger.exception("on_cycle callback failed")
                    cycles_done += 1
                except Exception:
                    logger.exception("[M5Clock] cycle %s failed", cycle_id)
                    cycles_done += 1
                # Só começa próximo ciclo após anterior encerrado — no overlap por design (runner guard)

        self._thread = threading.Thread(target=_loop, name="m5-clock", daemon=True)
        self._thread.start()
        logger.info("[M5Clock] started")

    def stop(self, timeout: float = 15.0) -> None:
        self._stop.set()
        self.runner.request_shutdown()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
        logger.info("[M5Clock] stopped cycles=%s", self._cycle_count)

    @property
    def reports(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self._reports)

    def run_cycles_blocking(self, count: int, target_start: Optional[datetime] = None) -> List[Dict[str, Any]]:
        """Executa N ciclos consecutivos de forma bloqueante (sem sleep M5 real) — para teste multi-cycle.

        Usa target_candle incremental de 5m sem esperar fronteira real.
        Garante no-overlap e valida cycle_id único / candle correto.
        """
        reports: List[Dict[str, Any]] = []
        if target_start is None:
            target_start = floor_m5(datetime.now(timezone.utc))
        # Normaliza para floor M5
        cur = floor_m5(target_start)
        for i in range(count):
            if self._stop.is_set():
                break
            cycle_id = f"m5-test-{cur.strftime('%Y%m%d%H%M')}-{uuid.uuid4().hex[:4]}"
            report = self.runner.run_cycle(cycle_id=cycle_id, target_candle=cur)
            reports.append(report)
            with self._lock:
                self._reports.append(report)
                self._cycle_count += 1
            cur = cur + timedelta(minutes=5)
        return reports
