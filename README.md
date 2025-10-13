#3D Printer Monitoring MVP

## Overview

This project is a **Minimum Viable Product (MVP)** of an AI-driven system for monitoring and detecting issues in 3D printing operations.  
It simulates multiple 3D printers, tracks their progress and filament usage, detects failures using heuristic AI methods, and provides a **real-time dashboard interface** built with **Gradio**.

The goal is to demonstrate an **AI-assisted monitoring system** that integrates simulation, detection, and visualization — not to build a production-grade tool.

---

##Features

### 1. Simulator (`simulator.py`)
- Simulates up to **60 printers**, randomly selecting **15** to run in parallel per batch.
- Generates random print outcomes:
  Successful prints**
  -Failed prints** (“Layer shift detected”)
  - Stuck prints**
- Updates the **SQLite database** (`database.db`).
- Logs activity in `data/log.txt`.

---

### 2. Failure Detection (`failure_detection.py`)
- Continuously monitors the `printers` table for anomalies:
  - Stuck prints** — progress not changing after a set time.
  - Air prints** — filament used but little to no progress.
  - Failed printers** — directly marked as failed.
  - Multiple simultaneous failures** — possible systemic issue.
- Logs events in `data/vision_log.txt`.

---

### 3. Filament Tracker (`filamenttracker.py`)
- Monitors filament usage from the `spools` table.
- Triggers alerts when remaining filament drops below **15%**.
- Logs events in `data/filament_log.txt`.

---

### 4. Logger (`logger.py`)
Centralized logging system:
- `log_event()` → general activity log (`data/log.txt`)
- `log_vision()` → AI/failure detection log (`data/vision_log.txt`)
- `log_filament()` → filament usage log (`data/filament_log.txt`)

All logs are automatically created inside the `data/` directory.

---

### 5. Dashboard (`dashboard.py`)
- Built using **Gradio**.
- Displays:
  - Printer statuses (Running, Completed, Failed)
  - Filament levels per spool
  - Event logs and alerts
- Updates in real time as the simulation and monitoring modules run.
- Automatically launches before the simulation when you run `starter.py`.

---

## Database Structure

**SQLite (`database.db`)** contains:
- `printers` — printer job info (status, start/end times, progress, etc.)
- `spools` — material info and remaining filament
- `events` — system-wide events and alerts

Initialized with sample data using `setup_db.py`.

---

##How It Works

 **Dashboard Launch**  
   When you run `starter.py`, the Gradio dashboard automatically launches first (on `http://localhost:7860`).

 **Simulation Begins**  
   The simulator starts running 15 random printers, updating their states in the database.

 **AI Monitoring**  
   `failure_detection.py` continuously checks for failure patterns and logs alerts.

 **Filament Monitoring**  
   `filamenttracker.py` monitors all spools and triggers low-filament alerts.

 **Real-Time Visualization**  
   The dashboard updates live from the database, showing progress and alerts in real time.

---

#Installation & Run

# Clone Repository
```bash
git clone https://github.com/yourusername/3d-printer-mvp.git
cd 3d-printer-mvp


#Create virtual environment (linux,macos)
python3 -m venv venv
source venv/bin/activate

#Install Dependencies
pip install -r requirements.txt

#Initialize Database
python setup_db.py

#Run the Simulation with Dashboard
python startrer.py

This will automatically:Launch the Gradio dashboard on localchost:7860 (dashboard.py),start the printer simulatoir(simulator.py),run the AI failure detection (failure_detection.py),run the filament tracker(filamenttracker.py)

### Export Data
After running a simulation, you can export the latest printer data to CSV and Excel:

```bash
python export.py

------------
-----------
Project Structure 

python_digital/
├── data/                  # log files
│   ├── log.txt
│   ├── filament_log.txt
│   └── vision_log.txt
├── simulator.py            # printer simulation
├── failure_detection.py    # heuristic AI detection
├── filamenttracker.py      # filament monitoring
├── logger.py               # centralized logging
├── dashboard.py            # Gradio dashboard UI
├── setup_db.py             # initialize SQLite database
├── starter.py              # launches all modules except setup_db.py
├── database.db             # SQLite database
├── README.md
└── venv/                   # Python virtual environment


Technologies Used

Python 3
SQLite — lightweight local database
threading — concurrent simulation and monitoring
Gradio — interactive web dashboard
Pandas — optional CSV export
Rule-based print failure detection

Suma suamrum -*-->

#/Each module can be run independently for testing.
#All logs are stored in the data/ directory.
#The system demonstrates:
#Real-time monitoring of printers and filament and automated anomaly detection
#Live visualization via Gradio UI
```


## Author

* **Danica Dimitrijevic*
