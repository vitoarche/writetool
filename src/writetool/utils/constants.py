"""Application constants."""

APP_NAME = "WriteTool"
APP_VERSION = "0.1.0"
APP_TITLE = "WriteTool - USB Installer Creator"

# FAT32 max file size
FAT32_MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB

# Checksum buffer size
CHECKSUM_BUFFER_SIZE = 8 * 1024 * 1024  # 8 MB

# Copy buffer size
COPY_BUFFER_SIZE = 4 * 1024 * 1024  # 4 MB

# DD block size for raw writes
DD_BLOCK_SIZE = 4 * 1024 * 1024  # 4 MB

# WIM split chunk size (3.8 GB to stay under FAT32 limit)
WIM_SPLIT_SIZE_MB = 3800

# ISO types
ISO_TYPE_WINDOWS = "windows"
ISO_TYPE_LINUX = "linux"
ISO_TYPE_MACOS = "macos"
ISO_TYPE_UNKNOWN = "unknown"

# Boot modes
BOOT_MODE_UEFI = "uefi"
BOOT_MODE_LEGACY = "legacy"

# Partition strategies
PARTITION_AUTO = "auto"
PARTITION_WIM_SPLIT = "wim_split"
PARTITION_DUAL = "dual"

# Pipeline stages
STAGE_UNMOUNT = "unmount"
STAGE_FORMAT = "format"
STAGE_EXTRACT_BOOT = "extract_boot"
STAGE_COPY_FILES = "copy_files"
STAGE_PROCESS_WIM = "process_wim"
STAGE_DD_WRITE = "dd_write"
STAGE_VERIFY = "verify"
STAGE_EJECT = "eject"

_STAGE_TR_KEYS = {
    STAGE_UNMOUNT: "stage.unmount",
    STAGE_FORMAT: "stage.format",
    STAGE_EXTRACT_BOOT: "stage.extract_boot",
    STAGE_COPY_FILES: "stage.copy_files",
    STAGE_PROCESS_WIM: "stage.process_wim",
    STAGE_DD_WRITE: "stage.dd_write",
    STAGE_VERIFY: "stage.verify",
    STAGE_EJECT: "stage.eject",
}


def get_stage_label(stage: str) -> str:
    """Return the translated label for a pipeline stage."""
    from writetool.i18n import tr
    key = _STAGE_TR_KEYS.get(stage)
    if key:
        return tr(key)
    return stage

# install.wim path inside ISO
INSTALL_WIM_PATH = "/sources/install.wim"
INSTALL_ESD_PATH = "/sources/install.esd"

# EFI boot file
EFI_BOOT_PATH = "/efi/boot/bootx64.efi"
