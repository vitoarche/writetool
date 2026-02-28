"""Language string loaders."""

from __future__ import annotations


def get_strings(lang: str) -> dict[str, str]:
    """Return translation dict for the given language code."""
    if lang == "tr":
        from writetool.i18n.langs.tr import STRINGS
    elif lang == "en":
        from writetool.i18n.langs.en import STRINGS
    elif lang == "ru":
        from writetool.i18n.langs.ru import STRINGS
    elif lang == "zh":
        from writetool.i18n.langs.zh import STRINGS
    elif lang == "de":
        from writetool.i18n.langs.de import STRINGS
    elif lang == "fr":
        from writetool.i18n.langs.fr import STRINGS
    else:
        from writetool.i18n.langs.tr import STRINGS
    return STRINGS
