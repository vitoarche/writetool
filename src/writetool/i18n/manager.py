"""Translation manager singleton with config persistence."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

_CONFIG_DIR = Path.home() / ".config" / "writetool"
_CONFIG_FILE = _CONFIG_DIR / "config.json"

DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("tr", "en", "ru", "zh", "de", "fr")

LANGUAGE_NAMES = {
    "tr": "Türkçe",
    "en": "English",
    "ru": "Русский",
    "zh": "中文",
    "de": "Deutsch",
    "fr": "Français",
}


class TranslationManager:
    """Singleton that holds translation strings and notifies on language change."""

    _instance: TranslationManager | None = None
    _initialized: bool

    def __new__(cls) -> TranslationManager:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return
        self._initialized = True
        self._lang = DEFAULT_LANGUAGE
        self._strings: dict[str, str] = {}
        self._listeners: list[Callable[[], None]] = []
        self._load_config()
        self._load_strings()

    # -- public API --

    def get_language(self) -> str:
        return self._lang

    def set_language(self, lang: str) -> None:
        if lang not in SUPPORTED_LANGUAGES:
            return
        if lang == self._lang:
            return
        self._lang = lang
        self._load_strings()
        self._save_config()
        self._notify()

    def tr(self, key: str, **kwargs: object) -> str:
        text = self._strings.get(key, key)
        if kwargs:
            try:
                text = text.format(**kwargs)
            except (KeyError, IndexError):
                pass
        return text

    def on_language_changed(self, callback: Callable[[], None]) -> None:
        self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[], None]) -> None:
        try:
            self._listeners.remove(callback)
        except ValueError:
            pass

    def has_saved_language(self) -> bool:
        """Return True if a language was explicitly saved to config."""
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            return "language" in data
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            return False

    # -- internal --

    def _load_strings(self) -> None:
        from writetool.i18n.langs import get_strings
        self._strings = get_strings(self._lang)

    def _notify(self) -> None:
        for cb in self._listeners:
            try:
                cb()
            except Exception:
                pass

    def _load_config(self) -> None:
        try:
            data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
            lang = data.get("language", DEFAULT_LANGUAGE)
            if lang in SUPPORTED_LANGUAGES:
                self._lang = lang
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            pass

    def _save_config(self) -> None:
        try:
            _CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            data: dict = {}
            if _CONFIG_FILE.exists():
                try:
                    data = json.loads(_CONFIG_FILE.read_text(encoding="utf-8"))
                except (json.JSONDecodeError, OSError):
                    pass
            data["language"] = self._lang
            _CONFIG_FILE.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except OSError:
            pass
