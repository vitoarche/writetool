"""Main write pipeline orchestrator.

Uses native OS tools for maximum performance:
- macOS: hdiutil mount + rsync
- Linux: mount -o loop + rsync
- Windows: mount ISO + robocopy
"""

from __future__ import annotations

import os
import platform
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from writetool.core.exceptions import (
    ISOError,
    WriteCancelledError,
    WriteError,
    WriteToolError,
)
from writetool.core.wim_splitter import is_wimlib_available, split_wim
from writetool.i18n import tr
from writetool.platform.base import DriveInfo, PlatformBackend
from writetool.utils.constants import (
    BOOT_MODE_LEGACY,
    BOOT_MODE_UEFI,
    FAT32_MAX_FILE_SIZE,
    PARTITION_AUTO,
    PARTITION_DUAL,
    PARTITION_WIM_SPLIT,
    STAGE_COPY_FILES,
    STAGE_EJECT,
    STAGE_FORMAT,
    STAGE_PROCESS_WIM,
    STAGE_UNMOUNT,
    STAGE_VERIFY,
    get_stage_label,
)


@dataclass
class WriteConfig:
    """Configuration for a write operation."""

    iso_path: Path
    drive: DriveInfo
    boot_mode: str = BOOT_MODE_UEFI
    partition_strategy: str = PARTITION_AUTO
    verify_after_write: bool = True


@dataclass
class WriteProgress:
    """Current progress of the write operation."""

    stage: str = ""
    stage_label: str = ""
    current_file: str = ""
    bytes_written: int = 0
    total_bytes: int = 0
    percent: float = 0.0


ProgressCallback = Callable[[WriteProgress], None]
LogCallback = Callable[[str], None]


