"""Worker thread for USB drive scanning."""

from __future__ import annotations

from PySide6.QtCore import Signal

from writetool.platform.base import DriveInfo, PlatformBackend
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
            self._emit_log("USB sürücüler taranıyor...")
            drives = self._backend.list_usb_drives()
            self.drives_found.emit(drives)
            self._emit_log(f"{len(drives)} USB sürücü bulundu.")
            self.finished_ok.emit()
        except Exception as e:
            self.error.emit(f"USB tarama hatası: {e}")
