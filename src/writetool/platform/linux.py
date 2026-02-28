"""Linux platform backend using lsblk, parted, mkfs."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from writetool.core.exceptions import DriveError, DriveInUseError, FormatError
from writetool.i18n import tr
from writetool.platform.base import DriveInfo, PlatformBackend


class LinuxBackend(PlatformBackend):

    def _run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        return subprocess.run(cmd, capture_output=True, text=True, check=check)

    def list_usb_drives(self) -> list[DriveInfo]:
        try:
            result = self._run(
                [
                    "lsblk",
                    "-J",
                    "-o",
                    "NAME,SIZE,TYPE,MOUNTPOINT,RM,VENDOR,MODEL,TRAN",
                    "-b",
                    "-d",
                ]
            )
            data = json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return []

        drives = []
        for dev in data.get("blockdevices", []):
            # Filter: removable USB disks only
            if dev.get("type") != "disk":
                continue
            if dev.get("tran") != "usb" and not dev.get("rm"):
                continue

            name_parts = []
            if dev.get("vendor"):
                name_parts.append(dev["vendor"].strip())
            if dev.get("model"):
                name_parts.append(dev["model"].strip())
            name = " ".join(name_parts) or "USB Drive"

            device = f"/dev/{dev['name']}"
            size = int(dev.get("size", 0))

            # Get partitions
            parts_result = self._run(
                ["lsblk", "-J", "-o", "NAME,MOUNTPOINT", device], check=False
            )
            partitions = []
            mount = None
            if parts_result.returncode == 0:
                try:
                    pdata = json.loads(parts_result.stdout)
                    for bd in pdata.get("blockdevices", []):
                        for child in bd.get("children", []):
                            p = f"/dev/{child['name']}"
                            partitions.append(p)
                            mp = child.get("mountpoint")
                            if mp and mount is None:
                                mount = mp
                except json.JSONDecodeError:
                    pass

            drives.append(
                DriveInfo(
                    device=device,
                    name=name,
                    size=size,
                    mountpoint=mount,
                    partitions=partitions,
                )
            )
        return drives

    def unmount_drive(self, drive: DriveInfo) -> None:
        for part in drive.partitions:
            result = self._run(["umount", part], check=False)
            # Ignore "not mounted" errors
            if result.returncode != 0 and "not mounted" not in result.stderr:
                raise DriveInUseError(
                    tr("platform.unmount_failed", device=part, error=result.stderr.strip())
                )

        # Also try unmounting the device itself
        self._run(["umount", drive.device], check=False)

    def format_drive_gpt_fat32(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        # Create GPT table
        self._checked_run(["parted", "-s", drive.device, "mklabel", "gpt"])
        # Create FAT32 partition
        self._checked_run(
            ["parted", "-s", drive.device, "mkpart", "primary", "fat32", "1MiB", "100%"]
        )
        # Set boot flag
        self._checked_run(["parted", "-s", drive.device, "set", "1", "boot", "on"])

        part = self._partition_path(drive.device, 1)
        # Format
        self._checked_run(["mkfs.vfat", "-F", "32", "-n", label, part])
        return part

    def format_drive_mbr_ntfs(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        self._checked_run(["parted", "-s", drive.device, "mklabel", "msdos"])
        self._checked_run(
            ["parted", "-s", drive.device, "mkpart", "primary", "ntfs", "1MiB", "100%"]
        )
        self._checked_run(["parted", "-s", drive.device, "set", "1", "boot", "on"])

        part = self._partition_path(drive.device, 1)
        self._checked_run(["mkfs.ntfs", "-f", "-L", label, part])
        return part

    def format_drive_dual(
        self, drive: DriveInfo, boot_label: str = "BOOT", data_label: str = "DATA"
    ) -> tuple[str, str]:
        self._checked_run(["parted", "-s", drive.device, "mklabel", "gpt"])
        # 1GB FAT32 boot partition
        self._checked_run(
            ["parted", "-s", drive.device, "mkpart", "primary", "fat32", "1MiB", "1024MiB"]
        )
        self._checked_run(["parted", "-s", drive.device, "set", "1", "boot", "on"])
        # Remaining space as NTFS
        self._checked_run(
            ["parted", "-s", drive.device, "mkpart", "primary", "ntfs", "1024MiB", "100%"]
        )

        boot_part = self._partition_path(drive.device, 1)
        data_part = self._partition_path(drive.device, 2)

        self._checked_run(["mkfs.vfat", "-F", "32", "-n", boot_label, boot_part])
        self._checked_run(["mkfs.ntfs", "-f", "-L", data_label, data_part])

        return boot_part, data_part

    def mount_partition(self, partition_device: str) -> Path:
        mount_dir = Path(tempfile.mkdtemp(prefix="writetool_"))
        result = self._run(["mount", partition_device, str(mount_dir)], check=False)
        if result.returncode != 0:
            mount_dir.rmdir()
            raise DriveError(tr("platform.mount_error", error=result.stderr.strip()))
        return mount_dir

    def eject_drive(self, drive: DriveInfo) -> None:
        self.unmount_drive(drive)
        # Use udisksctl if available, otherwise eject
        result = self._run(
            ["udisksctl", "power-off", "-b", drive.device], check=False
        )
        if result.returncode != 0:
            self._run(["eject", drive.device], check=False)

    def open_terminal_command(self, command: str) -> str:
        return f"pkexec {command}"

    def _partition_path(self, device: str, num: int) -> str:
        """Get partition device path. Handles /dev/sdX1 and /dev/nvmeXnYp1 styles."""
        if device[-1].isdigit():
            return f"{device}p{num}"
        return f"{device}{num}"

    def _checked_run(self, cmd: list[str]) -> subprocess.CompletedProcess:
        result = self._run(cmd, check=False)
        if result.returncode != 0:
            raise FormatError(
                tr("platform.command_failed", command=" ".join(cmd), error=result.stderr.strip())
            )
        return result
