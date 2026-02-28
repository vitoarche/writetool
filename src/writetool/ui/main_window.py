"""Main application window."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from writetool.core.writer_engine import WriteConfig
from writetool.i18n import on_language_changed, tr
from writetool.platform.base import DriveInfo, PlatformBackend
from writetool.ui.dialogs import confirm_write, show_error, show_success
from writetool.ui.drive_selector import DriveSelector
from writetool.ui.iso_selector import ISOSelector
from writetool.ui.progress_panel import ProgressPanel
from writetool.ui.settings_panel import SettingsPanel
from writetool.utils.constants import APP_TITLE, ISO_TYPE_LINUX, ISO_TYPE_MACOS, ISO_TYPE_UNKNOWN, ISO_TYPE_WINDOWS
from writetool.workers.iso_info_worker import ISOInfoWorker
from writetool.workers.write_worker import WriteWorker


class MainWindow(QMainWindow):
    """Main application window for WriteTool."""

    def __init__(self, backend: PlatformBackend, parent=None):
        super().__init__(parent)
        self._backend = backend
        self._write_worker: WriteWorker | None = None
        self._iso_info_worker: ISOInfoWorker | None = None
        self._selected_drive: DriveInfo | None = None
        self._iso_path: Path | None = None
        self._iso_type: str = ISO_TYPE_UNKNOWN
        self._setup_ui()
        self._connect_signals()
        on_language_changed(self.retranslate)

        # Initial USB scan
        self._drive_selector.refresh()

    def _setup_ui(self):
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(620, 560)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(20, 16, 20, 16)
        main_layout.setSpacing(12)

        # Title
        title = QLabel(APP_TITLE)
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # ISO Selector
        self._iso_selector = ISOSelector()
        main_layout.addWidget(self._iso_selector)

        # Drive Selector
        self._drive_selector = DriveSelector(self._backend)
        main_layout.addWidget(self._drive_selector)

        # Settings
        self._settings_panel = SettingsPanel()
        main_layout.addWidget(self._settings_panel)

        # Progress
        self._progress_panel = ProgressPanel()
        main_layout.addWidget(self._progress_panel)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self._start_btn = QPushButton(tr("main.start_button"))
        self._start_btn.setObjectName("startButton")
        self._start_btn.setEnabled(False)

        self._cancel_btn = QPushButton(tr("main.cancel_button"))
        self._cancel_btn.setObjectName("cancelButton")
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.setVisible(False)

        btn_layout.addWidget(self._start_btn)
        btn_layout.addSpacing(16)
        btn_layout.addWidget(self._cancel_btn)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # Author label (bottom-right)
        author_label = QLabel("author: arche")
        author_label.setObjectName("authorLabel")
        author_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        main_layout.addWidget(author_label)

    def retranslate(self):
        self._start_btn.setText(tr("main.start_button"))
        self._cancel_btn.setText(tr("main.cancel_button"))

    def _connect_signals(self):
        self._iso_selector.iso_selected.connect(self._on_iso_selected)
        self._drive_selector.drive_selected.connect(self._on_drive_selected)
        self._start_btn.clicked.connect(self._on_start)
        self._cancel_btn.clicked.connect(self._on_cancel)

    def _on_iso_selected(self, path: Path):
        self._iso_path = path
        self._iso_type = ISO_TYPE_UNKNOWN
        self._update_start_button()
        self._start_iso_analysis(path)

    def _start_iso_analysis(self, path: Path):
        """Start background ISO type detection."""
        if self._iso_info_worker and self._iso_info_worker.isRunning():
            self._iso_info_worker.cancel()
            self._iso_info_worker.wait()

        self._settings_panel.set_detecting()
        self._iso_info_worker = ISOInfoWorker(path, self)
        self._iso_info_worker.info_ready.connect(self._on_iso_info)
        self._iso_info_worker.error.connect(self._on_iso_info_error)
        self._iso_info_worker.start()

    def _on_iso_info(self, info):
        """Handle ISO analysis result."""
        self._iso_type = info.iso_type
        self._settings_panel.set_iso_type(info.iso_type)
        self._iso_selector.iso_type_detected.emit(info.iso_type)

    def _on_iso_info_error(self, message: str):
        """Handle ISO analysis error — default to unknown."""
        self._iso_type = ISO_TYPE_UNKNOWN
        self._settings_panel.set_iso_type(ISO_TYPE_UNKNOWN)

    def _on_drive_selected(self, drive: DriveInfo | None):
        self._selected_drive = drive
        self._update_start_button()

    def _update_start_button(self):
        enabled = self._iso_path is not None and self._selected_drive is not None
        self._start_btn.setEnabled(enabled)

    def _on_start(self):
        if not self._iso_path or not self._selected_drive:
            return

        is_dd = self._iso_type in (ISO_TYPE_LINUX, ISO_TYPE_MACOS, ISO_TYPE_UNKNOWN)

        # Confirm
        if not confirm_write(self, self._selected_drive, self._iso_path.name, is_dd_mode=is_dd):
            return

        # Build config
        config = WriteConfig(
            iso_path=self._iso_path,
            drive=self._selected_drive,
            boot_mode=self._settings_panel.get_boot_mode(),
            partition_strategy=self._settings_panel.get_partition_strategy(),
            iso_type=self._iso_type,
        )

        # UI state: writing
        self._set_writing_state(True)
        self._progress_panel.reset()

        # Start worker
        self._write_worker = WriteWorker(self._backend, config, self)
        self._write_worker.progress.connect(self._progress_panel.set_progress)
        self._write_worker.log.connect(self._progress_panel.append_log)
        self._write_worker.stage_changed.connect(self._on_stage_changed)
        self._write_worker.finished_ok.connect(self._on_write_finished)
        self._write_worker.error.connect(self._on_write_error)
        self._write_worker.cancelled.connect(self._on_write_cancelled)
        self._write_worker.start()

    def _on_cancel(self):
        if self._write_worker and self._write_worker.isRunning():
            self._write_worker.cancel()
            self._progress_panel.append_log(tr("main.cancel_requested"))

    def _on_stage_changed(self, stage_label: str, current_file: str):
        status = stage_label
        if current_file:
            status += f"  {current_file}"
        self._progress_panel.set_status(status)

    def _on_write_finished(self):
        self._set_writing_state(False)
        self._progress_panel.set_progress(100)
        self._progress_panel.set_status(tr("main.completed"))
        show_success(self)

    def _on_write_cancelled(self):
        self._set_writing_state(False)
        self._progress_panel.set_status(tr("main.cancelled"))

    def _on_write_error(self, message: str):
        self._set_writing_state(False)
        self._progress_panel.set_status(tr("main.error_status", message=message))
        show_error(self, tr("main.write_error_title"), message)

    def _set_writing_state(self, writing: bool):
        """Toggle UI elements based on whether writing is in progress."""
        self._start_btn.setEnabled(not writing)
        self._start_btn.setVisible(not writing)
        self._cancel_btn.setEnabled(writing)
        self._cancel_btn.setVisible(writing)
        self._settings_panel.set_enabled(not writing)
        self._iso_selector.setEnabled(not writing)
        self._drive_selector.setEnabled(not writing)
