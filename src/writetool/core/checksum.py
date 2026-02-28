"""Checksum calculation with progress callbacks."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Callable

from writetool.utils.constants import CHECKSUM_BUFFER_SIZE


def compute_checksum(
    file_path: Path,
    algorithm: str = "sha256",
    progress_callback: Callable[[int, int], None] | None = None,
    cancel_check: Callable[[], bool] | None = None,
) -> str:
    """Compute a file's checksum.

    Args:
        file_path: Path to the file.
        algorithm: 'sha256' or 'md5'.
        progress_callback: Called with (bytes_read, total_bytes).
        cancel_check: Called periodically; if it returns True, abort.

    Returns:
        Hex digest string.
    """
    h = hashlib.new(algorithm)
    total = file_path.stat().st_size
    read_bytes = 0

    with open(file_path, "rb") as f:
        while True:
            if cancel_check and cancel_check():
                return ""

            chunk = f.read(CHECKSUM_BUFFER_SIZE)
            if not chunk:
                break

            h.update(chunk)
            read_bytes += len(chunk)

            if progress_callback:
                progress_callback(read_bytes, total)

    return h.hexdigest()
