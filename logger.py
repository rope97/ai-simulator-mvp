import os
from datetime import datetime

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

LOG_FILE_MAIN = os.path.join(DATA_DIR, "log.txt")
LOG_FILE_FILAMENT = os.path.join(DATA_DIR, "filament_log.txt")
LOG_FILE_VISION = os.path.join(DATA_DIR, "vision_log.txt")

def log_event(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE_MAIN, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_filament(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE_FILAMENT, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_vision(message):
    timestamp = datetime.now().isoformat()
    with open(LOG_FILE_VISION, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

