"""Worker thread for the USB write pipeline."""

from __future__ import annotations

from PySide6.QtCore import Signal

from writetool.core.exceptions import WriteCancelledError
from writetool.core.writer_engine import WriteConfig, WriteProgress, WriterEngine
from writetool.i18n import tr
from writetool.platform.base import PlatformBackend
from writetool.workers.base_worker import BaseWorker


class WriteWorker(BaseWorker):
    """Runs the full write pipeline in a background thread."""

    # Emitted with (stage, current_file)
    stage_changed = Signal(str, str)

    # Emitted when the operation is cancelled by the user
    cancelled = Signal()

    def __init__(self, backend: PlatformBackend, config: WriteConfig, parent=None):
        super().__init__(parent)
        self._backend = backend
        self._config = config
        self._engine: WriterEngine | None = None

    def cancel(self) -> None:
        super().cancel()
        if self._engine:
            self._engine.cancel()

    def run(self):
        try:
            self._engine = WriterEngine(
                backend=self._backend,
                progress_callback=self._on_progress,
                log_callback=self._on_log,
            )

            self._engine.write(self._config)
            self.finished_ok.emit()

        except WriteCancelledError:
            self._emit_log(tr("write.cancelled"))
            self.cancelled.emit()

        except Exception as e:
            self.error.emit(str(e))

    def _on_progress(self, p: WriteProgress):
        self._emit_progress(p.percent)
        self.stage_changed.emit(p.stage_label, p.current_file)

    def _on_log(self, message: str):
        self._emit_log(message)
