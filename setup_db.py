import sqlite3
import random
DB_PATH = "database.db"

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS printers (
        printer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        serial_no TEXT,
        part_description TEXT,
        batch TEXT,
        part_name TEXT,
        status TEXT,
        machine TEXT,
        start_time TEXT,
        end_time TEXT,
        estimated_time_min INTEGER,
        material_g INTEGER,
        spool_id INTEGER,
        operator TEXT,
        job_id TEXT,
        error_message TEXT,
        progress_percent INTEGER	
    )
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS spools (
        spool_id INTEGER PRIMARY KEY AUTOINCREMENT,
        material_type TEXT,
        total_g INTEGER,
        remaining_g INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS events (
        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        printer_id INTEGER,
        event_type TEXT,
        message TEXT
    )
    """)

    printers = []
    operators = ["Alice", "Bob", "Charlie", "Dora", "Eve"]
    machines = [f"Printer-{i+1:02d}" for i in range(60)]

    for i in range(60):
        printers.append((
            f"SN-{i+1:03d}",                     # serial_no
            f"Part-{i+1}",                       # part_description
            f"Batch-{chr(65 + (i % 26))}",       # batch (A-Z)
            f"Component-{i+1}",                  # part_name
            "Idle",                              # status
            machines[i],                         # masina
            None, None,                          # start_time, end_time
            random.randint(60, 240),             # estimated_time_min
            None,                                # material_g
            (i % 3) + 1,                         # spool_id (rotiram izmedju 1–3)
            operators[i % len(operators)],       # operator
            f"JOB-{100 + i}",                    # job_id
            None,                                # error_message
            0                                    # progress_percent
        ))

    c.executemany("""
    INSERT INTO printers (serial_no, part_description, batch, part_name, status, machine, start_time, end_time,
                          estimated_time_min, material_g, spool_id, operator, job_id, error_message, progress_percent)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, printers)

    spools = [
        ("PLA", 1000, 1000),
        ("ABS", 1200, 1200),
        ("PETG", 800, 800)
    ]
    c.executemany("INSERT INTO spools (material_type, total_g, remaining_g) VALUES (?, ?, ?)", spools)

    conn.commit()
    conn.close()
    print("Database setup complete! Tables created and sample data inserted.")

if __name__ == "__main__":
    setup_database()

