import sys
import os
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu
from PySide6.QtGui import QPixmap, QAction, QIcon
import ytlistener
import threading

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint)  
        self.setAttribute(Qt.WA_TranslucentBackground)  
        self.setStyleSheet(""" 
            background-color: rgba(0, 0, 0, 180);
            color: white;
        """)

        layout = QVBoxLayout()

        # Szare przyciski
        self.minimize_button = QPushButton("Minimize to Tray")
        self.minimize_button.setStyleSheet("""
            background-color: rgba(169, 169, 169, 150);
            border: none;
            color: white;
            padding: 10px;
        """)
        self.minimize_button.clicked.connect(self.minimize_to_tray)
        layout.addWidget(self.minimize_button)

        self.close_button = QPushButton("Close")
        self.close_button.setStyleSheet("""
            background-color: rgba(169, 169, 169, 150); 
            border: none;
            color: white;
            padding: 10px;
        """)
        self.close_button.clicked.connect(self.close_app)
        layout.addWidget(self.close_button)

        self.setLayout(layout)

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("icon.png"))
        self.tray_icon.setVisible(True)

        tray_menu = QMenu(self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close_app)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)

        self.listener_thread = threading.Thread(target=ytlistener.refresh_window_title)
        self.listener_thread.daemon = True
        self.listener_thread.start()

    def minimize_to_tray(self):
        self.hide()

    def close_app(self):
        self.tray_icon.setVisible(False)
        QApplication.quit() 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MyApp()
    window.show()

    sys.exit(app.exec())
