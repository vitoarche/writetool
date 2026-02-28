"""Application entry point with language selection and privilege enforcement."""

import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from writetool.i18n import (
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    get_language,
    set_language,
    tr,
)
from writetool.platform.detector import get_backend
from writetool.ui.main_window import MainWindow
from writetool.ui.styles import STYLESHEET
from writetool.utils.constants import APP_NAME
from writetool.utils.privileges import is_admin, request_elevation


class LanguageDialog(QDialog):
    """Startup dialog for language selection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("WriteTool")
        self.setFixedSize(380, 200)
        self.setWindowFlags(
            Qt.WindowType.Dialog
            | Qt.WindowType.WindowTitleHint
            | Qt.WindowType.CustomizeWindowHint
        )
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)

        # Title
        title = QLabel("WriteTool")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title.font()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        layout.addWidget(title)

        # Language label + combo
        lang_row = QHBoxLayout()
        lang_row.setSpacing(16)
        self._lang_label = QLabel("Language:")
        self._lang_combo = QComboBox()
        self._lang_combo.setFixedHeight(32)
        for code in SUPPORTED_LANGUAGES:
            self._lang_combo.addItem(LANGUAGE_NAMES[code], code)

        # Set current language in combo
        current = get_language()
        idx = list(SUPPORTED_LANGUAGES).index(current)
        self._lang_combo.setCurrentIndex(idx)
        self._lang_combo.currentIndexChanged.connect(self._on_lang_changed)

        lang_row.addWidget(self._lang_label)
        lang_row.addWidget(self._lang_combo, 1)
        layout.addLayout(lang_row)

        layout.addStretch()

        # Continue button
        self._continue_btn = QPushButton(tr("app.continue_button"))
        self._continue_btn.setObjectName("startButton")
        self._continue_btn.setFixedHeight(36)
        self._continue_btn.clicked.connect(self.accept)
        layout.addWidget(self._continue_btn)

    def _on_lang_changed(self, index: int):
        code = self._lang_combo.itemData(index)
        if code:
            set_language(code)
            self._retranslate()

    def _retranslate(self):
        self._lang_label.setText(tr("settings.language_label"))
        self._continue_btn.setText(tr("app.continue_button"))

    def selected_language(self) -> str:
        return self._lang_combo.currentData()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)

    # Force Fusion style — bypasses macOS native rendering that ignores QSS colors
    app.setStyle("Fusion")

    app.setStyleSheet(STYLESHEET)

    # Fix placeholder text visibility on dark background
    palette = app.palette()
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor("#9399b2"))
    app.setPalette(palette)

    # Step 1: Language selection
    # Skip only if --skip-lang was passed (after admin elevation)
    if "--skip-lang" not in sys.argv:
        lang_dialog = LanguageDialog()
        if lang_dialog.exec() != QDialog.DialogCode.Accepted:
            sys.exit(0)

    # Step 2: Enforce admin privileges
    if not is_admin():
        QMessageBox.warning(
            None,
            tr("app.privilege_title"),
            tr("app.privilege_message"),
        )
        if request_elevation():
            sys.exit(0)
        else:
            QMessageBox.critical(
                None,
                tr("app.privilege_error_title"),
                tr("app.privilege_error_message"),
            )
            sys.exit(1)

    backend = get_backend()
    window = MainWindow(backend)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
