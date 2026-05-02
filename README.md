# WireTrip

Lightweight deception-based intrusion detection system for home labs.

WireTrip creates harmless decoy files (“honeyfiles”) and monitors them for any access or modification. If a file is interacted with, it logs the event for analysis.

This helps simulate and study suspicious activity in a controlled environment.

---

## Features

- Automatically generates decoy files in safe directories
- Monitors file access and modification
- Logs suspicious activity with timestamps
- Optional process detection for forensic analysis
- Designed for local/home lab use only

---

## Usage

```bash
python3 wiretrip.py
