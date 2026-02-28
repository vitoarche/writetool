"""QSS stylesheet for the application."""

STYLESHEET = """
QMainWindow {
    background-color: #1e1e2e;
}

QWidget {
    color: #cdd6f4;
    font-family: ".AppleSystemUIFont", "SF Pro Display", "Helvetica Neue", "Segoe UI", sans-serif;
    font-size: 13px;
}

QGroupBox {
    border: 1px solid #45475a;
    border-radius: 8px;
    margin-top: 12px;
    padding: 16px 12px 12px 12px;
    background-color: #181825;
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: #89b4fa;
    font-weight: bold;
}

QPushButton {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 16px;
    color: #cdd6f4;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #45475a;
    border-color: #585b70;
}

QPushButton:pressed {
    background-color: #585b70;
}

QPushButton:disabled {
    background-color: #1e1e2e;
    color: #585b70;
    border-color: #313244;
}

QPushButton#startButton {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-size: 14px;
    font-weight: bold;
    padding: 12px 32px;
    border: none;
    border-radius: 8px;
}

QPushButton#startButton:hover {
    background-color: #b4d0fb;
}

QPushButton#startButton:disabled {
    background-color: #45475a;
    color: #585b70;
}

QPushButton#cancelButton {
    background-color: #f38ba8;
    color: #1e1e2e;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
}

QPushButton#cancelButton:hover {
    background-color: #f5a0b8;
}

QComboBox {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 12px;
    color: #cdd6f4;
}

QComboBox::drop-down {
    border: none;
    width: 24px;
}

QComboBox QAbstractItemView {
    background-color: #313244;
    border: 1px solid #45475a;
    color: #cdd6f4;
    selection-background-color: #45475a;
}

QLineEdit {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 8px 12px;
    color: #cdd6f4;
}

QLineEdit:focus {
    border-color: #89b4fa;
}

QLineEdit:read-only {
    background-color: #181825;
    color: #a6adc8;
}

QRadioButton {
    spacing: 8px;
    color: #cdd6f4;
}

QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #45475a;
    background-color: #313244;
}

QRadioButton::indicator:checked {
    border-color: #89b4fa;
    background-color: #89b4fa;
}

QProgressBar {
    border: none;
    border-radius: 6px;
    background-color: #313244;
    text-align: center;
    color: #cdd6f4;
    font-weight: bold;
    height: 24px;
}

QProgressBar::chunk {
    background-color: #89b4fa;
    border-radius: 6px;
}

QTextEdit#logPanel {
    background-color: #11111b;
    border: 1px solid #313244;
    border-radius: 6px;
    color: #a6adc8;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", monospace;
    font-size: 12px;
    padding: 8px;
}

QLabel#titleLabel {
    font-size: 18px;
    font-weight: bold;
    color: #89b4fa;
}

QLabel#statusLabel {
    color: #a6adc8;
    font-size: 12px;
}

QLabel#checksumLabel {
    color: #a6adc8;
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 11px;
}
"""
