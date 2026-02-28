"""Base QThread worker with common signals."""

from __future__ import annotations

from PySide6.QtCore import QThread, Signal


class BaseWorker(QThread):
    """Base worker thread with standard signals."""

    # Emitted with (message,)
    log = Signal(str)

    # Emitted with (percent,) 0-100
    progress = Signal(float)

    # Emitted on successful completion
    finished_ok = Signal()

    # Emitted with error message on failure
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._cancelled = False

    def cancel(self) -> None:
        """Request cancellation."""
        self._cancelled = True

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    def run(self):
        """Override in subclasses. Must call _check_cancel() periodically."""
        raise NotImplementedError

    def _check_cancel(self) -> bool:
        """Returns True if cancelled."""
        return self._cancelled

    def _emit_log(self, message: str):
        self.log.emit(message)

    def _emit_progress(self, percent: float):
        self.progress.emit(min(100.0, max(0.0, percent)))