def _mount_iso(iso_path: Path) -> Path:
    """Mount an ISO file and return the mount point.

    Uses native OS tools for each platform.
    """
    system = platform.system()

    if system == "Darwin":
        result = subprocess.run(
            ["hdiutil", "mount", "-nobrowse", "-readonly", str(iso_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ISOError(tr("engine.iso_mount_error", error=result.stderr.strip()))
        # Parse mount point from output (last column of last line)
        for line in result.stdout.strip().splitlines():
            parts = line.split("\t")
            if len(parts) >= 3:
                mount_point = parts[-1].strip()
                if mount_point and Path(mount_point).exists():
                    return Path(mount_point)
        raise ISOError(tr("engine.iso_mount_not_found"))

    elif system == "Linux":
        mount_dir = Path(tempfile.mkdtemp(prefix="writetool_iso_"))
        result = subprocess.run(
            ["mount", "-o", "loop,ro", str(iso_path), str(mount_dir)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            mount_dir.rmdir()
            raise ISOError(tr("engine.iso_mount_error", error=result.stderr.strip()))
        return mount_dir

    elif system == "Windows":
        escaped = str(iso_path).replace("'", "''")
        result = subprocess.run(
            [
                "powershell",
                "-NoProfile",
                "-Command",
                f"(Mount-DiskImage -ImagePath '{escaped}' -PassThru | "
                "Get-Volume).DriveLetter",
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise ISOError(tr("engine.iso_mount_error", error=result.stderr.strip()))
        letter = result.stdout.strip()
        return Path(f"{letter}:\\")

    raise ISOError(tr("engine.iso_unsupported", system=system))


def _unmount_iso(mount_point: Path, iso_path: Path | None = None) -> None:
    """Unmount a previously mounted ISO.

    Args:
        mount_point: The mount point path.
        iso_path: Original ISO file path (required on Windows for Dismount-DiskImage).
    """
    system = platform.system()

    if system == "Darwin":
        subprocess.run(
            ["hdiutil", "detach", str(mount_point), "-quiet"],
            capture_output=True,
            check=False,
        )
    elif system == "Linux":
        subprocess.run(
            ["umount", str(mount_point)],
            capture_output=True,
            check=False,
        )
        mount_point.rmdir()
    elif system == "Windows":
        if iso_path:
            escaped = str(iso_path).replace("'", "''")
            subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f"Dismount-DiskImage -ImagePath '{escaped}'",
                ],
                capture_output=True,
                check=False,
            )


def _get_install_wim_size(iso_mount: Path) -> int:
    """Find install.wim or install.esd and return its size."""
    wim = _get_install_wim_path(iso_mount)
    if wim:
        try:
            return wim.stat().st_size
        except OSError:
            return 0
    return 0


def _get_install_wim_path(iso_mount: Path) -> Path | None:
    """Find install.wim or install.esd path (case-insensitive)."""
    for name in ("install.wim", "install.esd"):
        found = _find_case_insensitive(iso_mount, "sources", name)
        if found:
            return found
    return None


def _find_case_insensitive(base: Path, *parts: str) -> Path | None:
    """Find a path under base matching parts case-insensitively.

    Returns the resolved Path if found, None otherwise.
    """
    current = base
    for part in parts:
        found = None
        try:
            for child in current.iterdir():
                if child.name.lower() == part.lower():
                    found = child
                    break
        except OSError:
            return None
        if found is None:
            return None
        current = found
    return current


def _has_efi_boot(iso_mount: Path) -> bool:
    """Check if the ISO has UEFI boot files."""
    return _find_case_insensitive(iso_mount, "efi", "boot", "bootx64.efi") is not None


def _dir_total_size(path: Path) -> int:
    """Get total size of all files in a directory tree."""
    total = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = Path(dirpath) / f
            try:
                total += fp.stat().st_size
            except OSError:
                pass
    return total


class WriterEngine:
    """Orchestrates the full USB write pipeline.

    Uses native ISO mounting and rsync/cp for fast file copy
    instead of pycdlib which is much slower.
    """

    def __init__(
        self,
        backend: PlatformBackend,
        progress_callback: ProgressCallback | None = None,
        log_callback: LogCallback | None = None,
    ):
        self._backend = backend
        self._progress_cb = progress_callback
        self._log_cb = log_callback
        self._cancelled = False
        self._copy_proc: subprocess.Popen | None = None

    def cancel(self) -> None:
        """Request cancellation of the current write operation."""
        self._cancelled = True
        if self._copy_proc and self._copy_proc.poll() is None:
            self._copy_proc.terminate()

    @property
    def is_cancelled(self) -> bool:
        return self._cancelled

    def write(self, config: WriteConfig) -> None:
        """Execute the full write pipeline."""
        self._cancelled = False
        iso_mount: Path | None = None

        try:
            # Mount ISO natively
            self._log(tr("engine.mounting_iso"))
            iso_mount = _mount_iso(config.iso_path)
            self._log(tr("engine.iso_mount", path=iso_mount))

            # Analyze mounted ISO
            wim_size = _get_install_wim_size(iso_mount)
            wim_path = _get_install_wim_path(iso_mount)
            has_efi = _has_efi_boot(iso_mount)
            total_size = _dir_total_size(iso_mount)
            is_wim_oversized = wim_size > FAT32_MAX_FILE_SIZE

            from writetool.utils.formatting import format_size
            self._log(
                f"ISO: {format_size(total_size)}, "
                f"install.wim: {format_size(wim_size)}, "
                f"EFI: {has_efi}"
            )

            # Determine strategy
            strategy = self._resolve_strategy(config, is_wim_oversized)
            self._log(tr("engine.strategy", strategy=strategy))

            # Stage 1: Unmount USB
            self._check_cancel()
            self._set_stage(STAGE_UNMOUNT, 0, 0)
            self._log(tr("engine.unmounting_drive"))
            self._backend.unmount_drive(config.drive)

            # Stage 2: Format
            self._check_cancel()
            self._set_stage(STAGE_FORMAT, 0, 0)
            usb_mount, data_mount = self._format_drive(config, strategy)
            self._log(tr("engine.usb_mount", path=usb_mount))

            # Stage 3: Copy files
            self._check_cancel()
            self._set_stage(STAGE_COPY_FILES, 0, total_size)

            skip_wim = strategy in (PARTITION_WIM_SPLIT, PARTITION_DUAL)
            self._copy_files(iso_mount, usb_mount, total_size, skip_wim, wim_path)

            # Stage 4: Handle WIM if needed
            if skip_wim and wim_path:
                self._check_cancel()
                self._set_stage(STAGE_PROCESS_WIM, 0, wim_size)
                self._handle_wim(wim_path, strategy, usb_mount, data_mount)

            # Stage 5: Verify
            if config.verify_after_write:
                self._check_cancel()
                self._set_stage(STAGE_VERIFY, 0, 0)
                self._log(tr("engine.verifying"))
                self._verify(usb_mount, has_efi)

            # Stage 6: Eject
            self._set_stage(STAGE_EJECT, 0, 0)
            self._log(tr("engine.ejecting"))
            try:
                self._backend.eject_drive(config.drive)
            except WriteToolError:
                self._log(tr("engine.eject_failed"))

            self._log(tr("engine.write_complete"))

        finally:
            if iso_mount:
                try:
                    _unmount_iso(iso_mount, config.iso_path)
                except Exception as e:
                    self._log(f"ISO unmount warning: {e}")

    def _resolve_strategy(self, config: WriteConfig, is_wim_oversized: bool) -> str:
        if config.partition_strategy != PARTITION_AUTO:
            return config.partition_strategy
        if not is_wim_oversized:
            return PARTITION_AUTO
        if is_wimlib_available():
            return PARTITION_WIM_SPLIT
        return PARTITION_DUAL

    def _format_drive(
        self, config: WriteConfig, strategy: str
    ) -> tuple[Path, Path | None]:
        if config.boot_mode == BOOT_MODE_LEGACY:
            self._log(tr("engine.format_mbr_exfat"))
            part = self._backend.format_drive_mbr_ntfs(config.drive)
            mount = self._backend.mount_partition(part)
            return mount, None

        if strategy == PARTITION_DUAL:
            self._log(tr("engine.format_gpt_dual"))
            boot_part, data_part = self._backend.format_drive_dual(config.drive)
            boot_mount = self._backend.mount_partition(boot_part)
            data_mount = self._backend.mount_partition(data_part)
            return boot_mount, data_mount

        self._log(tr("engine.format_gpt_fat32"))
        part = self._backend.format_drive_gpt_fat32(config.drive)
        mount = self._backend.mount_partition(part)
        return mount, None

    def _copy_files(
        self,
        iso_mount: Path,
        usb_mount: Path,
        total_size: int,
        skip_wim: bool,
        wim_path: Path | None,
    ) -> None:
        """Copy files from mounted ISO to USB.

        Uses 'cp' for reliability on macOS (rsync 2.x has FAT32 temp-file issues).
        Tracks progress by polling destination size.
        """
        self._log(tr("engine.copying_files"))

        # Build file list from ISO mount, excluding install.wim if needed
        skip_name = wim_path.name.lower() if (skip_wim and wim_path) else None
        file_count = 0
        bytes_copied = 0

        for dirpath, dirnames, filenames in os.walk(iso_mount):
            rel_dir = os.path.relpath(dirpath, iso_mount)
            dest_dir = usb_mount / rel_dir if rel_dir != "." else usb_mount
            dest_dir.mkdir(parents=True, exist_ok=True)

            for fname in filenames:
                if self._cancelled:
                    raise WriteCancelledError(tr("engine.copy_cancelled"))

                # Skip install.wim if strategy requires separate handling
                if skip_name and rel_dir.lower() == "sources" and fname.lower() == skip_name:
                    continue

                src = Path(dirpath) / fname
                dst = dest_dir / fname
                file_count += 1

                try:
                    src_size = src.stat().st_size
                    shutil.copy2(str(src), str(dst))
                    bytes_copied += src_size
                except OSError as e:
                    self._log(tr("engine.copy_warning", fname=fname, error=e))
                    continue

                # Emit progress every 20 files
                if file_count % 20 == 0:
                    pct = (bytes_copied / total_size * 100) if total_size > 0 else 0
                    self._emit_copy_progress(min(pct, 99), fname, total_size)

        self._emit_copy_progress(100, "", total_size)
        self._log(tr("engine.copy_done", count=file_count))

    def _emit_copy_progress(self, pct: float, speed: str, total_size: int):
        progress = WriteProgress(
            stage=STAGE_COPY_FILES,
            stage_label=get_stage_label(STAGE_COPY_FILES),
            current_file=speed,
            bytes_written=int(total_size * pct / 100),
            total_bytes=total_size,
            percent=pct,
        )
        if self._progress_cb:
            self._progress_cb(progress)

    @staticmethod
    def _get_rsync_version() -> float:
        """Detect rsync major.minor version."""
        try:
            result = subprocess.run(
                ["rsync", "--version"],
                capture_output=True,
                text=True,
                check=False,
            )
            match = re.search(r"version\s+(\d+)\.(\d+)", result.stdout)
            if match:
                return float(f"{match.group(1)}.{match.group(2)}")
        except FileNotFoundError:
            pass
        return 2.0  # conservative fallback

    def _handle_wim(
        self,
        wim_path: Path,
        strategy: str,
        usb_mount: Path,
        data_mount: Path | None,
    ) -> None:
        """Handle install.wim — split or copy to data partition."""
        if strategy == PARTITION_WIM_SPLIT:
            self._log(tr("engine.wim_splitting"))
            # Split directly from mounted ISO to USB — no temp copy needed
            sources_dir = usb_mount / "sources"
            sources_dir.mkdir(parents=True, exist_ok=True)
            swm_files = split_wim(wim_path, sources_dir)
            self._log(tr("engine.wim_split_done", count=len(swm_files)))

        elif strategy == PARTITION_DUAL and data_mount:
            self._log(tr("engine.wim_copying_data"))
            data_sources = data_mount / "sources"
            data_sources.mkdir(parents=True, exist_ok=True)
            dest = data_sources / wim_path.name
            self._log(tr("engine.wim_rsync", name=wim_path.name))
            result = subprocess.run(
                ["rsync", "-a", "--info=progress2", str(wim_path), str(dest)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode != 0:
                raise WriteError(tr("engine.wim_copy_error", error=result.stderr))
            self._log(tr("engine.wim_copied"))

    def _verify(self, usb_mount: Path, has_efi: bool) -> None:
        checks = [
            usb_mount / "sources",
            usb_mount / "boot",
        ]
        if has_efi:
            checks.append(usb_mount / "efi" / "boot" / "bootx64.efi")

        for path in checks:
            if not path.exists():
                self._log(tr("engine.verify_warning", path=path))

        self._log(tr("engine.verify_done"))

    def _set_stage(self, stage: str, current: int, total: int):
        progress = WriteProgress(
            stage=stage,
            stage_label=get_stage_label(stage),
            bytes_written=current,
            total_bytes=total,
            percent=(current / total * 100) if total > 0 else 0,
        )
        if self._progress_cb:
            self._progress_cb(progress)

    def _log(self, message: str):
        if self._log_cb:
            self._log_cb(message)

    def _check_cancel(self):
        if self._cancelled:
            raise WriteCancelledError(tr("engine.cancel"))
