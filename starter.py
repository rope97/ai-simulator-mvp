import threading
import subprocess
import time
from simulator import simulate_all_printers
from failure_detection import detect_failures, detect_failures_loop
from filamenttrack import monitor_filament_loop

def start_dashboard():
    """Runs the dashboard in a background process."""
    print("Launching Gradio dashboard on http://localhost:7860")
    subprocess.Popen(["python", "dashboard.py"])
    time.sleep(3)

dashboard_thread = threading.Thread(target=start_dashboard, daemon=True)
dashboard_thread.start()

print("Starting simulation and monitoring modules...")


sim_thread = threading.Thread(target=simulate_all_printers)
sim_thread.start()

detect_failures_thread = threading.Thread(target=detect_failures_loop, daemon=True)
detect_failures_thread.start()

filament_thread = threading.Thread(target=monitor_filament_loop, daemon=True)
filament_thread.start()


sim_thread.join()
print("Simulation finished. Vision module is still running (daemon=True).")

