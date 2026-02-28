"""WIM file splitting using wimlib-imagex."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from writetool.core.exceptions import WimError, WimlibNotFoundError
from writetool.utils.constants import WIM_SPLIT_SIZE_MB


def is_wimlib_available() -> bool:
    """Check if wimlib-imagex is installed and accessible."""
    return shutil.which("wimlib-imagex") is not None


def get_wimlib_path() -> str:
    """Return the path to wimlib-imagex, or raise if not found."""
    path = shutil.which("wimlib-imagex")
    if path is None:
        raise WimlibNotFoundError(
            "wimlib-imagex bulunamadı. Lütfen wimlib paketini kurun:\n"
            "  macOS:   brew install wimlib\n"
            "  Linux:   sudo apt install wimtools\n"
            "  Windows: https://wimlib.net/downloads/"
        )
    return path


def split_wim(
    wim_path: Path,
    output_dir: Path,
    split_size_mb: int = WIM_SPLIT_SIZE_MB,
    output_name: str = "install",
) -> list[Path]:
    """Split a WIM file into .swm parts.

    Args:
        wim_path: Path to the source .wim file.
        output_dir: Directory to place the .swm files.
        split_size_mb: Maximum size of each part in MB.
        output_name: Base name for output files.

    Returns:
        List of paths to the generated .swm files.
    """
    wimlib = get_wimlib_path()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_pattern = output_dir / f"{output_name}.swm"

    result = subprocess.run(
        [
            wimlib,
            "split",
            str(wim_path),
            str(output_pattern),
            str(split_size_mb),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        raise WimError(f"WIM bölme hatası: {result.stderr.strip()}")

    # Collect output files: install.swm, install2.swm, install3.swm, ...
    swm_files = sorted(output_dir.glob(f"{output_name}*.swm"))
    if not swm_files:
        raise WimError("WIM bölme sonrası .swm dosyaları bulunamadı.")

    return swm_files
