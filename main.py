import os
import subprocess
from pathlib import Path

server = "100.96.46.91"
home = Path.home()
remote_path = home
mount_path = "/mnt/nimbus"
sync_path = Path(home, "nimbus")

def login():
    user = input("User: ")
    return user

user = login()

# Vérifier et créer le répertoire de montage local s'il n'existe pas
if not Path(mount_path).is_dir():
    try:
        mount_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory {mount_path} created.")
    except OSError as e:
        print(f"An error occurred while creating the directory: {e}")

# Idem mais avec le répertoire de synchro local 
if not Path(sync_path).is_dir():
    try:
        sync_path.mkdir(parents=True, exist_ok=True)
        print(f"Directory {sync_path} created.")
    except OSError as e:
        print(f"An error occurred while creating the directory: {e}")


mount = [
    "sudo", "sshfs",
    "-o", "allow_other,default_permissions", 
    f"{user}@{server}:{remote_path}",
    mount_path
]

try:
    subprocess.run(mount, check=True)
    print("Nimbus has been mounted.")
except subprocess.CalledProcessError as e:
    print(f"Error while mounting Nimbus: {e}")

def watch():
    fswatch = ["fswatch", "-o", sync_path, mount_path]
    print("Watching for files to sync...")
    try:
        for line in iter(subprocess.Popen(fswatch, stdout=subprocess.PIPE).stdout.readline, b''):
            print("Change detected, synchronizing...")
            sync()
    except KeyboardInterrupt:
        print("Adios.")

def sync():
    unison = [
        "unison",
        sync_path,
        mount_path,
        "-auto",  
        "-batch" 
    ] 

    try:
        subprocess.run(unison, check=True)
        print("Synchronization completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during synchronization: {e}")

    watch()

sync()