import sys
import os
import webbrowser
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QGroupBox, QGridLayout, QSizePolicy, QSpacerItem,
                             QMessageBox, QFrame)
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AimAssistApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COD AimAssist v1.5")
        self.setWindowIcon(QIcon(resource_path("assets/icon.ico")))
        self.setGeometry(100, 100, 900, 700)
        self.aim_assist_active = None
        self.setup_ui()

    def setup_ui(self):
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.North)
        self.tabs.setMovable(False)
        self.multiplayer_tab = self.create_multiplayer_tab()
        self.settings_tab = self.create_settings_tab()
        self.contact_tab = self.create_contact_tab()
        self.tabs.addTab(self.multiplayer_tab, "Multiplayer")
        self.tabs.addTab(self.settings_tab, "Settings")
        self.tabs.addTab(self.contact_tab, "Contact")
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color: #AAAAAA; padding: 5px;")
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.addWidget(self.status_label)
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.apply_styles()
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)

    def create_multiplayer_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Aim Assist Multiplayer")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #FFA500; margin-bottom: 20px;")
        layout.addWidget(title)
        aim_assist_group = self.create_aim_assist_group()
        layout.addWidget(aim_assist_group)
        additional_buttons = self.create_additional_buttons()
        layout.addWidget(additional_buttons)
        version = QLabel("Version 1.5 | Updated: 2023-11-15")
        version.setFont(QFont("Arial", 9))
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #666666; margin-top: 20px;")
        layout.addWidget(version)
        tab.setLayout(layout)
        return tab

    def create_settings_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        title = QLabel("Settings & Configuration")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1E90FF; margin-bottom: 20px;")
        layout.addWidget(title)
        mouse_group = QGroupBox("Mouse Settings")
        mouse_group.setStyleSheet("QGroupBox { font-weight: bold; color: #CCCCCC; }")
        mouse_layout = QGridLayout()
        mouse_layout.addWidget(QLabel("Sensitivity:"), 0, 0)
        mouse_layout.addWidget(QLabel("Aim Smoothing:"), 1, 0)
        mouse_layout.addWidget(QLabel("ADS Multiplier:"), 2, 0)
        mouse_layout.addWidget(QLabel("Scope Sensitivity:"), 3, 0)
        for i in range(4):
            value_label = QLabel("Default")
            value_label.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 4px;")
            mouse_layout.addWidget(value_label, i, 1)
        mouse_group.setLayout(mouse_layout)
        layout.addWidget(mouse_group)
        assist_group = QGroupBox("Aim Assist Settings")
        assist_group.setStyleSheet("QGroupBox { font-weight: bold; color: #CCCCCC; }")
        assist_layout = QGridLayout()
        assist_layout.addWidget(QLabel("Strength:"), 0, 0)
        assist_layout.addWidget(QLabel("FOV:"), 1, 0)
        assist_layout.addWidget(QLabel("Max Distance:"), 2, 0)
        assist_layout.addWidget(QLabel("Target Priority:"), 3, 0)
        for i in range(4):
            value_label = QLabel("Default")
            value_label.setStyleSheet("background-color: #333333; padding: 5px; border-radius: 4px;")
            assist_layout.addWidget(value_label, i, 1)
        assist_group.setLayout(assist_layout)
        layout.addWidget(assist_group)
        btn_save = self.create_button("Save Settings", "#4CAF50")
        btn_reset = self.create_button("Reset to Default", "#F44336")
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_reset)
        layout.addLayout(btn_layout)
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        tab.setLayout(layout)
        return tab

    def create_contact_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(30)
        layout.setContentsMargins(30, 30, 30, 30)
        title = QLabel("Contact & Support")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1E90FF; margin-bottom: 20px;")
        layout.addWidget(title)
        layout.addWidget(QLabel("support@codassist.com"))
        tab.setLayout(layout)
        return tab

    def create_button(self, text, color, tooltip=""):
        btn = QPushButton(text)
        btn.setFont(QFont("Arial", 12, QFont.Bold))
        btn.setCursor(Qt.PointingHandCursor)
        if tooltip:
            btn.setToolTip(tooltip)
        btn.setStyleSheet(
            f"QPushButton {{ background-color: {color}; color: white; border-radius: 8px; padding: 10px; }}"
            f"QPushButton:hover {{ background-color: {self.lighten_color(color)}; }}"
        )
        return btn

    def lighten_color(self, hex_color, factor=0.3):
        color = QColor(hex_color)
        return color.lighter(int(100 + factor * 100)).name()

    def update_status(self):
        if self.aim_assist_active:
            self.status_label.setText(f"Active: {self.aim_assist_active} | Press F8 to stop")
        else:
            self.status_label.setText("Ready | Select an aim assist mode")

    def activate_aim_assist(self, name):
        self.aim_assist_active = name
        self.status_label.setText(f"Active: {name} | Press F8 to stop")

    def deactivate_aim_assist(self, name):
        if self.aim_assist_active == name:
            self.aim_assist_active = None
            self.status_label.setText("Aim assist deactivated")

    def create_aim_assist_group(self):
        group = QGroupBox()
        layout = QGridLayout()
        assist_types = [("Lite AimAssist", "#4CAF50"), ("Normal AimAssist", "#2196F3")]
        for i, (name, color) in enumerate(assist_types):
            btn = self.create_button(name, color)
            stop_btn = self.create_button(f"Stop {name}", "#555555")
            layout.addWidget(btn, i, 0)
            layout.addWidget(stop_btn, i, 1)
            btn.clicked.connect(lambda _, n=name: self.activate_aim_assist(n))
            stop_btn.clicked.connect(lambda _, n=name: self.deactivate_aim_assist(n))
        group.setLayout(layout)
        return group

    def create_additional_buttons(self):
        widget = QWidget()
        layout = QHBoxLayout()
        buttons = [("Head", "#9C27B0"), ("Random", "#00BCD4"), ("Chests", "#795548")]
        for name, color in buttons:
            btn = self.create_button(name, color)
            layout.addWidget(btn)
        widget.setLayout(layout)
        return widget

    def apply_styles(self):
        self.setStyleSheet("QMainWindow { background-color: #121212; }")

if __name__ == "__main__":
    if sys.platform == "win32":
        import ctypes
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(220, 220, 220))
    app.setPalette(palette)
    window = AimAssistApp()
    window.show()
    sys.exit(app.exec_())
