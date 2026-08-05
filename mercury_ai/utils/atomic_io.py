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
    temp_path = f"{path}.tmp"

    # Ensure parent directory exists
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # Serialize to temp file first
    dump_kwargs: dict = {"indent": indent}
    if default is not None:
        dump_kwargs["default"] = default

    with open(temp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, **dump_kwargs)
        f.flush()
        os.fsync(f.fileno())

    # Atomic replace with retry + exponential backoff
    # On Windows, antivirus/Defender can delete the .tmp file between
    # open() and os.replace(), so we re-create it on each retry if needed.
    for attempt in range(max_retries):
        try:
            os.replace(temp_path, path)
            return
        except OSError as e:
            if attempt == max_retries - 1:
                logger.error(
                    "atomic_json_write: failed to replace %s after %d attempts: %s",
                    path,
                    max_retries,
                    e,
                    exc_info=True,
                )
                # Clean up temp file on final failure
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
                raise
            time.sleep(backoff_base * (2 ** attempt))
            # Re-create temp file if it was deleted (e.g. by antivirus)
            if not os.path.exists(temp_path):
                with open(temp_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, **dump_kwargs)
                    f.flush()
                    os.fsync(f.fileno())
