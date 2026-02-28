"""Worker thread for USB drive scanning."""

from __future__ import annotations

from PySide6.QtCore import Signal

from writetool.i18n import tr
from writetool.platform.base import PlatformBackend
from writetool.workers.base_worker import BaseWorker


class ScanWorker(BaseWorker):
    """Scans for USB drives in a background thread."""

    # Emitted with the list of detected drives
    drives_found = Signal(list)

    def __init__(self, backend: PlatformBackend, parent=None):
        super().__init__(parent)
        self._backend = backend

    def run(self):
        try:
            self._emit_log(tr("scan.scanning"))
            drives = self._backend.list_usb_drives()
            self.drives_found.emit(drives)
            self._emit_log(tr("scan.found", count=len(drives)))
            self.finished_ok.emit()
        except Exception as e:
            self.error.emit(tr("scan.error", error=e))
