import pandas as pd
import sqlite3
import os

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
def export_printers_csv():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM printers", conn)
    csv_path = os.path.join(DATA_DIR, "printers.csv")
    df.to_csv(csv_path, index=False)
    conn.close()
    print(f"Exported to {csv_path}")

def export_printers_xlsx():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql("SELECT * FROM printers", conn)
    xlsx_path = os.path.join(DATA_DIR, "printers.xlsx")
    df.to_excel(xlsx_path, index=False)
    conn.close()
    print(f"Exported to {xlsx_path}")

if __name__ == "__main__":
    print("Exporting printer data from database.db ...")
    export_printers_csv()
    export_printers_xlsx()
    print("Export complete.")

