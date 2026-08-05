import time
import logging


class LiveMonitor:
    """Stub - Monitor ao vivo (placeholder para V2)."""

    def __init__(self):
        self._running = False

    def start(self):
        self._running = True

    def stop(self):
        self._running = False

    @property
    def is_running(self) -> bool:
        return self._running
>>>>>>>>> Temporary merge branch 2
