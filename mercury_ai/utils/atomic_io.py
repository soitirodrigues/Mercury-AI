"""
Atomic JSON write utility for Mercury-AI.

Provides crash-safe JSON persistence by writing to a temporary file first,
then atomically replacing the target file via os.replace(). Includes retry
with exponential backoff to handle transient OS-level locking issues
(common on Windows during concurrent access).

This is the canonical pattern for all JSON persistence in Mercury-AI,
extracted from the reference implementation in
``mercury_ai.analysis.institutional_memory_engine.InstitutionalMemoryEngine.flush()``.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
import time
from typing import Any

logger = logging.getLogger(__name__)

__all__ = ["atomic_json_write"]


def atomic_json_write(
    path: str,
    data: Any,
    *,
    indent: int = 4,
    max_retries: int = 5,
    backoff_base: float = 0.05,
    default: Any = None,
) -> None:
    """Write *data* as JSON to *path* atomically.

    The data is first serialized to a temporary file (``{path}.tmp``), then
    ``os.replace()`` is used to atomically swap it into place. If the
    replace fails with an ``OSError`` (e.g. transient lock on Windows),
    the operation is retried with exponential backoff.

    Parameters
    ----------
    path:
        Destination file path.
    data:
        Python object to serialize as JSON.
    indent:
        JSON indentation level (default 4).
    max_retries:
        Maximum number of ``os.replace`` attempts (default 5).
    backoff_base:
        Base delay in seconds for exponential backoff
        (default 0.05 → 0.05, 0.1, 0.2, 0.4, ...).
    default:
        Optional ``default`` callable/object passed to ``json.dump``
        for non-serializable values (e.g. ``default=str``).

    Raises
    ------
    OSError
        If all retry attempts fail.
    """
    # Ensure parent directory exists
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # Serialize to temp file first
    dump_kwargs: dict = {"indent": indent}
    if default is not None:
        dump_kwargs["default"] = default

    # Each call gets a UNIQUE temp file via tempfile.mkstemp() to avoid
    # collisions when multiple threads write to the same destination path
    # concurrently (Windows WinError 32 on shared .json.tmp). The retry
    # loop handles transient OSError on os.replace().
    last_exc: Exception | None = None
    for attempt in range(max_retries):
        fd = -1
        temp_path = None
        try:
            # Create a unique temp file in the same directory as the target
            # (required for os.replace to work atomically on the same volume).
            fd, temp_path = tempfile.mkstemp(
                dir=parent or ".",
                prefix=".tmp_",
                suffix=".json",
            )
            os.close(fd)
            fd = -1  # mark as closed

            with open(temp_path, "w", encoding="utf-8") as f:
                json.dump(data, f, **dump_kwargs)
                f.flush()
                os.fsync(f.fileno())
            os.replace(temp_path, path)
            return
        except (OSError, PermissionError) as e:
            last_exc = e
            # Clean up this attempt's temp file
            if temp_path is not None:
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
            if attempt == max_retries - 1:
                logger.error(
                    "atomic_json_write: failed to write %s after %d attempts: %s",
                    path,
                    max_retries,
                    e,
                    exc_info=True,
                )
                raise
            time.sleep(backoff_base * (2 ** attempt))
    # Should never reach here, but satisfy type checkers
    if last_exc:
        raise last_exc
