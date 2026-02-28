"""Windows platform backend using PowerShell and diskpart."""

from __future__ import annotations

import json
import subprocess
import tempfile
from pathlib import Path

from writetool.core.exceptions import DriveError, FormatError
from writetool.i18n import tr
from writetool.platform.base import DriveInfo, PlatformBackend


class WindowsBackend(PlatformBackend):

    def _ps(self, script: str) -> str:
        """Run a PowerShell command and return stdout."""
        result = subprocess.run(
            ["powershell", "-NoProfile", "-Command", script],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise DriveError(tr("platform.powershell_error", error=result.stderr.strip()))
        return result.stdout.strip()

    def _diskpart(self, commands: list[str]) -> str:
        """Run diskpart with a script and return output."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("\n".join(commands) + "\n")
            script_path = f.name

        try:
            result = subprocess.run(
                ["diskpart", "/s", script_path],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise FormatError(tr("platform.diskpart_error", error=result.stderr.strip()))
            return result.stdout
        finally:
            Path(script_path).unlink(missing_ok=True)

    def list_usb_drives(self) -> list[DriveInfo]:
        script = (
            "Get-Disk | Where-Object { $_.BusType -eq 'USB' } | "
            "Select-Object Number, FriendlyName, Size, PartitionStyle | "
            "ConvertTo-Json"
        )
        try:
            raw = self._ps(script)
            if not raw:
                return []
            data = json.loads(raw)
        except (json.JSONDecodeError, DriveError):
            return []

        # Normalize to list
        if isinstance(data, dict):
            data = [data]

        drives = []
        for disk in data:
            disk_num = disk.get("Number", 0)
            device = f"\\\\.\\PhysicalDrive{disk_num}"

            # Get partitions and mount points
            part_script = (
                f"Get-Partition -DiskNumber {disk_num} -ErrorAction SilentlyContinue | "
                "Select-Object PartitionNumber, DriveLetter, Size | ConvertTo-Json"
            )
            try:
                part_raw = self._ps(part_script)
                parts_data = json.loads(part_raw) if part_raw else []
            except (json.JSONDecodeError, DriveError):
                parts_data = []

            if isinstance(parts_data, dict):
                parts_data = [parts_data]

            partitions = []
            mount = None
            for p in parts_data:
                letter = p.get("DriveLetter")
                if letter and str(letter) != "0":
                    partitions.append(f"{letter}:")
                    if mount is None:
                        mount = f"{letter}:\\"

            drives.append(
                DriveInfo(
                    device=device,
                    name=disk.get("FriendlyName", "USB Drive"),
                    size=int(disk.get("Size", 0)),
                    mountpoint=mount,
                    partitions=partitions,
                )
            )
        return drives

    def unmount_drive(self, drive: DriveInfo) -> None:
        disk_num = self._disk_number(drive)
        script = (
            f"Get-Partition -DiskNumber {disk_num} -ErrorAction SilentlyContinue | "
            "ForEach-Object { "
            "  if ($_.DriveLetter) { "
            "    $vol = Get-Volume -DriveLetter $_.DriveLetter -ErrorAction SilentlyContinue; "
            "    if ($vol) { "
            "      $vol | Set-Volume -DriveLetter $null -ErrorAction SilentlyContinue "
            "    } "
            "  } "
            "}"
        )
        try:
            self._ps(script)
        except DriveError:
            pass  # Best effort

    def format_drive_gpt_fat32(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        disk_num = self._disk_number(drive)
        commands = [
            f"select disk {disk_num}",
            "clean",
            "convert gpt",
            "create partition primary",
            f"format fs=fat32 quick label={label}",
            "assign",
        ]
        self._diskpart(commands)
        return self._get_assigned_letter(disk_num)

    def format_drive_mbr_ntfs(self, drive: DriveInfo, label: str = "WRITETOOL") -> str:
        disk_num = self._disk_number(drive)
        commands = [
            f"select disk {disk_num}",
            "clean",
            "convert mbr",
            "create partition primary",
            "active",
            f"format fs=ntfs quick label={label}",
            "assign",
        ]
        self._diskpart(commands)
        return self._get_assigned_letter(disk_num)

    def format_drive_dual(
        self, drive: DriveInfo, boot_label: str = "BOOT", data_label: str = "DATA"
    ) -> tuple[str, str]:
        disk_num = self._disk_number(drive)
        commands = [
            f"select disk {disk_num}",
            "clean",
            "convert gpt",
            "create partition primary size=1024",
            f"format fs=fat32 quick label={boot_label}",
            "assign",
            "create partition primary",
            f"format fs=ntfs quick label={data_label}",
            "assign",
        ]
        self._diskpart(commands)

        # Get both drive letters
        script = (
            f"Get-Partition -DiskNumber {disk_num} | "
            "Sort-Object PartitionNumber | "
            "Select-Object DriveLetter | ConvertTo-Json"
        )
        raw = self._ps(script)
        parts = json.loads(raw)
        if isinstance(parts, dict):
            parts = [parts]

        letters = [p["DriveLetter"] for p in parts if p.get("DriveLetter")]
        if len(letters) < 2:
            raise FormatError(tr("platform.dual_no_letters"))
        return f"{letters[0]}:\\", f"{letters[1]}:\\"

    def mount_partition(self, partition_device: str) -> Path:
        # On Windows, partitions are already mounted with drive letters
        return Path(partition_device)

    def eject_drive(self, drive: DriveInfo) -> None:
        disk_num = self._disk_number(drive)
        script = (
            f"$disk = Get-Disk -Number {disk_num}; "
            "$disk | Set-Disk -IsOffline $true"
        )
        try:
            self._ps(script)
        except DriveError:
            pass

    def open_terminal_command(self, command: str) -> str:
        return f'Start-Process powershell -Verb RunAs -ArgumentList "{command}"'

    def _disk_number(self, drive: DriveInfo) -> int:
        # Extract number from \\.\PhysicalDriveN
        return int(drive.device.replace("\\\\.\\PhysicalDrive", ""))

    def _get_assigned_letter(self, disk_num: int) -> str:
        script = (
            f"(Get-Partition -DiskNumber {disk_num} | "
            "Where-Object { $_.DriveLetter } | "
            "Select-Object -First 1).DriveLetter"
        )
        letter = self._ps(script).strip()
        if not letter:
            raise FormatError(tr("platform.no_drive_letter"))
        return f"{letter}:\\"
