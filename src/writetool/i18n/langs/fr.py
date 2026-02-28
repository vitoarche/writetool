"""Traductions françaises."""

STRINGS: dict[str, str] = {
    # -- app.py --
    "app.privilege_title": "Privilèges requis",
    "app.privilege_message": "WriteTool nécessite les droits administrateur pour écrire sur les clés USB.",
    "app.privilege_error_title": "Erreur",
    "app.privilege_error_message": "Impossible d'obtenir les droits administrateur. L'application ne peut pas fonctionner sans droits administrateur.",
    "app.continue_button": "Continuer",

    # -- main_window.py --
    "main.start_button": "Lancer l'écriture",
    "main.cancel_button": "Annuler",
    "main.cancel_requested": "Annulation demandée...",
    "main.completed": "Terminé !",
    "main.cancelled": "Annulé.",
    "main.error_status": "Erreur : {message}",
    "main.write_error_title": "Erreur d'écriture",

    # -- dialogs.py --
    "dialog.confirm_title": "Confirmation d'écriture",
    "dialog.confirm_warning": "TOUTES LES DONNÉES sur <b>{drive_name}</b> seront SUPPRIMÉES !",
    "dialog.confirm_detail": "<b>{iso_name}</b> sera écrit sur <b>{name}</b> ({size}).\n\nCette opération est irréversible. Voulez-vous continuer ?",
    "dialog.confirm_yes": "Oui, écrire",
    "dialog.confirm_no": "Annuler",
    "dialog.success_title": "Terminé",
    "dialog.success_message": "Écriture USB terminée avec succès !",
    "dialog.success_detail": "Vous pouvez retirer la clé USB en toute sécurité.",

    # -- drive_selector.py --
    "drive.group_title": "USB cible",
    "drive.refresh": "Actualiser",
    "drive.scanning": "Analyse en cours...",
    "drive.not_found": "Aucune clé USB trouvée",
    "drive.not_found_hint": "Insérez une clé USB et cliquez sur Actualiser.",
    "drive.found_count": "{count} lecteur(s) trouvé(s).",
    "drive.scan_error": "Erreur d'analyse",

    # -- iso_selector.py --
    "iso.group_title": "Fichier ISO",
    "iso.placeholder": "Sélectionnez un fichier ISO Windows...",
    "iso.browse": "Parcourir...",
    "iso.checksum_none": "SHA256 : —",
    "iso.verify": "Vérifier",
    "iso.file_dialog_title": "Sélectionner un fichier ISO",
    "iso.file_filter": "Fichiers ISO (*.iso);;Tous les fichiers (*)",
    "iso.checksum_computing": "SHA256 : calcul en cours...",
    "iso.checksum_result": "SHA256 : {hash}",
    "iso.checksum_error": "SHA256 : erreur — {message}",
    "iso.checksum_progress": "SHA256 : calcul... {percent:.0f}%",

    # -- settings_panel.py --
    "settings.group_title": "Options",
    "settings.boot_label": "Démarrage :",
    "settings.boot_uefi": "UEFI",
    "settings.boot_legacy": "Legacy BIOS",
    "settings.partition_label": "Partition :",
    "settings.partition_auto": "Automatique",
    "settings.partition_wim_split": "Diviser WIM",
    "settings.partition_dual": "Double partition",
    "settings.wimlib_missing": "wimlib-imagex introuvable. Installation :\n  macOS : brew install wimlib\n  Linux : sudo apt install wimtools",
    "settings.language_label": "Langue :",

    # -- progress_panel.py --
    "progress.group_title": "Progression",

    # -- constants.py / stage labels --
    "stage.unmount": "Démontage...",
    "stage.format": "Formatage...",
    "stage.extract_boot": "Extraction des fichiers de démarrage...",
    "stage.copy_files": "Copie des fichiers...",
    "stage.process_wim": "Traitement de install.wim...",
    "stage.verify": "Vérification...",
    "stage.eject": "Éjection...",

    # -- writer_engine.py --
    "engine.mounting_iso": "Montage de l'ISO...",
    "engine.iso_mount": "ISO monté : {path}",
    "engine.strategy": "Stratégie : {strategy}",
    "engine.unmounting_drive": "Démontage du lecteur...",
    "engine.usb_mount": "USB monté : {path}",
    "engine.verifying": "Vérification...",
    "engine.eject_failed": "Éjection échouée, veuillez retirer manuellement.",
    "engine.write_complete": "Écriture terminée !",
    "engine.format_mbr_exfat": "Formatage : MBR + ExFAT...",
    "engine.format_gpt_dual": "Formatage : GPT + FAT32 (boot) + ExFAT (données)...",
    "engine.format_gpt_fat32": "Formatage : GPT + FAT32...",
    "engine.copying_files": "Copie des fichiers...",
    "engine.copy_cancelled": "Copie annulée.",
    "engine.copy_warning": "ATTENTION : Impossible de copier {fname} : {error}",
    "engine.copy_done": "Copie terminée ({count} fichiers).",
    "engine.wim_splitting": "Division de install.wim (wimlib-imagex)...",
    "engine.wim_split_done": "WIM divisé en {count} parties.",
    "engine.wim_copying_data": "Copie de install.wim sur la partition données...",
    "engine.wim_rsync": "Copie avec rsync : {name}...",
    "engine.wim_copy_error": "Erreur de copie WIM : {error}",
    "engine.wim_copied": "install.wim copié.",
    "engine.verify_warning": "ATTENTION : Fichier/dossier attendu introuvable : {path}",
    "engine.verify_done": "Vérification terminée.",
    "engine.cancel": "Écriture annulée par l'utilisateur.",
    "engine.iso_mount_error": "Erreur de montage ISO : {error}",
    "engine.iso_mount_not_found": "Point de montage ISO introuvable.",
    "engine.iso_unsupported": "Montage ISO non pris en charge : {system}",
    "engine.ejecting": "Éjection...",

    # -- wim_splitter.py --
    "wim.not_found": "wimlib-imagex introuvable. Veuillez installer wimlib :\n  macOS :   brew install wimlib\n  Linux :   sudo apt install wimtools\n  Windows : https://wimlib.net/downloads/",
    "wim.split_error": "Erreur de division WIM : {error}",
    "wim.no_swm_files": "Aucun fichier .swm trouvé après la division WIM.",

    # -- iso_handler.py --
    "iso.not_found_error": "ISO introuvable : {path}",
    "iso.invalid_error": "Fichier ISO invalide : {error}",

    # -- scan_worker.py --
    "scan.scanning": "Recherche de clés USB...",
    "scan.found": "{count} clé(s) USB trouvée(s).",
    "scan.error": "Erreur de recherche USB : {error}",

    # -- checksum_worker.py --
    "checksum.computing": "Calcul de {algorithm}...",
    "checksum.cancelled": "Calcul de la somme de contrôle annulé.",
    "checksum.result": "{algorithm} : {digest}",
    "checksum.error": "Erreur de somme de contrôle : {error}",

    # -- write_worker.py --
    "write.cancelled": "Écriture annulée.",

    # -- platform --
    "platform.unmount_failed": "Impossible de démonter '{device}' : {error}",
    "platform.format_error": "Erreur de formatage : {error}",
    "platform.dual_format_error": "Erreur de double formatage : {error}",
    "platform.mount_error": "Erreur de montage : {error}",
    "platform.mount_not_found": "Point de montage introuvable : {device}",
    "platform.partition_not_found": "Partition avec le label '{label}' introuvable : {device}",
    "platform.eject_error": "Erreur d'éjection : {error}",
    "platform.command_failed": "Commande échouée : {command}\n{error}",
    "platform.powershell_error": "Erreur PowerShell : {error}",
    "platform.diskpart_error": "Erreur Diskpart : {error}",
    "platform.dual_no_letters": "Double partition créée mais les lettres de lecteur n'ont pas pu être attribuées.",
    "platform.no_drive_letter": "Impossible d'attribuer une lettre de lecteur.",
}
