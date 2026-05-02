# WireTrip
(Anyone can improve this as it is fully open source)

Lightweight deception-based intrusion detection system for home labs and personal machines.

WireTrip generates realistic decoy files (“honeyfiles”) in common user directories and monitors them for any modification. If a file is accessed or changed, the event is logged locally for analysis.

It is designed for learning how file-based monitoring and deception techniques work in cybersecurity.

---

## Features

- Automatically deploys decoy files into standard user directories:
  - Documents
  - Downloads
  - Desktop

- Monitors file integrity using hash comparison
- Logs any detected changes with timestamps
- Minimal setup (single Python file)
- No external dependencies

---

## How it works

WireTrip creates harmless-looking files such as:

- backup_passwords.txt
- server_keys.txt
- old_config.txt

These files act as decoys.  
If any file is modified, WireTrip detects the change and logs it.

This is similar in concept to file integrity monitoring systems like Tripwire, used in security environments to detect unauthorized changes.

---

## Usage

```bash
python3 wiretrip.py
