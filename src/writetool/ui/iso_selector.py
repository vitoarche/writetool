"""ISO file selection widget."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from writetool.i18n import on_language_changed, tr


class ISOSelector(QGroupBox):
    """Widget for selecting an ISO file."""

    iso_selected = Signal(Path)  # Emitted when a valid ISO is chosen
    iso_type_detected = Signal(str)  # Emitted with detected ISO type

    def __init__(self, parent=None):
        super().__init__(tr("iso.group_title"), parent)
        self._iso_path: Path | None = None
        self._setup_ui()
        on_language_changed(self.retranslate)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 12)

        path_row = QHBoxLayout()
        path_row.setSpacing(12)
        self._path_edit = QLineEdit()
        self._path_edit.setPlaceholderText(tr("iso.placeholder"))
        self._path_edit.setReadOnly(True)

        self._browse_btn = QPushButton(tr("iso.browse"))
        self._browse_btn.setFixedWidth(110)
        self._browse_btn.clicked.connect(self._on_browse)

        path_row.addWidget(self._path_edit, 1)
        path_row.addWidget(self._browse_btn)
        layout.addLayout(path_row)

    def retranslate(self):
        self.setTitle(tr("iso.group_title"))
        self._path_edit.setPlaceholderText(tr("iso.placeholder"))
        self._browse_btn.setText(tr("iso.browse"))

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
        """Set the ISO path."""
        self._iso_path = path
        self._path_edit.setText(str(path))
        self.iso_selected.emit(path)

    def get_iso_path(self) -> Path | None:
        return self._iso_path
