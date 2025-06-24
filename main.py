import os
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

server = os.getenv("SERVER_IP")
home = Path.home()
remote_path = home
mount_path = Path("/mnt/nimbus")
sync_path = Path(home, "nimbus")

def login():
    user = input("User: ")
    return user

user = login()

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
    unison = f"unison {sync_path} {mount_path} -auto -batch"

    try:
        subprocess.run(unison, shell=True, check=True)
        print("Synchronization completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during synchronization: {e}")

def watch():
    fswatch = f"fswatch -o {sync_path} {mount_path}"

    print("Watching for files to sync...")

    try:
        for line in iter(subprocess.Popen(fswatch, shell=True, stdout=subprocess.PIPE).stdout.readline, b''):
            print("Change detected, synchronizing...")
            sync()
    except KeyboardInterrupt:
        print("o7")

mount = f"sudo sshfs -o allow_other,default_permissions {user}@{server}:{remote_path} {mount_path}"

try:
    subprocess.run(mount, shell=True, check=True)
    print("Nimbus has been mounted.")
    sync()
except subprocess.CalledProcessError as e:
    print(f"Error while mounting Nimbus: {e}")
finally:
    watch()
