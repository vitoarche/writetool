"""ISO reading and file extraction using pycdlib."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import pycdlib

from writetool.core.exceptions import InvalidISOError, ISONotFoundError
from writetool.i18n import tr
from writetool.utils.constants import (
    FAT32_MAX_FILE_SIZE,
    INSTALL_ESD_PATH,
    INSTALL_WIM_PATH,
    ISO_TYPE_LINUX,
    ISO_TYPE_MACOS,
    ISO_TYPE_UNKNOWN,
    ISO_TYPE_WINDOWS,
)


@dataclass
class ISOInfo:
    """Information about an ISO file."""

    path: Path
    total_size: int
    file_count: int
    install_wim_size: int  # 0 if not found
    has_efi_boot: bool
    is_wim_oversized: bool  # install.wim > 4GB
    iso_type: str = ISO_TYPE_UNKNOWN


_WINDOWS_MARKERS = {"/sources/install.wim", "/sources/install.esd"}
_MACOS_MARKERS = {"/basesystem.dmg", "/installesd.dmg", "/system/library/"}
_LINUX_MARKERS = {"/isolinux/", "/casper/", "/liveos/", "/.disk/info", "/boot/grub/"}


def _detect_iso_type(paths: set[str]) -> str:
    """Detect ISO type from a set of lowercase file/directory paths."""
    # Windows: has install.wim or install.esd
    for marker in _WINDOWS_MARKERS:
        if any(p == marker or p.startswith(marker + "/") for p in paths):
            return ISO_TYPE_WINDOWS

    # macOS: has basesystem.dmg, installesd.dmg, or system/library/
    for marker in _MACOS_MARKERS:
        if any(p == marker or p.startswith(marker) for p in paths):
            return ISO_TYPE_MACOS

    # Linux: has isolinux/, casper/, liveos/, .disk/info, or boot/grub/
    for marker in _LINUX_MARKERS:
        if any(p == marker or p.startswith(marker) for p in paths):
            return ISO_TYPE_LINUX

    return ISO_TYPE_UNKNOWN


class ISOHandler:
    """Reads and extracts files from an ISO image."""

    def __init__(self, iso_path: Path):
        if not iso_path.exists():
            raise ISONotFoundError(tr("iso.not_found_error", path=iso_path))
        self.iso_path = iso_path
        self._iso: pycdlib.PyCdlib | None = None

    def open(self) -> None:
        """Open the ISO file for reading."""
        self._iso = pycdlib.PyCdlib()
        try:
            self._iso.open(str(self.iso_path))
        except Exception as e:
            self._iso = None
            raise InvalidISOError(tr("iso.invalid_error", error=e)) from e

    def close(self) -> None:
        """Close the ISO file."""
        if self._iso:
            self._iso.close()
            self._iso = None

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args):
        self.close()

    def get_info(self) -> ISOInfo:
        """Analyze the ISO and return summary info."""
        iso = self._ensure_open()
        total_size = 0
        file_count = 0
        install_wim_size = 0
        has_efi = False
        all_paths: set[str] = set()

        facade = self._get_facade(iso)

        for dirpath, dirnames, filenames in facade.walk("/"):
            # Collect directory paths for type detection
            for dname in dirnames:
                all_paths.add(self._join_path(dirpath, dname).lower() + "/")

            for fname in filenames:
                file_count += 1
                full_path = self._join_path(dirpath, fname)
                lower = full_path.lower()
                all_paths.add(lower)

                try:
                    size = self._file_size(iso, facade, full_path)
                    total_size += size
                except Exception:
                    continue

                if lower == INSTALL_WIM_PATH or lower == INSTALL_ESD_PATH:
                    install_wim_size = size
                if "/efi/boot/bootx64.efi" in lower:
                    has_efi = True

        iso_type = _detect_iso_type(all_paths)

        return ISOInfo(
            path=self.iso_path,
            total_size=total_size,
            file_count=file_count,
            install_wim_size=install_wim_size,
            has_efi_boot=has_efi,
            is_wim_oversized=install_wim_size > FAT32_MAX_FILE_SIZE,
            iso_type=iso_type,
        )

    def extract_all(
        self,
        dest: Path,
        skip_wim: bool = False,
        progress_callback: Callable[[str, int, int], None] | None = None,
        cancel_check: Callable[[], bool] | None = None,
    ) -> None:
        """Extract all files from ISO to destination.

        Args:
            dest: Destination directory.
            skip_wim: If True, skip install.wim/install.esd (for separate handling).
            progress_callback: Called with (current_file, bytes_extracted, total_bytes).
            cancel_check: If returns True, abort extraction.
        """
        iso = self._ensure_open()
        facade = self._get_facade(iso)

        # First pass: calculate total size
        total_size = 0
        files_to_extract: list[tuple[str, int]] = []

        for dirpath, _, filenames in facade.walk("/"):
            for fname in filenames:
                full_path = self._join_path(dirpath, fname)
                try:
                    size = self._file_size(iso, facade, full_path)
                except Exception:
                    continue

                lower = full_path.lower()
                if skip_wim and (lower == INSTALL_WIM_PATH or lower == INSTALL_ESD_PATH):
                    continue

                files_to_extract.append((full_path, size))
                total_size += size

        # Second pass: extract
        extracted = 0
        for iso_file_path, size in files_to_extract:
            if cancel_check and cancel_check():
                return

            # Build destination path
            rel = iso_file_path.lstrip("/")
            out_path = dest / rel
            out_path.parent.mkdir(parents=True, exist_ok=True)

            if progress_callback:
                progress_callback(rel, extracted, total_size)

            self._extract_file(iso, facade, iso_file_path, out_path)
            extracted += size

        if progress_callback:
            progress_callback("", total_size, total_size)

    def extract_file(self, iso_path: str, dest_path: Path) -> None:
        """Extract a single file from the ISO."""
        iso = self._ensure_open()
        facade = self._get_facade(iso)
        dest_path.parent.mkdir(parents=True, exist_ok=True)
        self._extract_file(iso, facade, iso_path, dest_path)

    def _ensure_open(self) -> pycdlib.PyCdlib:
        if self._iso is None:
            self.open()
        return self._iso  # type: ignore

    def _get_facade(self, iso: pycdlib.PyCdlib):
        """Get the best facade: prefer UDF, then Joliet, then Rock Ridge."""
        if iso.has_udf():
            return _UDFFacade(iso)
        if iso.has_joliet():
            return _JolietFacade(iso)
        return _RockRidgeFacade(iso)

    def _file_size(self, iso: pycdlib.PyCdlib, facade, path: str) -> int:
        return facade.file_size(path)

    def _extract_file(self, iso: pycdlib.PyCdlib, facade, iso_path: str, out: Path):
        facade.extract(iso_path, str(out))

    def _join_path(self, dirpath: str, fname: str) -> str:
        if dirpath.endswith("/"):
            return dirpath + fname
        return dirpath + "/" + fname


def _decode_udf_name(raw: bytes) -> str:
    """Decode a UDF file identifier from raw bytes.

    UDF names are typically UTF-16BE with a leading compression byte:
      0x08 = UTF-8, 0x10 = UTF-16BE.
    """
    if not raw:
        return ""
    if raw[0:1] == b"\x10" and len(raw) > 1:
        return raw[1:].decode("utf-16-be", errors="replace")
    if raw[0:1] == b"\x08" and len(raw) > 1:
        return raw[1:].decode("utf-8", errors="replace")
    # Fallback: try utf-16-be stripping null bytes
    try:
        return raw.decode("utf-16-be", errors="replace").replace("\x00", "")
    except Exception:
        return raw.decode("ascii", errors="replace")


class _UDFFacade:
    def __init__(self, iso: pycdlib.PyCdlib):
        self._iso = iso
        self._size_cache: dict[str, int] = {}

    def walk(self, path: str):
        yield from self._walk_udf(path)

    def _walk_udf(self, path: str):
        dirs: list[str] = []
        files: list[str] = []
        try:
            for child in self._iso.list_children(udf_path=path):
                if child is None:
                    continue
                raw_name = child.file_identifier()
                name = _decode_udf_name(raw_name)
                if not name or name in (".", ".."):
                    continue
                full = path.rstrip("/") + "/" + name
                size = child.get_data_length()
                self._size_cache[full.lower()] = size
                if child.is_dir():
                    dirs.append(name)
                else:
                    files.append(name)
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            return

        yield path, dirs, files
        for d in dirs:
            subpath = path.rstrip("/") + "/" + d
            yield from self._walk_udf(subpath)

    def file_size(self, path: str) -> int:
        cached = self._size_cache.get(path.lower())
        if cached is not None:
            return cached
        # Fallback: list parent dir
        parent = "/".join(path.split("/")[:-1]) or "/"
        fname = path.split("/")[-1].lower()
        try:
            for child in self._iso.list_children(udf_path=parent):
                if child is None:
                    continue
                cname = _decode_udf_name(child.file_identifier())
                if cname.lower() == fname and not child.is_dir():
                    return child.get_data_length()
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            pass
        return 0

    def extract(self, iso_path: str, dest: str):
        self._iso.get_file_from_iso(dest, udf_path=iso_path)


class _JolietFacade:
    def __init__(self, iso: pycdlib.PyCdlib):
        self._iso = iso

    def walk(self, path: str):
        yield from self._walk_joliet(path)

    def _walk_joliet(self, path: str):
        dirs = []
        files = []
        try:
            for child in self._iso.list_children(joliet_path=path):
                if child is None:
                    continue
                name = child.file_identifier.decode("utf-8", errors="replace")
                if name in (".", "..") or name == "\x00":
                    continue
                if child.is_dir():
                    dirs.append(name)
                else:
                    files.append(name)
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            return

        yield path, dirs, files
        for d in dirs:
            subpath = path.rstrip("/") + "/" + d
            yield from self._walk_joliet(subpath)

    def file_size(self, path: str) -> int:
        parent = "/".join(path.split("/")[:-1]) or "/"
        fname = path.split("/")[-1]
        try:
            for child in self._iso.list_children(joliet_path=parent):
                if child is None:
                    continue
                cname = child.file_identifier.decode("utf-8", errors="replace")
                if cname == fname and not child.is_dir():
                    return child.data_length
        except pycdlib.pycdlibexception.PyCdlibInvalidInput:
            pass
        return 0

    def extract(self, iso_path: str, dest: str):
        self._iso.get_file_from_iso(dest, joliet_path=iso_path)


class _RockRidgeFacade:
    def __init__(self, iso: pycdlib.PyCdlib):
        self._iso = iso

    def walk(self, path: str):
        yield from self._walk_rr(path)

    def _walk_rr(self, path: str):
        dirs = []
        files = []
        try:
            for child in self._iso.list_children(rr_path=path):
                if child is None:
                    continue
                name = child.file_identifier.decode("utf-8", errors="replace")
                if name in (".", "..") or name == "\x00":
                    continue
                if child.is_dir():
                    dirs.append(name)
                else:
                    files.append(name)
        except (pycdlib.pycdlibexception.PyCdlibInvalidInput, AttributeError):
            return

        yield path, dirs, files
        for d in dirs:
            subpath = path.rstrip("/") + "/" + d
            yield from self._walk_rr(subpath)

    def file_size(self, path: str) -> int:
        parent = "/".join(path.split("/")[:-1]) or "/"
        fname = path.split("/")[-1]
        try:
            for child in self._iso.list_children(rr_path=parent):
                if child is None:
                    continue
                cname = child.file_identifier.decode("utf-8", errors="replace")
                if cname == fname and not child.is_dir():
                    return child.data_length
        except (pycdlib.pycdlibexception.PyCdlibInvalidInput, AttributeError):
            pass
        return 0

    def extract(self, iso_path: str, dest: str):
        try:
            self._iso.get_file_from_iso(dest, rr_path=iso_path)
        except (pycdlib.pycdlibexception.PyCdlibInvalidInput, AttributeError):
            self._iso.get_file_from_iso(dest, iso_path=iso_path)
