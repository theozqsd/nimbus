import os
import subprocess

server = "100.96.46.91"
remote_path = "/home/theo"
mount_path = "/mnt/nimbus"
sync_path = "/home/theo/nimbus"

def login():
    user = input("User: ")
    return user

user = login()

# Vérifier et créer le répertoire de montage local s'il n'existe pas
if not os.path.isdir(mount_path):
    try:
        os.makedirs(mount_path)
        print(f"Directory {mount_path} created.")
    except OSError as e:
        print(f"An error occurred while creating the directory: {e}")

# Idem mais avec le répertoire de synchro local 
if not os.path.isdir(sync_path):
    try:
        os.makedirs(sync_path)
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

def watch():
    fswatch = ["fswatch", "-o", sync_path, mount_path]
    print("Watching for files to sync...")
    try:
        for line in iter(subprocess.Popen(fswatch, stdout=subprocess.PIPE).stdout.readline, b''):
            print("Change detected, synchronizing...")
            sync()
    except KeyboardInterrupt:
        print("Adios.")

watch()