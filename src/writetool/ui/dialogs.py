"""Confirmation and error dialogs."""

from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QWidget

from writetool.i18n import tr
from writetool.platform.base import DriveInfo
from writetool.utils.formatting import format_size


def confirm_write(parent: QWidget, drive: DriveInfo, iso_name: str) -> bool:
    """Show a confirmation dialog before writing.

    Returns True if the user confirms.
    """
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Warning)
    msg.setWindowTitle(tr("dialog.confirm_title"))
    msg.setText(
        tr("dialog.confirm_warning", drive_name=drive.display_name)
    )
    msg.setInformativeText(
        tr(
            "dialog.confirm_detail",
            iso_name=iso_name,
            name=drive.name,
            size=format_size(drive.size),
        )
    )
    msg.setStandardButtons(
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
    )
    msg.setDefaultButton(QMessageBox.StandardButton.No)
    msg.button(QMessageBox.StandardButton.Yes).setText(tr("dialog.confirm_yes"))
    msg.button(QMessageBox.StandardButton.No).setText(tr("dialog.confirm_no"))

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
    msg.setWindowTitle(tr("dialog.success_title"))
    msg.setText(tr("dialog.success_message"))
    msg.setInformativeText(tr("dialog.success_detail"))
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()
