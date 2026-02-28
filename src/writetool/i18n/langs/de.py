"""Deutsche Übersetzungen."""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "Berechtigung erforderlich",
    "app.privilege_message": "WriteTool benötigt Administratorrechte, um auf USB-Laufwerke zu schreiben.",
    "app.privilege_error_title": "Fehler",
    "app.privilege_error_message": "Administratorrechte konnten nicht erlangt werden. Die App kann ohne Administratorrechte nicht ausgeführt werden.",
    "app.continue_button": "Weiter",

    # -- main_window.py --
    "main.start_button": "Schreiben starten",
    "main.cancel_button": "Abbrechen",
    "main.cancel_requested": "Abbruch angefordert...",
    "main.completed": "Abgeschlossen!",
    "main.cancelled": "Abgebrochen.",
    "main.error_status": "Fehler: {message}",
    "main.write_error_title": "Schreibfehler",

    # -- dialogs.py --
    "dialog.confirm_title": "Schreibbestätigung",
    "dialog.confirm_warning": "ALLE DATEN auf <b>{drive_name}</b> werden GELÖSCHT!",
    "dialog.confirm_detail": "<b>{iso_name}</b> wird auf <b>{name}</b> ({size}) geschrieben.\n\nDieser Vorgang kann nicht rückgängig gemacht werden. Fortfahren?",
    "dialog.confirm_yes": "Ja, schreiben",
    "dialog.confirm_no": "Abbrechen",
    "dialog.dd_warning": "Dieses Image wird per Raw-Blockkopie (DD-Modus) geschrieben. Das gesamte Laufwerk wird mit dem Image-Inhalt überschrieben.",
    "dialog.success_title": "Abgeschlossen",
    "dialog.success_message": "USB-Schreibvorgang erfolgreich abgeschlossen!",
    "dialog.success_detail": "Sie können das USB-Laufwerk sicher entfernen.",

    # -- drive_selector.py --
    "drive.group_title": "Ziel-USB",
    "drive.refresh": "Aktualisieren",
    "drive.scanning": "Wird gescannt...",
    "drive.not_found": "Kein USB-Laufwerk gefunden",
    "drive.not_found_hint": "USB-Laufwerk einstecken und Aktualisieren klicken.",
    "drive.found_count": "{count} Laufwerk(e) gefunden.",
    "drive.scan_error": "Scanfehler",

    # -- iso_selector.py --
    "iso.group_title": "ISO-Datei",
    "iso.placeholder": "ISO-Datei auswählen...",
    "iso.browse": "Durchsuchen...",
    "iso.checksum_none": "SHA256: —",
    "iso.verify": "Prüfen",
    "iso.file_dialog_title": "ISO-Datei auswählen",
    "iso.file_filter": "Disk-Images (*.iso *.dmg *.img);;ISO-Dateien (*.iso);;Alle Dateien (*)",
    "iso.checksum_computing": "SHA256: wird berechnet...",
    "iso.checksum_result": "SHA256: {hash}",
    "iso.checksum_error": "SHA256: Fehler — {message}",
    "iso.checksum_progress": "SHA256: wird berechnet... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "Optionen",
    "settings.boot_label": "Boot:",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "Partition:",
    "settings.partition_auto": "Automatisch",
    "settings.partition_wim_split": "WIM aufteilen",
    "settings.partition_dual": "Doppelte Partition",
    "settings.wimlib_missing": "wimlib-imagex nicht gefunden. Installation:\n  macOS: brew install wimlib\n  Linux: sudo apt install wimtools",
    "settings.language_label": "Sprache:",
    "settings.iso_type_label": "ISO-Typ:",
    "settings.iso_type_windows": "Windows",
    "settings.iso_type_linux": "Linux",
    "settings.iso_type_macos": "macOS",
    "settings.iso_type_unknown": "Unbekannt",
    "settings.iso_type_detecting": "Erkennung...",
    "settings.dd_note": "Dieses Image wird per Raw-Blockkopie (DD) geschrieben. Boot-Modus und Partitionsoptionen gelten nicht.",

    # -- progress_panel.py --
    "progress.group_title": "Fortschritt",

    # -- constants.py / stage labels --
    "stage.unmount": "Wird ausgehängt...",
    "stage.format": "Wird formatiert...",
    "stage.extract_boot": "Boot-Dateien werden extrahiert...",
    "stage.copy_files": "Dateien werden kopiert...",
    "stage.process_wim": "install.wim wird verarbeitet...",
    "stage.dd_write": "Image wird geschrieben...",
    "stage.verify": "Wird überprüft...",
    "stage.eject": "Wird ausgeworfen...",

    # -- writer_engine.py --
    "engine.mounting_iso": "ISO wird eingehängt...",
    "engine.iso_mount": "ISO eingehängt: {path}",
    "engine.strategy": "Strategie: {strategy}",
    "engine.unmounting_drive": "Laufwerk wird ausgehängt...",
    "engine.usb_mount": "USB eingehängt: {path}",
    "engine.verifying": "Wird überprüft...",
    "engine.eject_failed": "Auswerfen fehlgeschlagen, bitte manuell entfernen.",
    "engine.write_complete": "Schreibvorgang abgeschlossen!",
    "engine.format_mbr_exfat": "Formatierung: MBR + ExFAT...",
    "engine.format_gpt_dual": "Formatierung: GPT + FAT32 (Boot) + ExFAT (Daten)...",
    "engine.format_gpt_fat32": "Formatierung: GPT + FAT32...",
    "engine.copying_files": "Dateien werden kopiert...",
    "engine.copy_cancelled": "Kopieren abgebrochen.",
    "engine.copy_warning": "WARNUNG: {fname} konnte nicht kopiert werden: {error}",
    "engine.copy_done": "Dateikopie abgeschlossen ({count} Dateien).",
    "engine.wim_splitting": "install.wim wird aufgeteilt (wimlib-imagex)...",
    "engine.wim_split_done": "WIM in {count} Teile aufgeteilt.",
    "engine.wim_copying_data": "install.wim wird auf Datenpartition kopiert...",
    "engine.wim_rsync": "Kopieren mit rsync: {name}...",
    "engine.wim_copy_error": "WIM-Kopierfehler: {error}",
    "engine.wim_copied": "install.wim kopiert.",
    "engine.verify_warning": "WARNUNG: Erwartete Datei/Ordner nicht gefunden: {path}",
    "engine.verify_done": "Überprüfung abgeschlossen.",
    "engine.cancel": "Schreibvorgang vom Benutzer abgebrochen.",
    "engine.iso_mount_error": "ISO-Einhängefehler: {error}",
    "engine.iso_mount_not_found": "ISO-Einhängepunkt nicht gefunden.",
    "engine.iso_unsupported": "ISO-Einhängen nicht unterstützt: {system}",
    "engine.iso_type_detected": "ISO-Typ: {iso_type}",
    "engine.dd_writing": "Raw-Image wird auf USB geschrieben...",
    "engine.dd_write_complete": "Raw-Image-Schreibvorgang abgeschlossen.",
    "engine.dd_cancelled": "Image-Schreibvorgang abgebrochen.",
    "engine.drive_too_small": "Laufwerk zu klein: ISO ist {iso_size}, aber Laufwerk hat nur {drive_size}.",
    "engine.dmg_not_supported": "DMG-Dateien werden nur auf macOS unterstützt.",
    "engine.unknown_iso_fallback": "Unbekannter ISO-Typ — verwende Raw-Schreibmodus (DD).",
    "engine.ejecting": "Wird ausgeworfen...",

    # -- wim_splitter.py --
    "wim.not_found": "wimlib-imagex nicht gefunden. Bitte wimlib installieren:\n  macOS:   brew install wimlib\n  Linux:   sudo apt install wimtools\n  Windows: https://wimlib.net/downloads/",
    "wim.split_error": "WIM-Aufteilungsfehler: {error}",
    "wim.no_swm_files": "Keine .swm-Dateien nach WIM-Aufteilung gefunden.",

    # -- iso_handler.py --
    "iso.not_found_error": "ISO nicht gefunden: {path}",
    "iso.invalid_error": "Ungültige ISO-Datei: {error}",

    # -- scan_worker.py --
    "scan.scanning": "USB-Laufwerke werden gescannt...",
    "scan.found": "{count} USB-Laufwerk(e) gefunden.",
    "scan.error": "USB-Scanfehler: {error}",

    # -- checksum_worker.py --
    "checksum.computing": "{algorithm} wird berechnet...",
    "checksum.cancelled": "Prüfsummenberechnung abgebrochen.",
    "checksum.result": "{algorithm}: {digest}",
    "checksum.error": "Prüfsummenfehler: {error}",

    # -- write_worker.py --
    "write.cancelled": "Schreibvorgang abgebrochen.",

    # -- platform --
    "platform.unmount_failed": "'{device}' konnte nicht ausgehängt werden: {error}",
    "platform.format_error": "Formatierungsfehler: {error}",
    "platform.dual_format_error": "Doppelformatierungsfehler: {error}",
    "platform.mount_error": "Einhängefehler: {error}",
    "platform.mount_not_found": "Einhängepunkt nicht gefunden: {device}",
    "platform.partition_not_found": "Partition mit Label '{label}' nicht gefunden: {device}",
    "platform.eject_error": "Auswurffehler: {error}",
    "platform.command_failed": "Befehl fehlgeschlagen: {command}\n{error}",
    "platform.powershell_error": "PowerShell-Fehler: {error}",
    "platform.diskpart_error": "Diskpart-Fehler: {error}",
    "platform.dual_no_letters": "Doppelte Partition erstellt, aber Laufwerksbuchstaben konnten nicht zugewiesen werden.",
    "platform.no_drive_letter": "Laufwerksbuchstabe konnte nicht zugewiesen werden.",
}
