import threading
from omega_ai.mm_trap_detector.grafana_reporter import update_grafana_metrics

if __name__ == "__main__":
    print("🚀 Starting Grafana Reporter for MM Trap Visualization")
    
    # Start the metrics updater in a background thread
    metrics_thread = threading.Thread(target=update_grafana_metrics, daemon=True)
    metrics_thread.start()
    
    print("✅ Grafana Reporter started successfully")
    
    # Keep main thread alive
    try:
        while True:
            metrics_thread.join(1)
    except KeyboardInterrupt:
        print("📴 Grafana Reporter shutting down")