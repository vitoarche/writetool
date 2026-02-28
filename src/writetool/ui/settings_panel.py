"""Boot mode and partition strategy settings panel."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QButtonGroup,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QRadioButton,
    QVBoxLayout,
)

from writetool.core.wim_splitter import is_wimlib_available
from writetool.i18n import on_language_changed, tr
from writetool.utils.constants import (
    BOOT_MODE_LEGACY,
    BOOT_MODE_UEFI,
    ISO_TYPE_LINUX,
    ISO_TYPE_MACOS,
    ISO_TYPE_UNKNOWN,
    ISO_TYPE_WINDOWS,
    PARTITION_AUTO,
    PARTITION_DUAL,
    PARTITION_WIM_SPLIT,
)


class SettingsPanel(QGroupBox):
    """Panel for boot mode and partition strategy selection."""

    def __init__(self, parent=None):
        super().__init__(tr("settings.group_title"), parent)
        self._iso_type = ISO_TYPE_UNKNOWN
        self._setup_ui()
        on_language_changed(self.retranslate)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # ISO type row
        iso_type_row = QHBoxLayout()
        self._iso_type_label = QLabel(tr("settings.iso_type_label"))
        self._iso_type_value = QLabel("")
        self._iso_type_value.setObjectName("statusLabel")
        iso_type_row.addWidget(self._iso_type_label)
        iso_type_row.addWidget(self._iso_type_value)
        iso_type_row.addStretch()
        layout.addLayout(iso_type_row)
        # Hide initially — shown after ISO selection
        self._iso_type_label.setVisible(False)
        self._iso_type_value.setVisible(False)

        # Boot mode
        self._boot_row = QHBoxLayout()
        self._boot_label = QLabel(tr("settings.boot_label"))
        self._uefi_radio = QRadioButton(tr("settings.boot_uefi"))
        self._legacy_radio = QRadioButton(tr("settings.boot_legacy"))
        self._uefi_radio.setChecked(True)

        self._boot_group = QButtonGroup(self)
        self._boot_group.addButton(self._uefi_radio)
        self._boot_group.addButton(self._legacy_radio)

        self._boot_row.addWidget(self._boot_label)
        self._boot_row.addWidget(self._uefi_radio)
        self._boot_row.addWidget(self._legacy_radio)
        self._boot_row.addStretch()
        layout.addLayout(self._boot_row)

        # Partition strategy
        self._part_row = QHBoxLayout()
        self._part_label = QLabel(tr("settings.partition_label"))
        self._auto_radio = QRadioButton(tr("settings.partition_auto"))
        self._wim_split_radio = QRadioButton(tr("settings.partition_wim_split"))
        self._dual_radio = QRadioButton(tr("settings.partition_dual"))
        self._auto_radio.setChecked(True)

        self._part_group = QButtonGroup(self)
        self._part_group.addButton(self._auto_radio)
        self._part_group.addButton(self._wim_split_radio)
        self._part_group.addButton(self._dual_radio)

        # Disable WIM split if wimlib not available
        if not is_wimlib_available():
            self._wim_split_radio.setEnabled(False)
            self._wim_split_radio.setToolTip(tr("settings.wimlib_missing"))

        self._part_row.addWidget(self._part_label)
        self._part_row.addWidget(self._auto_radio)
        self._part_row.addWidget(self._wim_split_radio)
        self._part_row.addWidget(self._dual_radio)
        self._part_row.addStretch()
        layout.addLayout(self._part_row)

        # DD note (hidden by default)
        self._dd_note = QLabel(tr("settings.dd_note"))
        self._dd_note.setWordWrap(True)
        self._dd_note.setObjectName("statusLabel")
        self._dd_note.setVisible(False)
        layout.addWidget(self._dd_note)

    def retranslate(self):
        self.setTitle(tr("settings.group_title"))
        self._iso_type_label.setText(tr("settings.iso_type_label"))
        self._boot_label.setText(tr("settings.boot_label"))
        self._uefi_radio.setText(tr("settings.boot_uefi"))
        self._legacy_radio.setText(tr("settings.boot_legacy"))
        self._part_label.setText(tr("settings.partition_label"))
        self._auto_radio.setText(tr("settings.partition_auto"))
        self._wim_split_radio.setText(tr("settings.partition_wim_split"))
        self._dual_radio.setText(tr("settings.partition_dual"))
        self._dd_note.setText(tr("settings.dd_note"))
        if not is_wimlib_available():
            self._wim_split_radio.setToolTip(tr("settings.wimlib_missing"))
        # Refresh ISO type display
        self.set_iso_type(self._iso_type)

    def set_iso_type(self, iso_type: str) -> None:
        """Update the displayed ISO type and toggle option visibility."""
        self._iso_type = iso_type

        type_labels = {
            ISO_TYPE_WINDOWS: tr("settings.iso_type_windows"),
            ISO_TYPE_LINUX: tr("settings.iso_type_linux"),
            ISO_TYPE_MACOS: tr("settings.iso_type_macos"),
            ISO_TYPE_UNKNOWN: tr("settings.iso_type_unknown"),
        }
        self._iso_type_value.setText(type_labels.get(iso_type, iso_type))
        self._iso_type_label.setVisible(True)
        self._iso_type_value.setVisible(True)

        is_dd = iso_type in (ISO_TYPE_LINUX, ISO_TYPE_MACOS, ISO_TYPE_UNKNOWN)

        # Hide boot/partition options for DD mode
        self._boot_label.setVisible(not is_dd)
        self._uefi_radio.setVisible(not is_dd)
        self._legacy_radio.setVisible(not is_dd)
        self._part_label.setVisible(not is_dd)
        self._auto_radio.setVisible(not is_dd)
        self._wim_split_radio.setVisible(not is_dd)
        self._dual_radio.setVisible(not is_dd)
        self._dd_note.setVisible(is_dd)

    def set_detecting(self) -> None:
        """Show detecting state."""
        self._iso_type_label.setVisible(True)
        self._iso_type_value.setVisible(True)
        self._iso_type_value.setText(tr("settings.iso_type_detecting"))

    def get_iso_type(self) -> str:
        return self._iso_type

    def get_boot_mode(self) -> str:
        if self._legacy_radio.isChecked():
            return BOOT_MODE_LEGACY
        return BOOT_MODE_UEFI

    def get_partition_strategy(self) -> str:
        if self._wim_split_radio.isChecked():
            return PARTITION_WIM_SPLIT
        if self._dual_radio.isChecked():
            return PARTITION_DUAL
        return PARTITION_AUTO

    def set_enabled(self, enabled: bool):
        """Enable or disable all settings."""
        self._uefi_radio.setEnabled(enabled)
        self._legacy_radio.setEnabled(enabled)
        self._auto_radio.setEnabled(enabled)
        self._dual_radio.setEnabled(enabled)
        if enabled and is_wimlib_available():
            self._wim_split_radio.setEnabled(True)
        elif not enabled:
            self._wim_split_radio.setEnabled(False)
