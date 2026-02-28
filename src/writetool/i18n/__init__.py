"""Internationalization module for WriteTool."""

from writetool.i18n.manager import (
    LANGUAGE_NAMES,
    SUPPORTED_LANGUAGES,
    TranslationManager,
)

_mgr = TranslationManager()

tr = _mgr.tr
set_language = _mgr.set_language
get_language = _mgr.get_language
on_language_changed = _mgr.on_language_changed
remove_listener = _mgr.remove_listener

__all__ = [
    "tr",
    "set_language",
    "get_language",
    "on_language_changed",
    "remove_listener",
    "SUPPORTED_LANGUAGES",
    "LANGUAGE_NAMES",
]
