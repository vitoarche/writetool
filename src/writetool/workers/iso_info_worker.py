"""Worker thread for ISO analysis."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal

from writetool.core.iso_handler import ISOHandler, ISOInfo
from writetool.workers.base_worker import BaseWorker


class ISOInfoWorker(BaseWorker):
    """Runs ISO analysis in a background thread."""

    info_ready = Signal(object)  # Emits ISOInfo

    def __init__(self, iso_path: Path, parent=None):
        super().__init__(parent)
        self._iso_path = iso_path

    def run(self):
        try:
            with ISOHandler(self._iso_path) as handler:
                info = handler.get_info()
            self.info_ready.emit(info)
            self.finished_ok.emit()
        except Exception as e:
            self.error.emit(str(e))
