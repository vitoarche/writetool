"""Admin/root privilege checking and elevation."""

import os
import shutil
import sys
import platform


def is_admin() -> bool:
    """Check if the current process has admin/root privileges."""
    system = platform.system()
    if system in ("Linux", "Darwin"):
        return os.geteuid() == 0
    elif system == "Windows":
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  # type: ignore[attr-defined]
    return False


def request_elevation() -> bool:
    """Attempt to re-launch the application with elevated privileges.

    Returns True if elevation was initiated (current process should exit).
    Returns False if elevation could not be performed.
    """
    import subprocess

    system = platform.system()
    # Build the full command preserving PYTHONPATH so editable installs work
    python = sys.executable
    if getattr(sys, "frozen", False):
        # PyInstaller frozen app — re-run the binary itself
        args = [python, "--skip-lang"]
    else:
        args = [python, "-m", "writetool", "--skip-lang"]

    if system == "Darwin":
        # Use osascript to prompt for admin; pass PYTHONPATH for editable installs
        pythonpath = os.environ.get("PYTHONPATH", "")
        site_dir = _get_site_packages_dir()
        if site_dir and site_dir not in pythonpath:
            pythonpath = f"{site_dir}:{pythonpath}" if pythonpath else site_dir
        env_prefix = f"PYTHONPATH={pythonpath} " if pythonpath else ""
        # Run elevated command in background (&) so osascript returns immediately
        # after auth succeeds; if user cancels, osascript exits with error code.
        cmd_str = env_prefix + " ".join(args) + " &"
        try:
            result = subprocess.run(
                [
                    "osascript",
                    "-e",
                    f'do shell script "{cmd_str}" with administrator privileges',
                ],
                capture_output=True,
            )
            return result.returncode == 0
        except OSError:
            return False

    elif system == "Linux":
        for cmd in ("pkexec", "sudo"):
            path = shutil.which(cmd)
            if path:
                try:
                    subprocess.Popen([path] + args)
                    return True
                except OSError:
                    continue
        return False

    elif system == "Windows":
        import ctypes
        if getattr(sys, "frozen", False):
            ctypes.windll.shell32.ShellExecuteW(  # type: ignore[attr-defined]
                None, "runas", python, "--skip-lang", None, 1
            )
        else:
            ctypes.windll.shell32.ShellExecuteW(  # type: ignore[attr-defined]
                None, "runas", f'"{python}"', "-m writetool --skip-lang", None, 1
            )
        return True

    return False


def _get_site_packages_dir() -> str | None:
    """Get the site-packages directory containing writetool."""
    try:
        import writetool
        pkg_dir = os.path.dirname(os.path.dirname(writetool.__file__))
        return pkg_dir
    except Exception:
        return None
