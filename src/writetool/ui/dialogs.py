"""Confirmation and error dialogs."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget

from writetool.platform.base import DriveInfo
from writetool.utils.formatting import format_size


def confirm_write(parent: QWidget, drive: DriveInfo, iso_name: str) -> bool:
    """Show a confirmation dialog before writing.

    Returns True if the user confirms.
    """
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle("Yazma Onayı")
    msg.setText(
        f"<b>{drive.display_name}</b> üzerindeki TÜM VERİLER SİLİNECEK!"
    )
    msg.setInformativeText(
        f"<b>{iso_name}</b> dosyası <b>{drive.name}</b> "
        f"({format_size(drive.size)}) sürücüsüne yazılacak.\n\n"
        "Bu işlem geri alınamaz. Devam etmek istiyor musunuz?"
    )
    msg.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    msg.setDefaultButton(QMessageBox.StandardButton.No)
    msg.button(QMessageBox.StandardButton.Yes).setText("Evet, Yazdır")
    msg.button(QMessageBox.StandardButton.No).setText("İptal")

    return msg.exec() == QMessageBox.StandardButton.Yes


def show_error(parent: QWidget, title: str, message: str) -> None:
    """Show an error dialog."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def show_info(parent: QWidget, title: str, message: str) -> None:
    """Show an informational dialog."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle(title)
    msg.setText(message)
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


def show_success(parent: QWidget) -> None:
    """Show a write-complete success dialog."""
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setWindowTitle("Tamamlandı")
    msg.setText("USB yazma işlemi başarıyla tamamlandı!")
    msg.setInformativeText("USB sürücüyü güvenle çıkarabilirsiniz.")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
