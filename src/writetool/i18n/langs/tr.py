"""Türkçe çeviriler."""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "Yetki Gerekli",
    "app.privilege_message": "WriteTool, USB sürücülere yazabilmek için yönetici yetkisi gerektirir.",
    "app.privilege_error_title": "Hata",
    "app.privilege_error_message": "Yönetici yetkisi alınamadı. Uygulama yönetici yetkisi olmadan çalışamaz.",
    "app.continue_button": "Devam Et",

    # -- main_window.py --
    "main.start_button": "Yazdırmaya Başla",
    "main.cancel_button": "İptal",
    "main.cancel_requested": "İptal istendi...",
    "main.completed": "Tamamlandı!",
    "main.cancelled": "İptal edildi.",
    "main.error_status": "Hata: {message}",
    "main.write_error_title": "Yazma Hatası",

    # -- dialogs.py --
    "dialog.confirm_title": "Yazma Onayı",
    "dialog.confirm_warning": "<b>{drive_name}</b> üzerindeki TÜM VERİLER SİLİNECEK!",
    "dialog.confirm_detail": "<b>{iso_name}</b> dosyası <b>{name}</b> ({size}) sürücüsüne yazılacak.\n\nBu işlem geri alınamaz. Devam etmek istiyor musunuz?",
    "dialog.confirm_yes": "Evet, Yazdır",
    "dialog.confirm_no": "İptal",
    "dialog.dd_warning": "Bu imaj ham blok kopyalama (DD modu) ile yazılacak. Tüm sürücü imaj içeriğiyle üzerine yazılacaktır.",
    "dialog.success_title": "Tamamlandı",
    "dialog.success_message": "USB yazma işlemi başarıyla tamamlandı!",
    "dialog.success_detail": "USB sürücüyü güvenle çıkarabilirsiniz.",

    # -- drive_selector.py --
    "drive.group_title": "Hedef USB",
    "drive.refresh": "Yenile",
    "drive.scanning": "Taranıyor...",
    "drive.not_found": "USB sürücü bulunamadı",
    "drive.not_found_hint": "USB sürücü takın ve Yenile'ye basın.",
    "drive.found_count": "{count} sürücü bulundu.",
    "drive.scan_error": "Tarama hatası",

    # -- iso_selector.py --
    "iso.group_title": "ISO Dosyası",
    "iso.placeholder": "ISO dosyasını seçin...",
    "iso.browse": "Gözat...",
    "iso.checksum_none": "SHA256: —",
    "iso.verify": "Doğrula",
    "iso.file_dialog_title": "ISO Dosyası Seç",
    "iso.file_filter": "Disk İmajları (*.iso *.dmg *.img);;ISO Dosyaları (*.iso);;Tüm Dosyalar (*)",
    "iso.checksum_computing": "SHA256: hesaplanıyor...",
    "iso.checksum_result": "SHA256: {hash}",
    "iso.checksum_error": "SHA256: hata — {message}",
    "iso.checksum_progress": "SHA256: hesaplanıyor... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "Seçenekler",
    "settings.boot_label": "Boot:",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "Partition:",
    "settings.partition_auto": "Otomatik",
    "settings.partition_wim_split": "WIM Böl",
    "settings.partition_dual": "Çift Partition",
    "settings.wimlib_missing": "wimlib-imagex bulunamadı. Kurulum:\n  macOS: brew install wimlib\n  Linux: sudo apt install wimtools",
    "settings.language_label": "Dil:",
    "settings.iso_type_label": "ISO Türü:",
    "settings.iso_type_windows": "Windows",
    "settings.iso_type_linux": "Linux",
    "settings.iso_type_macos": "macOS",
    "settings.iso_type_unknown": "Bilinmiyor",
    "settings.iso_type_detecting": "Algılanıyor...",
    "settings.dd_note": "Bu imaj ham blok kopyalama (DD) ile yazılacak. Boot modu ve bölüm seçenekleri uygulanmaz.",

    # -- progress_panel.py --
    "progress.group_title": "İlerleme",

    # -- constants.py / stage labels --
    "stage.unmount": "Unmount ediliyor...",
    "stage.format": "Formatlanıyor...",
    "stage.extract_boot": "Boot dosyaları çıkarılıyor...",
    "stage.copy_files": "Dosyalar kopyalanıyor...",
    "stage.process_wim": "install.wim işleniyor...",
    "stage.dd_write": "İmaj yazılıyor...",
    "stage.verify": "Doğrulanıyor...",
    "stage.eject": "Eject ediliyor...",

    # -- writer_engine.py --
    "engine.mounting_iso": "ISO mount ediliyor...",
    "engine.iso_mount": "ISO mount: {path}",
    "engine.strategy": "Strateji: {strategy}",
    "engine.unmounting_drive": "Drive unmount ediliyor...",
    "engine.usb_mount": "USB mount: {path}",
    "engine.verifying": "Doğrulanıyor...",
    "engine.eject_failed": "Eject edilemedi, elle çıkarabilirsiniz.",
    "engine.write_complete": "Yazma işlemi tamamlandı!",
    "engine.format_mbr_exfat": "Formatlanıyor: MBR + ExFAT...",
    "engine.format_gpt_dual": "Formatlanıyor: GPT + FAT32 (boot) + ExFAT (data)...",
    "engine.format_gpt_fat32": "Formatlanıyor: GPT + FAT32...",
    "engine.copying_files": "Dosyalar kopyalanıyor...",
    "engine.copy_cancelled": "Kopyalama iptal edildi.",
    "engine.copy_warning": "UYARI: {fname} kopyalanamadı: {error}",
    "engine.copy_done": "Dosya kopyalama tamamlandı ({count} dosya).",
    "engine.wim_splitting": "install.wim bölünüyor (wimlib-imagex)...",
    "engine.wim_split_done": "WIM {count} parçaya bölündü.",
    "engine.wim_copying_data": "install.wim data partition'a kopyalanıyor...",
    "engine.wim_rsync": "rsync ile kopyalanıyor: {name}...",
    "engine.wim_copy_error": "WIM kopyalama hatası: {error}",
    "engine.wim_copied": "install.wim kopyalandı.",
    "engine.verify_warning": "UYARI: Beklenen dosya/klasör bulunamadı: {path}",
    "engine.verify_done": "Doğrulama tamamlandı.",
    "engine.cancel": "Yazma işlemi kullanıcı tarafından iptal edildi.",
    "engine.iso_mount_error": "ISO mount hatası: {error}",
    "engine.iso_mount_not_found": "ISO mount noktası bulunamadı.",
    "engine.iso_unsupported": "ISO mount desteklenmiyor: {system}",
    "engine.iso_type_detected": "ISO türü: {iso_type}",
    "engine.dd_writing": "Ham imaj USB'ye yazılıyor...",
    "engine.dd_write_complete": "Ham imaj yazma tamamlandı.",
    "engine.dd_cancelled": "İmaj yazma iptal edildi.",
    "engine.drive_too_small": "Sürücü çok küçük: ISO {iso_size} ama sürücü sadece {drive_size}.",
    "engine.dmg_not_supported": "DMG dosyaları yalnızca macOS'ta yazılabilir.",
    "engine.unknown_iso_fallback": "Bilinmeyen ISO türü — ham yazma (DD) kullanılıyor.",
    "engine.ejecting": "Eject ediliyor...",

    # -- wim_splitter.py --
    "wim.not_found": "wimlib-imagex bulunamadı. Lütfen wimlib paketini kurun:\n  macOS:   brew install wimlib\n  Linux:   sudo apt install wimtools\n  Windows: https://wimlib.net/downloads/",
    "wim.split_error": "WIM bölme hatası: {error}",
    "wim.no_swm_files": "WIM bölme sonrası .swm dosyaları bulunamadı.",

    # -- iso_handler.py --
    "iso.not_found_error": "ISO bulunamadı: {path}",
    "iso.invalid_error": "Geçersiz ISO dosyası: {error}",

    # -- scan_worker.py --
    "scan.scanning": "USB sürücüler taranıyor...",
    "scan.found": "{count} USB sürücü bulundu.",
    "scan.error": "USB tarama hatası: {error}",

    # -- checksum_worker.py --
    "checksum.computing": "{algorithm} hesaplanıyor...",
    "checksum.cancelled": "Checksum hesaplama iptal edildi.",
    "checksum.result": "{algorithm}: {digest}",
    "checksum.error": "Checksum hatası: {error}",

    # -- write_worker.py --
    "write.cancelled": "Yazma işlemi iptal edildi.",

    # -- platform/macos.py --
    "platform.unmount_failed": "'{device}' unmount edilemedi: {error}",
    "platform.format_error": "Format hatası: {error}",
    "platform.dual_format_error": "Dual format hatası: {error}",
    "platform.mount_error": "Mount hatası: {error}",
    "platform.mount_not_found": "Mount noktası bulunamadı: {device}",
    "platform.partition_not_found": "'{label}' etiketli partition bulunamadı: {device}",
    "platform.eject_error": "Eject hatası: {error}",

    # -- platform/linux.py --
    "platform.command_failed": "Komut başarısız: {command}\n{error}",

    # -- platform/windows.py --
    "platform.powershell_error": "PowerShell hatası: {error}",
    "platform.diskpart_error": "Diskpart hatası: {error}",
    "platform.dual_no_letters": "Dual partition oluşturuldu ama sürücü harfleri atanamadı.",
    "platform.no_drive_letter": "Sürücü harfi atanamadı.",
}
