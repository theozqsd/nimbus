from pathlib import Path
from dotenv import load_dotenv,find_dotenv, set_key
import os
import subprocess
import pwinput
import sys
import time

load_dotenv()

server = os.getenv("SERVER_IP")
home = Path.home()
remote_path = os.getenv("REMOTE")
mount_path = Path("/mnt/nimbus")
sync_path = Path(home, "nimbus")
local_user = home.parts[2]
ssh_key_path = Path(home, ".ssh", "id_ed25519")
remote_user = os.getenv("REMOTE_USER")

if not remote_user:
    remote_user = input("User: ")
    env_path = find_dotenv()
    set_key(env_path, "REMOTE_USER", remote_user)

if not ssh_key_path.is_file():
    mount = f"sshfs -o allow_other,default_permissions {remote_user}@{server}:{remote_path} {mount_path}"
else:
    mount = f"sshfs -o IdentityFile={ssh_key_path},allow_other,default_permissions {remote_user}@{server}:{remote_path} {mount_path}"


if not mount_path.is_dir():
    try:
        mount_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory {mount_path} created.")
    except OSError as e:
        print(f"An error occurred while creating the directory: {e}")

if not sync_path.is_dir():
    try:
        sync_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory {sync_path} created.")
    except OSError as e:
        print(f"An error occurred while creating the directory: {e}")

def sync():
    unison = f"unison {sync_path} {mount_path} -auto -batch -prefer newer"

    try:
        subprocess.run(unison, shell=True, check=True)
        print("Synchronization completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during synchronization: {e}")

def watch():
    fswatch = f"fswatch -o {sync_path} {mount_path}"

    print("Waiting for files to sync...")

    try:
        for line in iter(subprocess.Popen(fswatch, shell=True, stdout=subprocess.PIPE).stdout.readline, b''):
            print("Change detected, synchronizing...")
            sync()
    except KeyboardInterrupt:
        print("o7")

try:
    subprocess.run(mount, shell=True, check=True)
    print("Nimbus has been mounted.")
    sync()
except subprocess.CalledProcessError as e:
    print(f"Error while mounting Nimbus: {e}")
finally:
    watch()
