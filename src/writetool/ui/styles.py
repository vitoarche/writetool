"""QSS stylesheet for the application — Catppuccin Mocha dark theme."""

import sys

_ROW_H = 34

if sys.platform == "darwin":
    _FONT = '"Helvetica Neue"'
elif sys.platform == "win32":
    _FONT = '"Segoe UI"'
else:
    _FONT = '"Noto Sans"'

STYLESHEET = f"""
/* ── Base ── */
QMainWindow {{
    background-color: #1e1e2e;
}}

QWidget {{
    color: #cdd6f4;
    font-family: {_FONT};
    font-size: 13px;
}}

/* ── Group boxes ── */
QGroupBox {{
    border: 1px solid #45475a;
    border-radius: 8px;
    margin-top: 14px;
    padding: 10px 12px 12px 12px;
    background-color: #181825;
}}

QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #89b4fa;
    font-weight: bold;
    font-size: 13px;
}}

/* ── Buttons (general) — border:0 removes Fusion's internal frame ── */
QPushButton {{
    background-color: #45475a;
    border: 0px;
    border-radius: 6px;
    padding: 0px 16px;
    min-height: {_ROW_H}px;
    max-height: {_ROW_H}px;
    color: #ffffff;
    font-size: 13px;
    font-weight: bold;
}}

QPushButton:hover {{
    background-color: #585b70;
}}

QPushButton:pressed {{
    background-color: #6c7086;
}}

QPushButton:disabled {{
    background-color: #1e1e2e;
    color: #585b70;
}}

/* ── Start button (accent blue) ── */
QPushButton#startButton {{
    background-color: #89b4fa;
    color: #11111b;
    font-size: 14px;
    font-weight: bold;
    padding: 10px 32px;
    border: 0px;
    border-radius: 8px;
    min-height: 22px;
    max-height: 44px;
}}

QPushButton#startButton:hover {{
    background-color: #b4d0fb;
}}

QPushButton#startButton:pressed {{
    background-color: #74a8f7;
}}

QPushButton#startButton:disabled {{
    background-color: #45475a;
    color: #585b70;
}}

/* ── Cancel button (accent red) ── */
QPushButton#cancelButton {{
    background-color: #f38ba8;
    color: #11111b;
    font-size: 14px;
    font-weight: bold;
    border: 0px;
    border-radius: 8px;
    padding: 10px 28px;
    min-height: 22px;
    max-height: 44px;
}}

QPushButton#cancelButton:hover {{
    background-color: #f5a0b8;
}}

QPushButton#cancelButton:pressed {{
    background-color: #e87a99;
}}

/* ── Combo box ── */
QComboBox {{
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 0px 12px;
    min-height: {_ROW_H}px;
    max-height: {_ROW_H}px;
    color: #cdd6f4;
}}

QComboBox:hover {{
    border-color: #585b70;
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox::down-arrow {{
    image: none;
    border-left: 4px solid transparent;
    border-right: 4px solid transparent;
    border-top: 6px solid #cdd6f4;
    margin-right: 8px;
}}

QComboBox QAbstractItemView {{
    background-color: #313244;
    border: 1px solid #45475a;
    color: #cdd6f4;
    selection-background-color: #45475a;
    selection-color: #ffffff;
    outline: none;
}}

/* ── Line edit ── */
QLineEdit {{
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 0px 12px;
    min-height: {_ROW_H}px;
    max-height: {_ROW_H}px;
    color: #cdd6f4;
}}

QLineEdit:focus {{
    border-color: #89b4fa;
}}

QLineEdit:read-only {{
    background-color: #181825;
    color: #a6adc8;
}}

/* ── Radio buttons ── */
QRadioButton {{
    spacing: 8px;
    color: #cdd6f4;
}}

QRadioButton::indicator {{
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #585b70;
    background-color: #313244;
}}

QRadioButton::indicator:hover {{
    border-color: #89b4fa;
}}

QRadioButton::indicator:checked {{
    border-color: #89b4fa;
    background-color: #89b4fa;
}}

/* ── Progress bar ── */
QProgressBar {{
    border: none;
    border-radius: 8px;
    background-color: #313244;
    text-align: center;
    color: #cdd6f4;
    font-weight: bold;
    min-height: 32px;
}}

QProgressBar::chunk {{
    background-color: #89b4fa;
    border-radius: 8px;
}}

/* ── Log panel ── */
QTextEdit#logPanel {{
    background-color: #11111b;
    border: 1px solid #313244;
    border-radius: 6px;
    color: #a6adc8;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", monospace;
    font-size: 12px;
    padding: 8px;
}}

/* ── Labels ── */
QLabel#titleLabel {{
    font-size: 18px;
    font-weight: bold;
    color: #89b4fa;
}}

QLabel#statusLabel {{
    color: #a6adc8;
    font-size: 12px;
}}

QLabel#checksumLabel {{
    color: #a6adc8;
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 11px;
}}

QLabel#authorLabel {{
    color: #585b70;
    font-size: 11px;
    padding-top: 4px;
}}

/* ── Scrollbar ── */
QScrollBar:vertical {{
    background-color: #181825;
    width: 10px;
    border-radius: 5px;
}}

QScrollBar::handle:vertical {{
    background-color: #45475a;
    border-radius: 5px;
    min-height: 20px;
}}

QScrollBar::handle:vertical:hover {{
    background-color: #585b70;
}}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

/* ── Message boxes ── */
QMessageBox {{
    background-color: #1e1e2e;
}}

QMessageBox QLabel {{
    color: #cdd6f4;
    font-size: 13px;
}}

QMessageBox QPushButton {{
    min-width: 80px;
}}

/* ── Dialog ── */
QDialog {{
    background-color: #1e1e2e;
}}
"""
