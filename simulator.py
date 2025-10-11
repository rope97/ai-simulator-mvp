import random
import datetime
import time
import sqlite3
import threading
from logger import log_event

DB_PATH = 'database.db'

def simulate_print(printer_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Uzmi podatke o printeru
    c.execute("SELECT status, spool_id, estimated_time_min FROM printers WHERE printer_id = ?", (printer_id,))
    printer = c.fetchone()
    if not printer:
        print(f"Printer {printer_id} not found.")
        return

    status, spool_id, estimated_time = printer
    if status != "Idle":
        print(f"Printer {printer_id} is already busy.")
        return

    start_time = datetime.datetime.now().isoformat()
    c.execute("UPDATE printers SET status = ?, start_time = ? WHERE printer_id = ?", ("Running", start_time, printer_id))
    conn.commit()

    print(f"Printer {printer_id} started printing...")
    for progress in range(0, 101, 20):  # koraci po 20%
    # Simulacija zastoja (10% šanse da se printer zaglavi)
        if random.random() < 0.1:
            log_event(f"Printer {printer_id}: progress stalled at {progress}%")
            time.sleep(3)
            continue

    c.execute("UPDATE printers SET progress_percent = ? WHERE printer_id = ?", (progress, printer_id))
    conn.commit()
    log_event(f"Printer {printer_id}: progress {progress}%")
    time.sleep(0.5)  
  
    success = random.choice([True, True, False])  #25-30% chance to fail

    material_used = random.randint(50, 150)
    c.execute("UPDATE spools SET remaining_g = remaining_g - ? WHERE spool_id = ?", (material_used, spool_id))

    end_time = datetime.datetime.now().isoformat()
    new_status = "Completed" if success else "Failed"
    error_message = None if success else "Layer shift detected"

    c.execute("""
        UPDATE printers
        SET status = ?, end_time = ?, material_g = ?, error_message = ?
        WHERE printer_id = ?
    """, (new_status, end_time, material_used, error_message, printer_id))

    c.execute("""
        INSERT INTO events (timestamp, printer_id, event_type, message)
        VALUES (?, ?, ?, ?)
    """, (datetime.datetime.now().isoformat(), printer_id, new_status, error_message or "Print completed."))

    conn.commit()
    conn.close()

    log_event(f"Printer {printer_id}: {new_status} (used {material_used}g)")

    print(f"Print {new_status} for printer {printer_id}.")

def simulate_all_printers():
    threads = []

    for printer_id in random.sample(range(1, 60),15):
         t = threading.Thread(target=simulate_print, args=(printer_id,))
         threads.append(t)
         t.start()
 
    for t in threads:
        t.join()
    print("\n all simulation are done")
 
if __name__ == "__main__":
    simulate_all_printers()
