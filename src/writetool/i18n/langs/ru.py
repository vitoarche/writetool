"""Русские переводы."""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "Требуются права",
    "app.privilege_message": "WriteTool требует права администратора для записи на USB-накопители.",
    "app.privilege_error_title": "Ошибка",
    "app.privilege_error_message": "Не удалось получить права администратора. Приложение не может работать без прав администратора.",
    "app.continue_button": "Продолжить",

    # -- main_window.py --
    "main.start_button": "Начать запись",
    "main.cancel_button": "Отмена",
    "main.cancel_requested": "Отмена запрошена...",
    "main.completed": "Завершено!",
    "main.cancelled": "Отменено.",
    "main.error_status": "Ошибка: {message}",
    "main.write_error_title": "Ошибка записи",

    # -- dialogs.py --
    "dialog.confirm_title": "Подтверждение записи",
    "dialog.confirm_warning": "ВСЕ ДАННЫЕ на <b>{drive_name}</b> будут УДАЛЕНЫ!",
    "dialog.confirm_detail": "<b>{iso_name}</b> будет записан на <b>{name}</b> ({size}).\n\nЭто действие необратимо. Продолжить?",
    "dialog.confirm_yes": "Да, записать",
    "dialog.confirm_no": "Отмена",
    "dialog.dd_warning": "Этот образ будет записан прямым блочным копированием (DD). Весь накопитель будет перезаписан содержимым образа.",
    "dialog.success_title": "Завершено",
    "dialog.success_message": "Запись на USB успешно завершена!",
    "dialog.success_detail": "Можно безопасно извлечь USB-накопитель.",

    # -- drive_selector.py --
    "drive.group_title": "Целевой USB",
    "drive.refresh": "Обновить",
    "drive.scanning": "Сканирование...",
    "drive.not_found": "USB-накопители не найдены",
    "drive.not_found_hint": "Подключите USB-накопитель и нажмите Обновить.",
    "drive.found_count": "Найдено накопителей: {count}.",
    "drive.scan_error": "Ошибка сканирования",

    # -- iso_selector.py --
    "iso.group_title": "ISO-файл",
    "iso.placeholder": "Выберите ISO-файл...",
    "iso.browse": "Обзор...",
    "iso.checksum_none": "SHA256: —",
    "iso.verify": "Проверить",
    "iso.file_dialog_title": "Выбор ISO-файла",
    "iso.file_filter": "Образы дисков (*.iso *.dmg *.img);;ISO-файлы (*.iso);;Все файлы (*)",
    "iso.checksum_computing": "SHA256: вычисляется...",
    "iso.checksum_result": "SHA256: {hash}",
    "iso.checksum_error": "SHA256: ошибка — {message}",
    "iso.checksum_progress": "SHA256: вычисляется... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "Параметры",
    "settings.boot_label": "Загрузка:",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "Разделы:",
    "settings.partition_auto": "Авто",
    "settings.partition_wim_split": "Разбить WIM",
    "settings.partition_dual": "Два раздела",
    "settings.wimlib_missing": "wimlib-imagex не найден. Установка:\n  macOS: brew install wimlib\n  Linux: sudo apt install wimtools",
    "settings.language_label": "Язык:",
    "settings.iso_type_label": "Тип ISO:",
    "settings.iso_type_windows": "Windows",
    "settings.iso_type_linux": "Linux",
    "settings.iso_type_macos": "macOS",
    "settings.iso_type_unknown": "Неизвестно",
    "settings.iso_type_detecting": "Определение...",
    "settings.dd_note": "Этот образ будет записан прямым блочным копированием (DD). Режим загрузки и параметры разделов не применяются.",

    # -- progress_panel.py --
    "progress.group_title": "Прогресс",

    # -- constants.py / stage labels --
    "stage.unmount": "Отключение...",
    "stage.format": "Форматирование...",
    "stage.extract_boot": "Извлечение загрузочных файлов...",
    "stage.copy_files": "Копирование файлов...",
    "stage.process_wim": "Обработка install.wim...",
    "stage.dd_write": "Запись образа...",
    "stage.verify": "Проверка...",
    "stage.eject": "Извлечение...",

    # -- writer_engine.py --
    "engine.mounting_iso": "Монтирование ISO...",
    "engine.iso_mount": "ISO смонтирован: {path}",
    "engine.strategy": "Стратегия: {strategy}",
    "engine.unmounting_drive": "Отключение накопителя...",
    "engine.usb_mount": "USB смонтирован: {path}",
    "engine.verifying": "Проверка...",
    "engine.eject_failed": "Не удалось извлечь, извлеките вручную.",
    "engine.write_complete": "Запись завершена!",
    "engine.format_mbr_exfat": "Форматирование: MBR + ExFAT...",
    "engine.format_gpt_dual": "Форматирование: GPT + FAT32 (boot) + ExFAT (data)...",
    "engine.format_gpt_fat32": "Форматирование: GPT + FAT32...",
    "engine.copying_files": "Копирование файлов...",
    "engine.copy_cancelled": "Копирование отменено.",
    "engine.copy_warning": "ВНИМАНИЕ: Не удалось скопировать {fname}: {error}",
    "engine.copy_done": "Копирование завершено ({count} файлов).",
    "engine.wim_splitting": "Разбиение install.wim (wimlib-imagex)...",
    "engine.wim_split_done": "WIM разбит на {count} частей.",
    "engine.wim_copying_data": "Копирование install.wim на раздел данных...",
    "engine.wim_rsync": "Копирование через rsync: {name}...",
    "engine.wim_copy_error": "Ошибка копирования WIM: {error}",
    "engine.wim_copied": "install.wim скопирован.",
    "engine.verify_warning": "ВНИМАНИЕ: Ожидаемый файл/папка не найден: {path}",
    "engine.verify_done": "Проверка завершена.",
    "engine.cancel": "Запись отменена пользователем.",
    "engine.iso_mount_error": "Ошибка монтирования ISO: {error}",
    "engine.iso_mount_not_found": "Точка монтирования ISO не найдена.",
    "engine.iso_unsupported": "Монтирование ISO не поддерживается: {system}",
    "engine.iso_type_detected": "Тип ISO: {iso_type}",
    "engine.dd_writing": "Запись образа на USB...",
    "engine.dd_write_complete": "Запись образа завершена.",
    "engine.dd_cancelled": "Запись образа отменена.",
    "engine.drive_too_small": "Накопитель слишком мал: ISO {iso_size}, а накопитель только {drive_size}.",
    "engine.dmg_not_supported": "DMG-файлы поддерживаются только на macOS.",
    "engine.unknown_iso_fallback": "Неизвестный тип ISO — используется прямая запись (DD).",
    "engine.ejecting": "Извлечение...",

    # -- wim_splitter.py --
    "wim.not_found": "wimlib-imagex не найден. Установите wimlib:\n  macOS:   brew install wimlib\n  Linux:   sudo apt install wimtools\n  Windows: https://wimlib.net/downloads/",
    "wim.split_error": "Ошибка разбиения WIM: {error}",
    "wim.no_swm_files": "Файлы .swm не найдены после разбиения WIM.",

    # -- iso_handler.py --
    "iso.not_found_error": "ISO не найден: {path}",
    "iso.invalid_error": "Недопустимый ISO-файл: {error}",

    # -- scan_worker.py --
    "scan.scanning": "Сканирование USB-накопителей...",
    "scan.found": "Найдено USB-накопителей: {count}.",
    "scan.error": "Ошибка сканирования USB: {error}",

    # -- checksum_worker.py --
    "checksum.computing": "Вычисление {algorithm}...",
    "checksum.cancelled": "Вычисление контрольной суммы отменено.",
    "checksum.result": "{algorithm}: {digest}",
    "checksum.error": "Ошибка контрольной суммы: {error}",

    # -- write_worker.py --
    "write.cancelled": "Запись отменена.",

    # -- platform --
    "platform.unmount_failed": "Не удалось отключить '{device}': {error}",
    "platform.format_error": "Ошибка форматирования: {error}",
    "platform.dual_format_error": "Ошибка двойного форматирования: {error}",
    "platform.mount_error": "Ошибка монтирования: {error}",
    "platform.mount_not_found": "Точка монтирования не найдена: {device}",
    "platform.partition_not_found": "Раздел с меткой '{label}' не найден: {device}",
    "platform.eject_error": "Ошибка извлечения: {error}",
    "platform.command_failed": "Команда не выполнена: {command}\n{error}",
    "platform.powershell_error": "Ошибка PowerShell: {error}",
    "platform.diskpart_error": "Ошибка Diskpart: {error}",
    "platform.dual_no_letters": "Двойной раздел создан, но буквы дисков не назначены.",
    "platform.no_drive_letter": "Не удалось назначить букву диска.",
}
