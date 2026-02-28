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
    PARTITION_AUTO,
    PARTITION_DUAL,
    PARTITION_WIM_SPLIT,
)


class SettingsPanel(QGroupBox):
    """Panel for boot mode and partition strategy selection."""

    def __init__(self, parent=None):
        super().__init__(tr("settings.group_title"), parent)
        self._setup_ui()
        on_language_changed(self.retranslate)

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Boot mode
        boot_row = QHBoxLayout()
        self._boot_label = QLabel(tr("settings.boot_label"))
        self._uefi_radio = QRadioButton(tr("settings.boot_uefi"))
        self._legacy_radio = QRadioButton(tr("settings.boot_legacy"))
        self._uefi_radio.setChecked(True)

        self._boot_group = QButtonGroup(self)
        self._boot_group.addButton(self._uefi_radio)
        self._boot_group.addButton(self._legacy_radio)

        boot_row.addWidget(self._boot_label)
        boot_row.addWidget(self._uefi_radio)
        boot_row.addWidget(self._legacy_radio)
        boot_row.addStretch()
        layout.addLayout(boot_row)

        # Partition strategy
        part_row = QHBoxLayout()
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

        part_row.addWidget(self._part_label)
        part_row.addWidget(self._auto_radio)
        part_row.addWidget(self._wim_split_radio)
        part_row.addWidget(self._dual_radio)
        part_row.addStretch()
        layout.addLayout(part_row)

    def retranslate(self):
        self.setTitle(tr("settings.group_title"))
        self._boot_label.setText(tr("settings.boot_label"))
        self._uefi_radio.setText(tr("settings.boot_uefi"))
        self._legacy_radio.setText(tr("settings.boot_legacy"))
        self._part_label.setText(tr("settings.partition_label"))
        self._auto_radio.setText(tr("settings.partition_auto"))
        self._wim_split_radio.setText(tr("settings.partition_wim_split"))
        self._dual_radio.setText(tr("settings.partition_dual"))
        if not is_wimlib_available():
            self._wim_split_radio.setToolTip(tr("settings.wimlib_missing"))

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
