
# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸

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