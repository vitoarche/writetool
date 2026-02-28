"""USB drive selection widget."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from writetool.i18n import on_language_changed, tr
from writetool.platform.base import DriveInfo, PlatformBackend
from writetool.workers.scan_worker import ScanWorker


class DriveSelector(QGroupBox):
    """Widget for selecting a USB drive."""

    drive_selected = Signal(object)  # Emitted with DriveInfo or None

    def __init__(self, backend: PlatformBackend, parent=None):
        super().__init__(tr("drive.group_title"), parent)
        self._backend = backend
        self._drives: list[DriveInfo] = []
        self._scan_worker: ScanWorker | None = None
        self._setup_ui()
        on_language_changed(self.retranslate)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        row = QHBoxLayout()
        row.setSpacing(20)
        self._combo = QComboBox()
        self._combo.setMinimumWidth(300)
        self._combo.currentIndexChanged.connect(self._on_selection_changed)

        self._refresh_btn = QPushButton(tr("drive.refresh"))
        self._refresh_btn.clicked.connect(self.refresh)

        row.addWidget(self._combo, 1)
        row.addWidget(self._refresh_btn)
        layout.addLayout(row)

        self._status_label = QLabel("")
        self._status_label.setObjectName("statusLabel")
        layout.addWidget(self._status_label)

    def retranslate(self):
        self.setTitle(tr("drive.group_title"))
        self._refresh_btn.setText(tr("drive.refresh"))
        # Re-populate combo text for current state
        if not self._drives:
            if self._combo.count() > 0:
                current_text = self._combo.itemText(0)
                if current_text:
                    # Keep scanning/error states, update empty state
                    self._combo.setItemText(0, tr("drive.not_found"))
                    self._status_label.setText(tr("drive.not_found_hint"))
        else:
            self._status_label.setText(tr("drive.found_count", count=len(self._drives)))

    def refresh(self):
        """Scan for USB drives."""
        self._combo.clear()
        self._combo.addItem(tr("drive.scanning"))
        self._combo.setEnabled(False)
        self._refresh_btn.setEnabled(False)

        self._scan_worker = ScanWorker(self._backend, self)
        self._scan_worker.drives_found.connect(self._on_drives_found)
        self._scan_worker.error.connect(self._on_scan_error)
        self._scan_worker.start()

    def get_selected_drive(self) -> DriveInfo | None:
        """Return the currently selected drive, or None."""
        idx = self._combo.currentIndex()
        if 0 <= idx < len(self._drives):
            return self._drives[idx]
        return None

    def _on_drives_found(self, drives: list[DriveInfo]):
        self._drives = drives
        self._combo.blockSignals(True)
        self._combo.clear()
        self._combo.setEnabled(True)
        self._refresh_btn.setEnabled(True)

        if not drives:
            self._combo.addItem(tr("drive.not_found"))
            self._status_label.setText(tr("drive.not_found_hint"))
            self._combo.blockSignals(False)
            self.drive_selected.emit(None)
        else:
            for d in drives:
                self._combo.addItem(d.display_name)
            self._status_label.setText(tr("drive.found_count", count=len(drives)))
            self._combo.blockSignals(False)
            self.drive_selected.emit(drives[0])

    def _on_scan_error(self, message: str):
        self._combo.blockSignals(True)
        self._combo.clear()
        self._combo.addItem(tr("drive.scan_error"))
        self._combo.setEnabled(True)
        self._refresh_btn.setEnabled(True)
        self._status_label.setText(message)
        self._combo.blockSignals(False)
        self.drive_selected.emit(None)

    def _on_selection_changed(self, index: int):
        if 0 <= index < len(self._drives):
            self.drive_selected.emit(self._drives[index])
        else:
            self.drive_selected.emit(None)
