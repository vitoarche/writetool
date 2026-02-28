"""Abstract platform backend interface."""

from __future__ import annotations

import abc
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass
class DriveInfo:
    """Represents a removable USB drive."""

    device: str  # e.g. /dev/disk2, /dev/sdb, \\.\PhysicalDrive1
    name: str  # Vendor + Model
    size: int  # bytes
    mountpoint: str | None = None
    partitions: list[str] = field(default_factory=list)

    @property
    def display_name(self) -> str:
        from writetool.utils.formatting import format_size
        return f"{self.name} ({format_size(self.size)}) [{self.device}]"


class PlatformBackend(abc.ABC):
    """Abstract base class for platform-specific operations."""

    @abc.abstractmethod
    def list_usb_drives(self) -> list[DriveInfo]:
        """Return a list of removable USB drives."""

    @abc.abstractmethod
    def unmount_drive(self, drive: DriveInfo) -> None:
        """Unmount all partitions on the drive."""

    @abc.abstractmethod
    def format_drive_gpt_fat32(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        """Format drive with GPT partition table and a single FAT32 partition.

        Returns the partition device path (e.g. /dev/disk2s1).
        """

    @abc.abstractmethod
    def format_drive_mbr_ntfs(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        """Format drive with MBR partition table and a single NTFS partition.

        Returns the partition device path.
        """

    @abc.abstractmethod
    def format_drive_dual(
        self, drive: DriveInfo, boot_label: str = "BOOT", data_label: str = "DATA"
    ) -> tuple[str, str]:
        """Format drive with GPT: FAT32 boot partition + NTFS/ExFAT data partition.

        Returns (boot_partition_path, data_partition_path).
        """

    @abc.abstractmethod
    def mount_partition(self, partition_device: str) -> Path:
        """Mount a partition and return the mount point path."""

    @abc.abstractmethod
    def eject_drive(self, drive: DriveInfo) -> None:
        """Safely eject the drive."""

    @abc.abstractmethod
    def dd_write(
        self,
        source_path: Path,
        drive: DriveInfo,
        block_size: int,
        progress_callback: Callable[[int, int], None] | None = None,
        cancel_check: Callable[[], bool] | None = None,
    ) -> None:
        """Write a raw image file to a drive using block copy.

        Args:
            source_path: Path to the ISO/IMG file to write.
            drive: Target drive info.
            block_size: Block size for read/write operations.
            progress_callback: Called with (bytes_written, total_bytes).
            cancel_check: If returns True, abort the write.
        """

    @abc.abstractmethod
    def open_terminal_command(self, command: str) -> str:
        """Return the full command string to run a command with admin privileges."""
