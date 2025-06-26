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

Copy the .env.example file into .env and configure it with your server details.

Launch the Nimbus GUI:

```bash
cd /path/to/nimbus
source venv/bin/activate
python3 gui.py
```

Use the system tray icon to open the cloud folder, local backup, force sync, or quit.

### Connect to your localhost

First start the ssh service

```bash
sudo systemctl start ssh.service
```

Then, use localhost as the server IP in the .env file, configure the other settings accordingly to your system.

## Contributing

Don't forget to lint your code with ruff :
```bash
python3 -m ruff check --fix
```

## Notes

The remote directory is mounted at `~/.local/share/nimbus/mount`

The local backup directory is `~/.local/share/nimbus/backup`

On quitting the app, the remote mount is cleanly unmounted using `fusermount -u`

Avoid killing the app abruptly to prevent Unison from detecting an empty root and potentially deleting files