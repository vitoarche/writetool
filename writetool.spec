# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for WriteTool — cross-platform."""

import platform

block_cipher = None

a = Analysis(
    ["src/writetool/__main__.py"],
    pathex=["src"],
    binaries=[],
    datas=[],
    hiddenimports=[
        "writetool",
        "writetool.app",
        "writetool.core",
        "writetool.core.checksum",
        "writetool.core.exceptions",
        "writetool.core.iso_handler",
        "writetool.core.wim_splitter",
        "writetool.core.writer_engine",
        "writetool.platform",
        "writetool.platform.base",
        "writetool.platform.detector",
        "writetool.platform.macos",
        "writetool.platform.linux",
        "writetool.platform.windows",
        "writetool.workers",
        "writetool.workers.base_worker",
        "writetool.workers.write_worker",
        "writetool.workers.checksum_worker",
        "writetool.workers.scan_worker",
        "writetool.ui",
        "writetool.ui.main_window",
        "writetool.ui.drive_selector",
        "writetool.ui.iso_selector",
        "writetool.ui.progress_panel",
        "writetool.ui.settings_panel",
        "writetool.ui.dialogs",
        "writetool.ui.styles",
        "writetool.utils",
        "writetool.utils.constants",
        "writetool.utils.formatting",
        "writetool.utils.privileges",
        "writetool.i18n",
        "writetool.i18n.manager",
        "writetool.i18n.langs",
        "writetool.i18n.langs.tr",
        "writetool.i18n.langs.en",
        "writetool.i18n.langs.ru",
        "writetool.i18n.langs.zh",
        "writetool.i18n.langs.de",
        "writetool.i18n.langs.fr",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "scipy", "PIL"],
    noarchive=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, cipher=block_cipher)

system = platform.system()

if system == "Darwin":
    exe = EXE(
        pyz,
        a.scripts,
        [],
        exclude_binaries=True,
        name="WriteTool",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=False,
        console=False,
        target_arch=None,
    )
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=False,
        name="WriteTool",
    )
    app = BUNDLE(
        coll,
        name="WriteTool.app",
        icon=None,
        bundle_identifier="com.writetool.app",
        info_plist={
            "CFBundleName": "WriteTool",
            "CFBundleDisplayName": "WriteTool",
            "CFBundleShortVersionString": "0.1.0",
            "CFBundleVersion": "0.1.0",
            "NSHighResolutionCapable": True,
            "LSMinimumSystemVersion": "11.0",
        },
    )

elif system == "Windows":
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name="WriteTool",
        debug=False,
        bootloader_ignore_signals=False,
        strip=False,
        upx=True,
        console=False,
        icon=None,
        uac_admin=True,  # Request admin on launch
    )

else:  # Linux
    exe = EXE(
        pyz,
        a.scripts,
        a.binaries,
        a.datas,
        [],
        name="WriteTool",
        debug=False,
        strip=True,
        upx=True,
        console=False,
    )
