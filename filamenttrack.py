import sqlite3
from logger import log_filament

DB_PATH = "database.db"
LOW_THRESHOLD = 0.15  # 15% filamenta

def check_filament():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT spool_id, total_g, remaining_g FROM spools")
    for spool_id, total, remaining in c.fetchall():
       if total == 0:
          continue     
       if remaining / total < LOW_THRESHOLD:
            log_filament(f"Spool {spool_id} low on filament: {remaining}/{total}g remaining")
    conn.close()

def monitor_filament_loop():
    import time
    while True:
        check_filament()
        time.sleep(5)

