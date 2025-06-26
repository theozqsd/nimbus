import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from pathlib import Path

home = Path.home()
nimbus_dir = home / "nimbus"
backup_dir = home / "Documents/nimbus"
nimbus_script = Path(__file__).parent / "main.py"
icon_path = Path(__file__).parent / "icon.png"

def log(message, symbol="ℹ️"):
    print(f"{symbol} {message}")

class TrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.sync_process = None
        self.watch_process = None

        self.tray = QSystemTrayIcon()
        self.tray.setIcon(QIcon.fromTheme("folder") if not icon_path.exists() else QIcon(str(icon_path)))
        self.tray.setToolTip("Nimbus")

        menu = QMenu()

        app_title = QAction("Nimbus")
        app_title.setEnabled(False)
        menu.addAction(app_title)
        menu.addSeparator()

        open_cloud_action = QAction("Open cloud drive", self.app)
        open_cloud_action.triggered.connect(self.open_folder)
        menu.addAction(open_cloud_action)

        open_backup_action = QAction("Open local backup", self.app)
        open_backup_action.triggered.connect(self.open_backup)
        menu.addAction(open_backup_action)

        sync_action = QAction("Force sync", self.app)
        sync_action.triggered.connect(self.force_sync)
        menu.addAction(sync_action)

        quit_action = QAction("Quit", self.app)
        quit_action.triggered.connect(self.quit_app)
        menu.addAction(quit_action)

        self.tray.setContextMenu(menu)
        self.tray.show()

        self.launch_nimbus()

        sys.exit(self.app.exec_())

    def launch_nimbus(self):
        self.sync_process = subprocess.Popen(["python3", str(nimbus_script)])
        log("Nimbus started.", "🚀")

    def open_folder(self):
        subprocess.Popen(["xdg-open", str(nimbus_dir)])

    def open_backup(self):
        subprocess.Popen(["xdg-open", str(backup_dir)])

    def force_sync(self):
        subprocess.Popen(["python3", str(nimbus_script)])
        log("Force sync.", "🔁")

    def quit_app(self):
        log("Closing...", "👋")

        for proc in [self.sync_process, self.watch_process]:
            if proc and proc.poll() is None:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()

        try:
            subprocess.run(["fusermount", "-u", str(nimbus_dir)], check=True)
            log("Successfully unmounted.", "✅")
        except subprocess.CalledProcessError as e:
            log(f"Unmounting error : {e}", "⚠️")

        self.tray.hide()
        QCoreApplication.quit()

if __name__ == "__main__":
    TrayApp()
