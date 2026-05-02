from pathlib import Path
import random
import time
import hashlib
from datetime import datetime

# =========================
# CONFIG
# =========================

HOME = Path.home()

TARGET_DIRS = [
    HOME / "Documents",
    HOME / "Downloads",
    HOME / "Desktop"
]

BAIT_FILES = [
    "backup_passwords.txt",
    "server_keys.txt",
    "old_config.txt",
    "notes_admin.txt",
    "wallet_backup.txt"
]

LOG_FILE = HOME / ".wiretrip_log.txt"
SCAN_INTERVAL = 2

file_hashes = {}

# =========================
# SETUP BAIT FILES
# =========================

def deploy_decoys():
    for _ in range(len(BAIT_FILES)):

        folder = random.choice(TARGET_DIRS)
        filename = random.choice(BAIT_FILES)

        path = folder / filename

        if not path.exists():
            path.write_text("SYSTEM BACKUP FILE - DO NOT MODIFY\n")
            print(f"[WireTrip] deployed -> {path}")

# =========================
# HASHING
# =========================

def hash_file(path):
    try:
        h = hashlib.sha256()
        h.update(path.read_bytes())
        return h.hexdigest()
    except:
        return None

# =========================
# LOGGING
# =========================

def log_event(path):
    entry = f"[{datetime.now()}] ACCESS DETECTED -> {path}\n"

    with open(LOG_FILE, "a") as f:
        f.write(entry)

    print(entry.strip())

# =========================
# INITIAL STATE
# =========================

def init_state():
    for folder in TARGET_DIRS:
        for file in folder.glob("*"):
            if file.is_file():
                file_hashes[file] = hash_file(file)

# =========================
# MONITOR LOOP
# =========================

def monitor():
    while True:

        for folder in TARGET_DIRS:
            for file in folder.glob("*"):

                if file.is_file():

                    current = hash_file(file)

                    if file not in file_hashes:
                        file_hashes[file] = current
                        continue

                    if file_hashes[file] != current:
                        log_event(file)
                        file_hashes[file] = current

        time.sleep(SCAN_INTERVAL)

# =========================
# BANNER
# =========================

def banner():
    print("""
========================
        WIRETRIP
  Deception IDS (Lab Tool)
========================
""")

# =========================
# MAIN
# =========================

def main():
    banner()

    print("[*] Deploying decoy files...")
    deploy_decoys()

    print("[*] Initializing state...")
    init_state()

    print("[*] Monitoring system...\n")

    monitor()

if __name__ == "__main__":
    main()
