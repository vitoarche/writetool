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
        super().__init__("Seçenekler", parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Boot mode
        boot_row = QHBoxLayout()
        boot_label = QLabel("Boot:")
        self._uefi_radio = QRadioButton("UEFI")
        self._legacy_radio = QRadioButton("Legacy BIOS")
        self._uefi_radio.setChecked(True)

        self._boot_group = QButtonGroup(self)
        self._boot_group.addButton(self._uefi_radio)
        self._boot_group.addButton(self._legacy_radio)

        boot_row.addWidget(boot_label)
        boot_row.addWidget(self._uefi_radio)
        boot_row.addWidget(self._legacy_radio)
        boot_row.addStretch()
        layout.addLayout(boot_row)

        # Partition strategy
        part_row = QHBoxLayout()
        part_label = QLabel("Partition:")
        self._auto_radio = QRadioButton("Otomatik")
        self._wim_split_radio = QRadioButton("WIM Böl")
        self._dual_radio = QRadioButton("Çift Partition")
        self._auto_radio.setChecked(True)

        self._part_group = QButtonGroup(self)
        self._part_group.addButton(self._auto_radio)
        self._part_group.addButton(self._wim_split_radio)
        self._part_group.addButton(self._dual_radio)

        # Disable WIM split if wimlib not available
        if not is_wimlib_available():
            self._wim_split_radio.setEnabled(False)
            self._wim_split_radio.setToolTip(
                "wimlib-imagex bulunamadı. Kurulum:\n"
                "  macOS: brew install wimlib\n"
                "  Linux: sudo apt install wimtools"
            )

        part_row.addWidget(part_label)
        part_row.addWidget(self._auto_radio)
        part_row.addWidget(self._wim_split_radio)
        part_row.addWidget(self._dual_radio)
        part_row.addStretch()
        layout.addLayout(part_row)

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
