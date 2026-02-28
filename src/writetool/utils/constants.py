"""Application constants."""

APP_NAME = "WriteTool"
APP_VERSION = "0.1.0"
APP_TITLE = "WriteTool - Windows USB Installer Creator"

# FAT32 max file size
FAT32_MAX_FILE_SIZE = 4 * 1024 * 1024 * 1024  # 4 GB

# Checksum buffer size
CHECKSUM_BUFFER_SIZE = 8 * 1024 * 1024  # 8 MB

# Copy buffer size
COPY_BUFFER_SIZE = 4 * 1024 * 1024  # 4 MB

# WIM split chunk size (3.8 GB to stay under FAT32 limit)
WIM_SPLIT_SIZE_MB = 3800

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
STAGE_VERIFY = "verify"
STAGE_EJECT = "eject"

STAGE_LABELS = {
    STAGE_UNMOUNT: "Unmount ediliyor...",
    STAGE_FORMAT: "Formatlanıyor...",
    STAGE_EXTRACT_BOOT: "Boot dosyaları çıkarılıyor...",
    STAGE_COPY_FILES: "Dosyalar kopyalanıyor...",
    STAGE_PROCESS_WIM: "install.wim işleniyor...",
    STAGE_VERIFY: "Doğrulanıyor...",
    STAGE_EJECT: "Eject ediliyor...",
}

# install.wim path inside ISO
INSTALL_WIM_PATH = "/sources/install.wim"
INSTALL_ESD_PATH = "/sources/install.esd"

# EFI boot file
EFI_BOOT_PATH = "/efi/boot/bootx64.efi"
