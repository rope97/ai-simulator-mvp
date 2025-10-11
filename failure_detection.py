import sqlite3
import datetime
from logger import log_vision

DB_PATH = 'database.db'

def detect_failures():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    now = datetime.datetime.now()

    # 1. Stuck print
    c.execute("SELECT printer_id, progress_percent, start_time FROM printers WHERE status = 'Running'")
    for printer_id, progress, start_time in c.fetchall():
        start_dt = datetime.datetime.fromisoformat(start_time)
        elapsed = (now - start_dt).total_seconds()
        if elapsed > 600 and progress < 20:
            log_vision(f"Printer {printer_id}: stuck at {progress}% after {elapsed:.0f} seconds")

    # 2. Air print
    c.execute("""
        SELECT p.printer_id, p.progress_percent, s.remaining_g
        FROM printers p
        JOIN spools s ON p.spool_id = s.spool_id
        WHERE p.status = 'Running'
    """)
    for printer_id, progress, remaining_g in c.fetchall():
        if remaining_g < 950 and progress < 10:  # primer granice
            log_vision(f" Printer {printer_id} might be air printing (material used, progress low)")

    # 3. Failed status
    c.execute("SELECT printer_id FROM printers WHERE status = 'Failed'")
    for printer_id, in c.fetchall():
        log_vision(f" Printer {printer_id} has failed!")

    # 4. Multiple failures
    c.execute("""
        SELECT COUNT(*) FROM printers WHERE status = 'Failed'
    """)
    fail_count = c.fetchone()[0]
    if fail_count > 2:
        log_vision(f" Warning: {fail_count} printers have failed simultaneously!")

    conn.close()

def detect_failures_loop():
    import time
    while True:
        detect_failures()
        time.sleep(2)

