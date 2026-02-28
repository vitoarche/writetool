"""Worker thread for checksum calculation."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from writetool.core.checksum import compute_checksum
from writetool.workers.base_worker import BaseWorker


class ChecksumWorker(BaseWorker):
    """Computes file checksum in a background thread."""

    # Emitted with (algorithm, hex_digest)
    checksum_ready = Signal(str, str)

    def __init__(self, file_path: Path, algorithm: str = "sha256", parent=None):
        super().__init__(parent)
        self._file_path = file_path
        self._algorithm = algorithm

    def run(self):
        try:
            self._emit_log(f"{self._algorithm.upper()} hesaplanıyor...")

            def on_progress(read_bytes: int, total: int):
                if total > 0:
                    self._emit_progress(read_bytes / total * 100)

            digest = compute_checksum(
                self._file_path,
                algorithm=self._algorithm,
                progress_callback=on_progress,
                cancel_check=lambda: self._cancelled,
            )

            if self._cancelled:
                self._emit_log("Checksum hesaplama iptal edildi.")
                return

            self.checksum_ready.emit(self._algorithm, digest)
            self._emit_log(f"{self._algorithm.upper()}: {digest}")
            self.finished_ok.emit()
        except Exception as e:
            self.error.emit(f"Checksum hatası: {e}")
