"""Application entry point with privilege checking."""

import sys

from PySide6.QtWidgets import QApplication, QMessageBox

from writetool.platform.detector import get_backend
from writetool.ui.main_window import MainWindow
from writetool.ui.styles import STYLESHEET
from writetool.utils.constants import APP_NAME
from writetool.utils.privileges import is_admin, request_elevation


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(STYLESHEET)

    # Check for admin privileges
    if not is_admin():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Yetki Gerekli")
        msg.setText(
            "WriteTool, USB sürücülere yazabilmek için yönetici yetkisi gerektirir."
        )
        msg.setInformativeText("Yönetici olarak yeniden başlatılsın mı?")
        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        msg.setDefaultButton(QMessageBox.StandardButton.Yes)
        msg.button(QMessageBox.StandardButton.Yes).setText("Yönetici Olarak Başlat")
        msg.button(QMessageBox.StandardButton.No).setText("Yine de Devam Et")

        result = msg.exec()
        if result == QMessageBox.StandardButton.Yes:
            if request_elevation():
                sys.exit(0)
            else:
                QMessageBox.critical(
                    None,
                    "Hata",
                    "Yönetici yetkisi alınamadı. Uygulama sınırlı modda çalışacak.",
                )

    backend = get_backend()
    window = MainWindow(backend)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
