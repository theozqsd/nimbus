from pathlib import Path
from dotenv import load_dotenv,find_dotenv, set_key
import os
import subprocess

load_dotenv()

server = os.getenv("SERVER_IP")
remote_user = os.getenv("REMOTE_USER")

home = Path.home()
local_user = home.parts[2]
remote_dir = os.getenv("REMOTE")
ssh_key_path = home / ".ssh" / "id_ed25519"
nimbus_dir = home / "nimbus"
backup_dir = home / "Documents/nimbus"

def log(message, symbol="ℹ️"):
    print(f"{symbol} {message}")
    try:
        subprocess.run(["notify-send", "Nimbus", f"{symbol} {message}"], check=True)
    except Exception:  
        pass

if not remote_user:
    remote_user = input("User: ")
    env_path = find_dotenv()
    set_key(env_path, "REMOTE_USER", remote_user)

if not ssh_key_path.is_file():
    mount = f"sshfs -o allow_other,default_permissions {remote_user}@{server}:{remote_dir} {nimbus_dir}"
else:
    mount = f"sshfs -o IdentityFile={ssh_key_path},allow_other,default_permissions,uid=1000,gid=1000 {remote_user}@{server}:{remote_dir} {nimbus_dir}"

if not nimbus_dir.is_dir():
    try:
        nimbus_dir.mkdir(parents=True, exist_ok=True)
        log(f"Directory {nimbus_dir} created.","✅")
    except OSError as e:
        log(f"An error occurred while creating the directory: {e}","❌")

if not backup_dir.is_dir():
    try:
        backup_dir.mkdir(parents=True, exist_ok=True)
        print(f"Directory {backup_dir} created.")
    except OSError as e:
        log(f"An error occurred while creating the directory: {e}","❌")

def sync():
    unison = f"unison {backup_dir} {nimbus_dir} -auto -batch -prefer newer"

    try:
        subprocess.run(unison, shell=True, check=True)
        log("Synchronization completed successfully.","✅")
    except subprocess.CalledProcessError as e:
        log(f"An error occurred during synchronization: {e}","❌")

def watch():
    fswatch = f"fswatch -o {backup_dir} {nimbus_dir}"

    log("Waiting for files to sync...","🔄")

    try:
        for line in iter(subprocess.Popen(fswatch, shell=True, stdout=subprocess.PIPE).stdout.readline, b''):
            log("Change detected, synchronizing...","🔄")
            sync()
    except KeyboardInterrupt:
        print("o7")

try:
    subprocess.run(mount, shell=True, check=True)
    log("Nimbus has been mounted.","✅")
    sync()
except subprocess.CalledProcessError as e:
    log(f"Error while mounting Nimbus: {e}","❌")
finally:
    watch()
