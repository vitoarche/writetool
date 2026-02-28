# WriteTool

Cross-platform Windows USB installer creator with a modern dark UI.

WriteTool writes Windows ISO images to USB drives using native OS tools for maximum performance. It supports UEFI and Legacy BIOS boot modes, automatic handling of large `install.wim` files (>4 GB), and multiple languages.

## Features

- **Cross-platform** — macOS, Linux, Windows
- **Native performance** — uses `hdiutil`/`mount`/`Mount-DiskImage` for ISO mounting, `cp`/`rsync`/`robocopy` for file copying
- **UEFI & Legacy BIOS** boot support
- **Automatic WIM handling** — splits `install.wim` via wimlib or creates a dual-partition layout when the file exceeds FAT32's 4 GB limit
- **SHA256 checksum** verification for ISO files
- **Multi-language** — English, Turkish, Russian, Chinese, German, French
- **Catppuccin Mocha** dark theme

## Screenshots

*Coming soon*

## Requirements

- Python 3.10+
- Administrator/root privileges (required for USB write operations)

### Platform-specific

| Platform | ISO Mount | Format | Additional |
|----------|-----------|--------|------------|
| macOS    | `hdiutil` | `diskutil` | — |
| Linux    | `mount`   | `parted`, `mkfs` | — |
| Windows  | PowerShell `Mount-DiskImage` | `diskpart` | — |

### Optional

- **wimlib** — for splitting large `install.wim` files (>4 GB)
  - macOS: `brew install wimlib`
  - Linux: `sudo apt install wimtools`
  - Windows: [wimlib.net/downloads](https://wimlib.net/downloads/)

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/vitoarche/writetool.git
cd writetool
pip install -e .
```

### Run directly

```bash
# From the project directory
pip install PySide6 pycdlib psutil
PYTHONPATH=src python3 -m writetool.app
```

### Build standalone executable

```bash
# Install build dependencies
pip install pyinstaller PySide6 pycdlib psutil

# Build for your platform
./build.sh
```

Output locations:
- **macOS**: `dist/WriteTool.app`
- **Linux**: `dist/WriteTool`
- **Windows**: `dist/WriteTool.exe`

## Usage

1. Launch WriteTool (requires admin/root)
2. Select your language
3. Browse and select a Windows ISO file
4. Select the target USB drive
5. Choose boot mode (UEFI or Legacy BIOS)
6. Click **Start Writing**

> **Warning**: All data on the selected USB drive will be erased.

## Project Structure

```
src/writetool/
├── app.py                 # Entry point, language dialog, privilege check
├── core/
│   ├── checksum.py        # SHA256 checksum computation
│   ├── exceptions.py      # Custom exception classes
│   ├── iso_handler.py     # ISO file validation
│   ├── wim_splitter.py    # WIM file splitting via wimlib
│   └── writer_engine.py   # Main write pipeline orchestrator
├── i18n/
│   ├── manager.py         # Translation manager
│   └── langs/             # Language files (en, tr, ru, zh, de, fr)
├── platform/
│   ├── base.py            # Abstract platform backend
│   ├── detector.py        # Platform auto-detection
│   ├── macos.py           # macOS backend
│   ├── linux.py           # Linux backend
│   └── windows.py         # Windows backend
├── ui/
│   ├── main_window.py     # Main application window
│   ├── iso_selector.py    # ISO file selector widget
│   ├── drive_selector.py  # USB drive selector widget
│   ├── settings_panel.py  # Boot mode & partition settings
│   ├── progress_panel.py  # Progress bar & log panel
│   ├── dialogs.py         # Confirmation & message dialogs
│   └── styles.py          # Catppuccin Mocha QSS stylesheet
├── utils/
│   ├── constants.py       # App constants & stage labels
│   ├── formatting.py      # Size formatting utilities
│   └── privileges.py      # Admin privilege check & elevation
└── workers/
    ├── base_worker.py     # Base QThread worker
    ├── write_worker.py    # USB write worker thread
    ├── checksum_worker.py # Checksum worker thread
    └── scan_worker.py     # USB scan worker thread
```

## License

MIT License. See [LICENSE](LICENSE) for details.
