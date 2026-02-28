#!/bin/bash
# Build WriteTool for the current platform
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "=== WriteTool Build ==="
echo "Platform: $(uname -s)"
echo ""

# Ensure dependencies
pip install pyinstaller PySide6 pycdlib psutil 2>/dev/null

# Clean previous build
rm -rf build dist

# Build
echo "Building..."
pyinstaller writetool.spec --noconfirm

echo ""
echo "=== Build Complete ==="

case "$(uname -s)" in
    Darwin)
        echo "Output: dist/WriteTool.app"
        echo "Run:    open dist/WriteTool.app"
        ;;
    Linux)
        echo "Output: dist/WriteTool"
        echo "Run:    ./dist/WriteTool"
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo "Output: dist/WriteTool.exe"
        echo "Run:    dist\\WriteTool.exe"
        ;;
esac
