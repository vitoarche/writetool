"""中文翻译。"""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "需要权限",
    "app.privilege_message": "WriteTool 需要管理员权限才能写入 USB 驱动器。",
    "app.privilege_error_title": "错误",
    "app.privilege_error_message": "无法获取管理员权限。应用无法在没有管理员权限的情况下运行。",
    "app.continue_button": "继续",

    # -- main_window.py --
    "main.start_button": "开始写入",
    "main.cancel_button": "取消",
    "main.cancel_requested": "正在取消...",
    "main.completed": "已完成！",
    "main.cancelled": "已取消。",
    "main.error_status": "错误：{message}",
    "main.write_error_title": "写入错误",

    # -- dialogs.py --
    "dialog.confirm_title": "写入确认",
    "dialog.confirm_warning": "<b>{drive_name}</b> 上的所有数据将被删除！",
    "dialog.confirm_detail": "<b>{iso_name}</b> 将写入 <b>{name}</b>（{size}）。\n\n此操作不可撤销。是否继续？",
    "dialog.confirm_yes": "确认写入",
    "dialog.confirm_no": "取消",
    "dialog.dd_warning": "此映像将使用原始块复制（DD 模式）写入。整个驱动器将被映像内容覆盖。",
    "dialog.success_title": "完成",
    "dialog.success_message": "USB 写入成功完成！",
    "dialog.success_detail": "您可以安全地弹出 USB 驱动器。",

    # -- drive_selector.py --
    "drive.group_title": "目标 USB",
    "drive.refresh": "刷新",
    "drive.scanning": "扫描中...",
    "drive.not_found": "未找到 USB 驱动器",
    "drive.not_found_hint": "请插入 USB 驱动器并点击刷新。",
    "drive.found_count": "找到 {count} 个驱动器。",
    "drive.scan_error": "扫描错误",

    # -- iso_selector.py --
    "iso.group_title": "ISO 文件",
    "iso.placeholder": "选择 ISO 文件...",
    "iso.browse": "浏览...",
    "iso.checksum_none": "SHA256：—",
    "iso.verify": "验证",
    "iso.file_dialog_title": "选择 ISO 文件",
    "iso.file_filter": "磁盘映像 (*.iso *.dmg *.img);;ISO 文件 (*.iso);;所有文件 (*)",
    "iso.checksum_computing": "SHA256：计算中...",
    "iso.checksum_result": "SHA256：{hash}",
    "iso.checksum_error": "SHA256：错误 — {message}",
    "iso.checksum_progress": "SHA256：计算中... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "选项",
    "settings.boot_label": "启动：",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "分区：",
    "settings.partition_auto": "自动",
    "settings.partition_wim_split": "拆分 WIM",
    "settings.partition_dual": "双分区",
    "settings.wimlib_missing": "未找到 wimlib-imagex。安装方法：\n  macOS：brew install wimlib\n  Linux：sudo apt install wimtools",
    "settings.language_label": "语言：",
    "settings.iso_type_label": "ISO 类型：",
    "settings.iso_type_windows": "Windows",
    "settings.iso_type_linux": "Linux",
    "settings.iso_type_macos": "macOS",
    "settings.iso_type_unknown": "未知",
    "settings.iso_type_detecting": "检测中...",
    "settings.dd_note": "此映像将使用原始块复制（DD）写入。启动模式和分区选项不适用。",

    # -- progress_panel.py --
    "progress.group_title": "进度",

    # -- constants.py / stage labels --
    "stage.unmount": "正在卸载...",
    "stage.format": "正在格式化...",
    "stage.extract_boot": "正在提取启动文件...",
    "stage.copy_files": "正在复制文件...",
    "stage.process_wim": "正在处理 install.wim...",
    "stage.dd_write": "正在写入映像...",
    "stage.verify": "正在验证...",
    "stage.eject": "正在弹出...",

    # -- writer_engine.py --
    "engine.mounting_iso": "正在挂载 ISO...",
    "engine.iso_mount": "ISO 挂载：{path}",
    "engine.strategy": "策略：{strategy}",
    "engine.unmounting_drive": "正在卸载驱动器...",
    "engine.usb_mount": "USB 挂载：{path}",
    "engine.verifying": "正在验证...",
    "engine.eject_failed": "弹出失败，请手动移除。",
    "engine.write_complete": "写入操作完成！",
    "engine.format_mbr_exfat": "格式化：MBR + ExFAT...",
    "engine.format_gpt_dual": "格式化：GPT + FAT32（启动）+ ExFAT（数据）...",
    "engine.format_gpt_fat32": "格式化：GPT + FAT32...",
    "engine.copying_files": "正在复制文件...",
    "engine.copy_cancelled": "复制已取消。",
    "engine.copy_warning": "警告：无法复制 {fname}：{error}",
    "engine.copy_done": "文件复制完成（{count} 个文件）。",
    "engine.wim_splitting": "正在拆分 install.wim（wimlib-imagex）...",
    "engine.wim_split_done": "WIM 已拆分为 {count} 个部分。",
    "engine.wim_copying_data": "正在将 install.wim 复制到数据分区...",
    "engine.wim_rsync": "正在使用 rsync 复制：{name}...",
    "engine.wim_copy_error": "WIM 复制错误：{error}",
    "engine.wim_copied": "install.wim 已复制。",
    "engine.verify_warning": "警告：未找到预期的文件/文件夹：{path}",
    "engine.verify_done": "验证完成。",
    "engine.cancel": "写入操作已被用户取消。",
    "engine.iso_mount_error": "ISO 挂载错误：{error}",
    "engine.iso_mount_not_found": "未找到 ISO 挂载点。",
    "engine.iso_unsupported": "不支持 ISO 挂载：{system}",
    "engine.iso_type_detected": "ISO 类型：{iso_type}",
    "engine.dd_writing": "正在将原始映像写入 USB...",
    "engine.dd_write_complete": "原始映像写入完成。",
    "engine.dd_cancelled": "映像写入已取消。",
    "engine.drive_too_small": "驱动器太小：ISO 为 {iso_size}，但驱动器仅有 {drive_size}。",
    "engine.dmg_not_supported": "DMG 文件仅在 macOS 上支持。",
    "engine.unknown_iso_fallback": "未知 ISO 类型 — 使用原始写入（DD）。",
    "engine.ejecting": "正在弹出...",

    # -- wim_splitter.py --
    "wim.not_found": "未找到 wimlib-imagex。请安装 wimlib：\n  macOS：  brew install wimlib\n  Linux：  sudo apt install wimtools\n  Windows：https://wimlib.net/downloads/",
    "wim.split_error": "WIM 拆分错误：{error}",
    "wim.no_swm_files": "WIM 拆分后未找到 .swm 文件。",

    # -- iso_handler.py --
    "iso.not_found_error": "未找到 ISO：{path}",
    "iso.invalid_error": "无效的 ISO 文件：{error}",

    # -- scan_worker.py --
    "scan.scanning": "正在扫描 USB 驱动器...",
    "scan.found": "找到 {count} 个 USB 驱动器。",
    "scan.error": "USB 扫描错误：{error}",

    # -- checksum_worker.py --
    "checksum.computing": "正在计算 {algorithm}...",
    "checksum.cancelled": "校验和计算已取消。",
    "checksum.result": "{algorithm}：{digest}",
    "checksum.error": "校验和错误：{error}",

    # -- write_worker.py --
    "write.cancelled": "写入操作已取消。",

    # -- platform --
    "platform.unmount_failed": "无法卸载 '{device}'：{error}",
    "platform.format_error": "格式化错误：{error}",
    "platform.dual_format_error": "双分区格式化错误：{error}",
    "platform.mount_error": "挂载错误：{error}",
    "platform.mount_not_found": "未找到挂载点：{device}",
    "platform.partition_not_found": "未找到标签为 '{label}' 的分区：{device}",
    "platform.eject_error": "弹出错误：{error}",
    "platform.command_failed": "命令失败：{command}\n{error}",
    "platform.powershell_error": "PowerShell 错误：{error}",
    "platform.diskpart_error": "Diskpart 错误：{error}",
    "platform.dual_no_letters": "双分区已创建，但无法分配驱动器号。",
    "platform.no_drive_letter": "无法分配驱动器号。",
}
