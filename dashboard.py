import gradio as gr
import sqlite3
import pandas as pd

DB_PATH = "database.db"

def get_printer_status():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql("SELECT * FROM printers", conn)
    conn.close()
    return df

def show_dashboard():
    df = get_printer_status()
    return df

with gr.Blocks() as demo:
    gr.Markdown("### Printer Dashboard")
    table = gr.DataFrame(value=show_dashboard(), interactive=False)

demo.launch()

