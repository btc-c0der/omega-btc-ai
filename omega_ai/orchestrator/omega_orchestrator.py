# 🚀 Omega AI Microservices Orchestrator
import subprocess
import time
import os
import threading

# ✅ Define microservices to manage
MICROSERVICES = {
    "MM Trap Detector": "omega_ai/services/mm_trap_detection/mm_trap_detector.py",
    "BTC Live Feed": "omega_ai/services/live/feed/btc_live_feed.py",
    "Alerts Manager": "omega_ai/services/alerts/alerts_manager.py",
    "API Gateway": "omega_ai/services/api_gateway.py"
}

# ✅ Function to start a service
def start_service(name, script):
    print(f"🚀 Starting {name}...")
    return subprocess.Popen(["python", script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# ✅ Function to monitor & restart microservices
def monitor_services():
    processes = {}

    while True:
        for name, script in MICROSERVICES.items():
            if name not in processes or processes[name].poll() is not None:
                print(f"⚠️ {name} stopped or failed! Restarting...")
                processes[name] = start_service(name, script)

        time.sleep(5)  # Monitor every 5 seconds

# ✅ Function to secure inter-service communication
def secure_communication():
    print("🔐 Securing Microservice Communication...")
    os.environ["OMEGA_SECURITY_KEY"] = "JAH-BLESS-THE-GRID"
    # Future: Implement encrypted messaging between services

# ✅ Start the orchestrator
if __name__ == "__main__":
    secure_communication()
    print("🔱 OMEGA GRID ORCHESTRATOR ACTIVE 🔱")

    # ✅ Launch monitoring in a separate thread
    threading.Thread(target=monitor_services, daemon=True).start()

    # ✅ Keep orchestrator running
    while True:
        time.sleep(60)  # Keep main script alive
