"""English translations."""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "Privileges Required",
    "app.privilege_message": "WriteTool requires administrator privileges to write to USB drives.",
    "app.privilege_error_title": "Error",
    "app.privilege_error_message": "Failed to obtain admin privileges. The app cannot run without admin privileges.",
    "app.continue_button": "Continue",

    # -- main_window.py --
    "main.start_button": "Start Writing",
    "main.cancel_button": "Cancel",
    "main.cancel_requested": "Cancellation requested...",
    "main.completed": "Completed!",
    "main.cancelled": "Cancelled.",
    "main.error_status": "Error: {message}",
    "main.write_error_title": "Write Error",

    # -- dialogs.py --
    "dialog.confirm_title": "Write Confirmation",
    "dialog.confirm_warning": "ALL DATA on <b>{drive_name}</b> will be ERASED!",
    "dialog.confirm_detail": "<b>{iso_name}</b> will be written to <b>{name}</b> ({size}).\n\nThis operation cannot be undone. Do you want to continue?",
    "dialog.confirm_yes": "Yes, Write",
    "dialog.confirm_no": "Cancel",
    "dialog.success_title": "Completed",
    "dialog.success_message": "USB write completed successfully!",
    "dialog.success_detail": "You can safely eject the USB drive.",

    # -- drive_selector.py --
    "drive.group_title": "Target USB",
    "drive.refresh": "Refresh",
    "drive.scanning": "Scanning...",
    "drive.not_found": "No USB drives found",
    "drive.not_found_hint": "Insert a USB drive and click Refresh.",
    "drive.found_count": "{count} drive(s) found.",
    "drive.scan_error": "Scan error",

    # -- iso_selector.py --
    "iso.group_title": "ISO File",
    "iso.placeholder": "Select a Windows ISO file...",
    "iso.browse": "Browse...",
    "iso.checksum_none": "SHA256: —",
    "iso.verify": "Verify",
    "iso.file_dialog_title": "Select ISO File",
    "iso.file_filter": "ISO Files (*.iso);;All Files (*)",
    "iso.checksum_computing": "SHA256: computing...",
    "iso.checksum_result": "SHA256: {hash}",
    "iso.checksum_error": "SHA256: error — {message}",
    "iso.checksum_progress": "SHA256: computing... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "Options",
    "settings.boot_label": "Boot:",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "Partition:",
    "settings.partition_auto": "Automatic",
    "settings.partition_wim_split": "Split WIM",
    "settings.partition_dual": "Dual Partition",
    "settings.wimlib_missing": "wimlib-imagex not found. Install:\n  macOS: brew install wimlib\n  Linux: sudo apt install wimtools",
    "settings.language_label": "Language:",

    # -- progress_panel.py --
    "progress.group_title": "Progress",

    # -- constants.py / stage labels --
    "stage.unmount": "Unmounting...",
    "stage.format": "Formatting...",
    "stage.extract_boot": "Extracting boot files...",
    "stage.copy_files": "Copying files...",
    "stage.process_wim": "Processing install.wim...",
    "stage.verify": "Verifying...",
    "stage.eject": "Ejecting...",

    # -- writer_engine.py --
    "engine.mounting_iso": "Mounting ISO...",
    "engine.iso_mount": "ISO mount: {path}",
    "engine.strategy": "Strategy: {strategy}",
    "engine.unmounting_drive": "Unmounting drive...",
    "engine.usb_mount": "USB mount: {path}",
    "engine.verifying": "Verifying...",
    "engine.eject_failed": "Eject failed, you can remove the drive manually.",
    "engine.write_complete": "Write operation completed!",
    "engine.format_mbr_exfat": "Formatting: MBR + ExFAT...",
    "engine.format_gpt_dual": "Formatting: GPT + FAT32 (boot) + ExFAT (data)...",
    "engine.format_gpt_fat32": "Formatting: GPT + FAT32...",
    "engine.copying_files": "Copying files...",
    "engine.copy_cancelled": "Copy cancelled.",
    "engine.copy_warning": "WARNING: Could not copy {fname}: {error}",
    "engine.copy_done": "File copy completed ({count} files).",
    "engine.wim_splitting": "Splitting install.wim (wimlib-imagex)...",
    "engine.wim_split_done": "WIM split into {count} parts.",
    "engine.wim_copying_data": "Copying install.wim to data partition...",
    "engine.wim_rsync": "Copying with rsync: {name}...",
    "engine.wim_copy_error": "WIM copy error: {error}",
    "engine.wim_copied": "install.wim copied.",
    "engine.verify_warning": "WARNING: Expected file/folder not found: {path}",
    "engine.verify_done": "Verification completed.",
    "engine.cancel": "Write operation cancelled by user.",
    "engine.iso_mount_error": "ISO mount error: {error}",
    "engine.iso_mount_not_found": "ISO mount point not found.",
    "engine.iso_unsupported": "ISO mounting not supported: {system}",
    "engine.ejecting": "Ejecting...",

    # -- wim_splitter.py --
    "wim.not_found": "wimlib-imagex not found. Please install wimlib:\n  macOS:   brew install wimlib\n  Linux:   sudo apt install wimtools\n  Windows: https://wimlib.net/downloads/",
    "wim.split_error": "WIM split error: {error}",
    "wim.no_swm_files": "No .swm files found after WIM split.",

    # -- iso_handler.py --
    "iso.not_found_error": "ISO not found: {path}",
    "iso.invalid_error": "Invalid ISO file: {error}",

    # -- scan_worker.py --
    "scan.scanning": "Scanning for USB drives...",
    "scan.found": "{count} USB drive(s) found.",
    "scan.error": "USB scan error: {error}",

    # -- checksum_worker.py --
    "checksum.computing": "Computing {algorithm}...",
    "checksum.cancelled": "Checksum computation cancelled.",
    "checksum.result": "{algorithm}: {digest}",
    "checksum.error": "Checksum error: {error}",

    # -- write_worker.py --
    "write.cancelled": "Write operation cancelled.",

    # -- platform/macos.py --
    "platform.unmount_failed": "Failed to unmount '{device}': {error}",
    "platform.format_error": "Format error: {error}",
    "platform.dual_format_error": "Dual format error: {error}",
    "platform.mount_error": "Mount error: {error}",
    "platform.mount_not_found": "Mount point not found: {device}",
    "platform.partition_not_found": "Partition with label '{label}' not found: {device}",
    "platform.eject_error": "Eject error: {error}",

    # -- platform/linux.py --
    "platform.command_failed": "Command failed: {command}\n{error}",

    # -- platform/windows.py --
    "platform.powershell_error": "PowerShell error: {error}",
    "platform.diskpart_error": "Diskpart error: {error}",
    "platform.dual_no_letters": "Dual partition created but drive letters could not be assigned.",
    "platform.no_drive_letter": "Drive letter could not be assigned.",
}
