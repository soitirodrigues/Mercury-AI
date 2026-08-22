"""Watchdog operacional — detecta ciclo/worker travado sem criar ciclos duplicados."""
from __future__ import annotations

import time
import threading
import logging
from dataclasses import dataclass, field
from typing import Optional, Callable

logger = logging.getLogger(__name__)


@dataclass
class WatchdogEvent:
    kind: str  # STALL | TIMEOUT | WORKER_DIED | QUEUE_STALLED
    message: str
    elapsed_s: float
    cycle_id: str


class CycleWatchdog:
    """Watchdog que monitora progresso sem iniciar novo ciclo.

    Usa threading.Timer polling a cada interval_s.
    Callback on_stall recebe WatchdogEvent e deve fazer recovery seguro
    (cancelar/isolated, nunca iniciar novo ciclo).
    """

    def __init__(
        self,
        cycle_id: str,
        interval_s: float = 5.0,
        stall_threshold_s: float = 45.0,
        on_event: Optional[Callable[[WatchdogEvent], None]] = None,
    ):
        self.cycle_id = cycle_id
        self.interval_s = interval_s
        self.stall_threshold_s = stall_threshold_s
        self.on_event = on_event
        self._stop = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._last_progress_t = time.monotonic()
        self._start_t = time.monotonic()
        self._lock = threading.Lock()
        self._completed = 0
        self._total = 0
        self._fired_stall = False

    def set_total(self, n: int) -> None:
        with self._lock:
            self._total = n

    def notify_progress(self, completed: int) -> None:
        with self._lock:
            if completed != self._completed:
                self._completed = completed
                self._last_progress_t = time.monotonic()
                self._fired_stall = False

    def _loop(self) -> None:
        while not self._stop.wait(self.interval_s):
            now = time.monotonic()
            with self._lock:
                completed = self._completed
                total = self._total
                last = self._last_progress_t
                stalled_for = now - last
                elapsed = now - self._start_t
            # Detectar stall: sem progresso por threshold
            if completed < total and stalled_for >= self.stall_threshold_s and not self._fired_stall:
                with self._lock:
                    self._fired_stall = True
                evt = WatchdogEvent(
                    kind="STALL",
                    message=f"no progress for {stalled_for:.1f}s ({completed}/{total} completed)",
                    elapsed_s=elapsed,
                    cycle_id=self.cycle_id,
                )
                logger.warning("[Watchdog %s] STALL: %s", self.cycle_id, evt.message)
                if self.on_event:
                    try:
                        self.on_event(evt)
                    except Exception:
                        logger.exception("watchdog on_event failed")

    def start(self) -> None:
        self._start_t = time.monotonic()
        self._last_progress_t = self._start_t
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name=f"m5-watchdog-{self.cycle_id}", daemon=True)
        self._thread.start()
        logger.info("[Watchdog %s] started interval=%.1fs stall=%.1fs", self.cycle_id, self.interval_s, self.stall_threshold_s)

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        logger.info("[Watchdog %s] stopped", self.cycle_id)
