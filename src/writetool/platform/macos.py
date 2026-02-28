"""macOS platform backend using diskutil."""

from __future__ import annotations

import plistlib
import subprocess
import tempfile
from pathlib import Path

from writetool.core.exceptions import DriveError, DriveInUseError, FormatError
from writetool.platform.base import DriveInfo, PlatformBackend


class MacOSBackend(PlatformBackend):

    def _run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)

    def _run_bytes(self, cmd: list[str]) -> bytes:
        result = subprocess.run(cmd, capture_output=True, check=True)
        return result.stdout

    def list_usb_drives(self) -> list[DriveInfo]:
        try:
            raw = self._run_bytes(["diskutil", "list", "-plist", "external", "physical"])
            plist = plistlib.loads(raw)
        except (subprocess.CalledProcessError, plistlib.InvalidFileException):
            return []

        drives = []
        for disk_id in plist.get("AllDisksAndPartitions", []):
            device = f"/dev/{disk_id.get('DeviceIdentifier', '')}"
            try:
                info_raw = self._run_bytes(["diskutil", "info", "-plist", device])
                info = plistlib.loads(info_raw)
            except (subprocess.CalledProcessError, plistlib.InvalidFileException):
                continue

            if not info.get("Removable", False) and not info.get("RemovableMedia", False):
                continue

            size = info.get("TotalSize", info.get("Size", 0))
            vendor = info.get("MediaName", "USB Drive")

            partitions = []
            mount = None
            for part in disk_id.get("Partitions", []):
                p_dev = f"/dev/{part.get('DeviceIdentifier', '')}"
                partitions.append(p_dev)
                mp = part.get("MountPoint")
                if mp and mount is None:
                    mount = mp

            drives.append(
                DriveInfo(
                    device=device,
                    name=vendor,
                    size=size,
                    mountpoint=mount,
                    partitions=partitions,
                )
            )
        return drives

    def unmount_drive(self, drive: DriveInfo) -> None:
        result = self._run(["diskutil", "unmountDisk", drive.device], check=False)
        if result.returncode != 0:
            # Retry with force
            result = self._run(
                ["diskutil", "unmountDisk", "force", drive.device], check=False
            )
            if result.returncode != 0:
                raise DriveInUseError(
                    f"'{drive.device}' unmount edilemedi: {result.stderr.strip()}"
                )

    def format_drive_gpt_fat32(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        result = self._run(
            ["diskutil", "eraseDisk", "FAT32", label, "GPTFormat", drive.device],
            check=False,
        )
        if result.returncode != 0:
            raise FormatError(f"Format hatası: {result.stderr.strip()}")

        # GPT creates: s1=EFI, s2=data. Find the data partition by label.
        return self._find_partition_by_label(drive.device, label)

    def format_drive_mbr_ntfs(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        # macOS cannot natively format NTFS; use ExFAT as fallback
        result = self._run(
            ["diskutil", "eraseDisk", "ExFAT", label, "MBRFormat", drive.device],
            check=False,
        )
        if result.returncode != 0:
            raise FormatError(f"Format hatası: {result.stderr.strip()}")
        # MBR: data partition is s1
        return self._find_partition_by_label(drive.device, label)

    def format_drive_dual(
        self, drive: DriveInfo, boot_label: str = "BOOT", data_label: str = "DATA"
    ) -> tuple[str, str]:
        # Use diskutil partitionDisk for dual partition
        result = self._run(
            [
                "diskutil",
                "partitionDisk",
                drive.device,
                "GPT",
                "FAT32",
                boot_label,
                "1G",
                "ExFAT",
                data_label,
                "R",  # remainder
            ],
            check=False,
        )
        if result.returncode != 0:
            raise FormatError(f"Dual format hatası: {result.stderr.strip()}")

        boot_part = self._find_partition_by_label(drive.device, boot_label)
        data_part = self._find_partition_by_label(drive.device, data_label)
        return boot_part, data_part

    def mount_partition(self, partition_device: str) -> Path:
        # Check if already mounted (macOS auto-mounts after format)
        mp = self._get_mount_point(partition_device)
        if mp:
            return mp

        result = self._run(["diskutil", "mount", partition_device], check=False)
        if result.returncode != 0:
            raise DriveError(f"Mount hatası: {result.stderr.strip()}")

        mp = self._get_mount_point(partition_device)
        if mp:
            return mp
        raise DriveError(f"Mount noktası bulunamadı: {partition_device}")

    def _get_mount_point(self, partition_device: str) -> Path | None:
        """Get the mount point of a partition, or None if not mounted."""
        try:
            info_raw = self._run_bytes(["diskutil", "info", "-plist", partition_device])
            info = plistlib.loads(info_raw)
            mp = info.get("MountPoint")
            if mp:
                return Path(mp)
        except (subprocess.CalledProcessError, plistlib.InvalidFileException):
            pass
        return None

    def _find_partition_by_label(self, device: str, label: str) -> str:
        """Find a partition device path by its volume label after formatting."""
        try:
            raw = self._run_bytes(["diskutil", "list", "-plist", device])
            plist = plistlib.loads(raw)
        except (subprocess.CalledProcessError, plistlib.InvalidFileException):
            pass
        else:
            for disk in plist.get("AllDisksAndPartitions", []):
                for part in disk.get("Partitions", []):
                    if part.get("VolumeName") == label:
                        return f"/dev/{part['DeviceIdentifier']}"

        # Fallback: pick the last non-EFI partition
        base = device.replace("/dev/", "")
        for n in range(5, 0, -1):
            candidate = f"/dev/{base}s{n}"
            try:
                info_raw = self._run_bytes(["diskutil", "info", "-plist", candidate])
                info = plistlib.loads(info_raw)
                if info.get("FilesystemName", "") != "EFI":
                    return candidate
            except (subprocess.CalledProcessError, plistlib.InvalidFileException):
                continue

        raise FormatError(f"'{label}' etiketli partition bulunamadı: {device}")

    def eject_drive(self, drive: DriveInfo) -> None:
        result = self._run(["diskutil", "eject", drive.device], check=False)
        if result.returncode != 0:
            raise DriveError(f"Eject hatası: {result.stderr.strip()}")

    def open_terminal_command(self, command: str) -> str:
        return f'osascript -e \'do shell script "{command}" with administrator privileges\''
