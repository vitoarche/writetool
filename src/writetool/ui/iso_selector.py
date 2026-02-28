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

from writetool.utils.formatting import truncate_hash
from writetool.workers.checksum_worker import ChecksumWorker


class ISOSelector(QGroupBox):
    """Widget for selecting an ISO file and computing its checksum."""

    iso_selected = Signal(Path)  # Emitted when a valid ISO is chosen
    checksum_ready = Signal(str, str)  # (algorithm, digest)

    def __init__(self, parent=None):
        super().__init__("ISO Dosyası", parent)
        self._iso_path: Path | None = None
        self._checksum_worker: ChecksumWorker | None = None
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # File path row
        path_row = QHBoxLayout()
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText("Windows ISO dosyasını seçin...")
        self._path_edit.setReadOnly(True)

        self._browse_btn = QPushButton("Gözat...")
        self._browse_btn.clicked.connect(self._on_browse)

        path_row.addWidget(self._path_edit, 1)
        path_row.addWidget(self._browse_btn)
        layout.addLayout(path_row)

        # Checksum row
        checksum_row = QHBoxLayout()
        self._checksum_label = QLabel("SHA256: —")
        self._checksum_label.setObjectName("checksumLabel")

        self._verify_btn = QPushButton("Doğrula")
        self._verify_btn.setEnabled(False)
        self._verify_btn.clicked.connect(self._on_verify)

        checksum_row.addWidget(self._checksum_label, 1)
        checksum_row.addWidget(self._verify_btn)
        layout.addLayout(checksum_row)

    def _on_browse(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "ISO Dosyası Seç",
            "",
            "ISO Dosyaları (*.iso);;Tüm Dosyalar (*)",
        )
        if path:
            self.set_iso_path(Path(path))

    def set_iso_path(self, path: Path):
        """Set the ISO path and start background checksum."""
        self._iso_path = path
        self._path_edit.setText(str(path))
        self._verify_btn.setEnabled(True)
        self._checksum_label.setText("SHA256: hesaplanıyor...")
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
        self._checksum_label.setText(f"SHA256: {truncate_hash(digest, 24)}")
        self._checksum_label.setToolTip(digest)
        self.checksum_ready.emit(algorithm, digest)

    def _on_checksum_error(self, message: str):
        self._checksum_label.setText(f"SHA256: hata — {message}")

    def _on_checksum_progress(self, percent: float):
        self._checksum_label.setText(f"SHA256: hesaplanıyor... {percent:.0f}%")
