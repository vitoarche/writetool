"""OS detection and platform backend factory."""

import platform

from writetool.core.exceptions import PlatformNotSupportedError
from writetool.platform.base import PlatformBackend


def detect_platform() -> str:
    """Return the current platform identifier: 'macos', 'linux', or 'windows'."""
    system = platform.system()
    if system == "Darwin":
        return "macos"
    elif system == "Linux":
        return "linux"
    elif system == "Windows":
        return "windows"
    raise PlatformNotSupportedError(f"Unsupported platform: {system}")


def get_backend() -> PlatformBackend:
    """Return the appropriate PlatformBackend for the current OS."""
    plat = detect_platform()
    if plat == "macos":
        from writetool.platform.macos import MacOSBackend
        return MacOSBackend()
    elif plat == "linux":
        from writetool.platform.linux import LinuxBackend
        return LinuxBackend()
    elif plat == "windows":
        from writetool.platform.windows import WindowsBackend
        return WindowsBackend()
    raise PlatformNotSupportedError(f"No backend for: {plat}")
