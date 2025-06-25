# Nimbus, still in WIP

Nimbus is a lightweight graphical application that mounts a remote directory via SSHFS, synchronizes files using Unison, and provides a simple system tray interface.

It's still in work in progress.

---

## Requirements

Install the following system dependencies:

```bash
sudo apt install sshfs unison fswatch python3-venv python3-pip libxcb-xinerama0
```

Create and activate the Python virtual environment, then install Python dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Configure your .env file at the project root with your server details:

```ini
SERVER_IP=192.168.1.42
REMOTE_USER=username
REMOTE=/path/to/remote/directory
```

Launch the Nimbus GUI:

```bash
cd /path/to/nimbus
source venv/bin/activate
python3 gui.py
```

Use the system tray icon to open the cloud folder, local backup, force sync, or quit.

## Notes

The remote directory is mounted at `~/nimbus`

The local backup directory is `~/nimbus_backup`

On quitting the app, the remote mount is cleanly unmounted using `fusermount -u`

Avoid killing the app abruptly to prevent Unison from detecting an empty root and potentially deleting files