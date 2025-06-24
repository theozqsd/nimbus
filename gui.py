import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from pathlib import Path

home = Path.home()
nimbus_dir = home / "nimbus"
nimbus_script = Path(__file__).parent / "main.py"
icon_path = Path(__file__).parent / "icon.png"

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon.fromTheme("folder") if not icon_path.exists() else QIcon(str(icon_path)))
        self.tray.setToolTip("Nimbus")
        
        menu = QMenu()
        app_title = QAction("Nimbus")
        app_title.setEnabled(False)
        menu.addAction(app_title)

        menu.addSeparator()
        
        open_action = QAction("Ouvrir dossier", self.app)
        open_action.triggered.connect(self.open_folder)
        menu.addAction(open_action)

        sync_action = QAction("Forcer synchronisation", self.app)
        sync_action.triggered.connect(self.force_sync)
        menu.addAction(sync_action)

        quit_action = QAction("Quitter", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()
        self.launch_nimbus()

        sys.exit(self.app.exec_())

    def launch_nimbus(self):
        subprocess.Popen(["python3", str(nimbus_script)])

    def open_folder(self):
        subprocess.Popen(["xdg-open", str(nimbus_dir)])

    def force_sync(self):
        subprocess.Popen(["python3", str(nimbus_script)])

    def quit_app(self):
        self.tray.hide()
        QCoreApplication.quit()

if __name__ == "__main__":
    TrayApp()
