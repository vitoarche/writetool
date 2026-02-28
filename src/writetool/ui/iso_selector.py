"""ISO file selection widget with checksum display."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from writetool.i18n import on_language_changed, tr
from writetool.workers.checksum_worker import ChecksumWorker


class ISOSelector(QGroupBox):
    """Widget for selecting an ISO file and computing its checksum."""

    iso_selected = Signal(Path)  # Emitted when a valid ISO is chosen
    checksum_ready = Signal(str, str)  # (algorithm, digest)
    iso_type_detected = Signal(str)  # Emitted with detected ISO type

    def __init__(self, parent=None):
        super().__init__(tr("iso.group_title"), parent)
        self._iso_path: Path | None = None
        self._checksum_worker: ChecksumWorker | None = None
        self._setup_ui()
        on_language_changed(self.retranslate)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)

        # File path row
        path_row = QHBoxLayout()
        path_row.setSpacing(20)
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText(tr("iso.placeholder"))
        self._path_edit.setReadOnly(True)

        self._browse_btn = QPushButton(tr("iso.browse"))
        self._browse_btn.clicked.connect(self._on_browse)

        path_row.addWidget(self._path_edit, 1)
        path_row.addWidget(self._browse_btn)
        layout.addLayout(path_row)
        # Checksum label
        self._checksum_label = QLabel(tr("iso.checksum_none"))
        self._checksum_label.setObjectName("checksumLabel")
        layout.addWidget(self._checksum_label)

        # Verify row — same layout as path row
        verify_row = QHBoxLayout()
        verify_row.setSpacing(20)
        self._checksum_edit = QLineEdit()
        self._checksum_edit.setReadOnly(True)
        self._checksum_edit.setPlaceholderText("SHA256")

        self._verify_btn = QPushButton(tr("iso.verify"))
        self._verify_btn.setEnabled(False)
        self._verify_btn.clicked.connect(self._on_verify)

        verify_row.addWidget(self._checksum_edit, 1)
        verify_row.addWidget(self._verify_btn)
        layout.addLayout(verify_row)

    def retranslate(self):
        self.setTitle(tr("iso.group_title"))
        self._path_edit.setPlaceholderText(tr("iso.placeholder"))
        self._browse_btn.setText(tr("iso.browse"))
        self._verify_btn.setText(tr("iso.verify"))
        if not self._iso_path:
            self._checksum_label.setText(tr("iso.checksum_none"))

    def _on_browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("iso.file_dialog_title"),
            "",
            tr("iso.file_filter"),
        )
        if path:
            self.set_iso_path(Path(path))

    def set_iso_path(self, path: Path):
        """Set the ISO path and start background checksum."""
        self._iso_path = path
        self._path_edit.setText(str(path))
        self._verify_btn.setEnabled(True)
        self._checksum_label.setText(tr("iso.checksum_computing"))
        self._checksum_edit.clear()
        self.iso_selected.emit(path)

        # Start background checksum
        self._start_checksum()

    def get_iso_path(self) -> Path | None:
        return self._iso_path

    def _on_verify(self):
        if self._iso_path:
            self._start_checksum()

    def _start_checksum(self):
        if self._checksum_worker and self._checksum_worker.isRunning():
            self._checksum_worker.cancel()
            self._checksum_worker.wait()

        self._checksum_worker = ChecksumWorker(self._iso_path, "sha256", self)
        self._checksum_worker.checksum_ready.connect(self._on_checksum_done)
        self._checksum_worker.error.connect(self._on_checksum_error)
        self._checksum_worker.progress.connect(self._on_checksum_progress)
        self._checksum_worker.start()

    def _on_checksum_done(self, algorithm: str, digest: str):
        self._checksum_label.setText("SHA256:")
        self._checksum_edit.setText(digest)
        self._checksum_edit.setToolTip(digest)
        self.checksum_ready.emit(algorithm, digest)

    def _on_checksum_error(self, message: str):
        self._checksum_label.setText(tr("iso.checksum_error", message=message))
        self._checksum_edit.clear()

    def _on_checksum_progress(self, percent: float):
        self._checksum_label.setText(tr("iso.checksum_progress", percent=percent))
        self._checksum_edit.clear()
