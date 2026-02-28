"""Progress bar and log panel widget."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGroupBox,
    QLabel,
    QProgressBar,
    QTextEdit,
    QVBoxLayout,
)


class ProgressPanel(QGroupBox):
    """Widget showing write progress and log output."""

    def __init__(self, parent=None):
        super().__init__("İlerleme", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Progress bar
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFormat("%p%")
        layout.addWidget(self._progress_bar)

        # Status label
        self._status_label = QLabel("")
        self._status_label.setObjectName("statusLabel")
        layout.addWidget(self._status_label)

        # Log output
        self._log_edit = QTextEdit()
        self._log_edit.setObjectName("logPanel")
        self._log_edit.setReadOnly(True)
        self._log_edit.setMaximumHeight(150)
        layout.addWidget(self._log_edit)

    def set_progress(self, percent: float):
        """Set progress bar value (0-100)."""
        self._progress_bar.setValue(int(percent))

    def set_status(self, text: str):
        """Set the status label text."""
        self._status_label.setText(text)

    def append_log(self, message: str):
        """Append a line to the log panel."""
        self._log_edit.append(f"[LOG] {message}")
        # Auto-scroll to bottom
        scrollbar = self._log_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def reset(self):
        """Clear progress and log."""
        self._progress_bar.setValue(0)
        self._status_label.setText("")
        self._log_edit.clear()
