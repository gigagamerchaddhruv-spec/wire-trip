import os
import time
import hashlib
import json
import psutil
from datetime import datetime

# ==========================
# CONFIG
# ==========================

CONFIG = {
    "watch_dir": "wiretrip/decoys",
    "log_dir": "wiretrip/logs",
    "log_file": "wiretrip/logs/access.log",
    "scan_interval": 2,
    "decoy_files": [
        "passwords.txt",
        "aws_keys.txt",
        "server_backup.sql",
        "admin_notes.txt",
        "router_config_backup.cfg"
    ]
}

file_hashes = {}

# ==========================
# SETUP
# ==========================

def setup_environment():
    os.makedirs(CONFIG["watch_dir"], exist_ok=True)
    os.makedirs(CONFIG["log_dir"], exist_ok=True)

    for name in CONFIG["decoy_files"]:
        path = os.path.join(CONFIG["watch_dir"], name)

        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(generate_fake_content(name))


# ==========================
# FAKE DATA GENERATOR
# ==========================

def generate_fake_content(filename):

    fake_data = {
        "passwords.txt":
        """
root:Sup3rSecret!
admin:LetMeIn123
backup:Password123
db_admin:qwertyuiop
""",

        "aws_keys.txt":
        """
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
""",

        "server_backup.sql":
        """
DATABASE: production

users:
admin
backup
service_account
""",

        "admin_notes.txt":
        """
TODO:
- rotate server credentials
- update firewall rules
- remove old admin accounts
""",

        "router_config_backup.cfg":
        """
router admin password: admin123
ssh enabled
vpn key: 89dhs92jds92jd
"""
    }

    return fake_data.get(filename, "Confidential data\n")


# ==========================
# HASHING
# ==========================

def hash_file(path):

    h = hashlib.sha256()

    try:
        with open(path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()
    except:
        return None


# ==========================
# PROCESS DETECTION
# ==========================

def find_process_using_file(filepath):

    users = []

    for proc in psutil.process_iter(['pid','name','open_files']):

        try:
            files = proc.info['open_files']
            if files:
                for f in files:
                    if filepath in f.path:
                        users.append(f"{proc.info['name']} (PID {proc.info['pid']})")
        except:
            pass

    return users


# ==========================
# LOGGING
# ==========================

def log_event(file):

    processes = find_process_using_file(file)

    with open(CONFIG["log_file"], "a") as log:

        log.write("\n=========================\n")
        log.write(f"TIME: {datetime.now()}\n")
        log.write(f"FILE TRIGGERED: {file}\n")

        if processes:
            log.write("PROCESS USING FILE:\n")
            for p in processes:
                log.write(f"  {p}\n")

        else:
            log.write("PROCESS: Unknown\n")


# ==========================
# INITIAL HASH BASELINE
# ==========================

def initialize_hashes():

    for root, dirs, files in os.walk(CONFIG["watch_dir"]):

        for name in files:

            path = os.path.join(root, name)
            file_hashes[path] = hash_file(path)


# ==========================
# SCANNER
# ==========================

def scan_files():

    for root, dirs, files in os.walk(CONFIG["watch_dir"]):

        for name in files:

            path = os.path.join(root, name)

            current_hash = hash_file(path)

            if path not in file_hashes:
                file_hashes[path] = current_hash
                continue

            if file_hashes[path] != current_hash:

                log_event(path)

                file_hashes[path] = current_hash


# ==========================
# BANNER
# ==========================

def banner():

    print("""
██╗    ██╗██╗██████╗ ███████╗████████╗██████╗ ██╗██████╗ 
██║    ██║██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██╔══██╗
██║ █╗ ██║██║██████╔╝█████╗     ██║   ██████╔╝██║██████╔╝
██║███╗██║██║██╔══██╗██╔══╝     ██║   ██╔══██╗██║██╔═══╝ 
╚███╔███╔╝██║██║  ██║███████╗   ██║   ██║  ██║██║██║     
 ╚══╝╚══╝ ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝     

WireTrip Defensive Honeypot
""")


# ==========================
# MAIN LOOP
# ==========================

def main():

    banner()

    print("[*] Setting up environment")
    setup_environment()

    print("[*] Initializing baseline hashes")
    initialize_hashes()

    print("[*] Monitoring decoy files...\n")

    while True:

        scan_files()
        time.sleep(CONFIG["scan_interval"])


if __name__ == "__main__":
    main()
