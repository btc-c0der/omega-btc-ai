#!/bin/bash

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

set -e

echo "🚀 Starting OmegaBTC AI Trading System..."

# Set up database tables
echo "📊 Setting up PostgreSQL database..."
python -c "from omega_ai.db_manager.database import setup_database; setup_database()"

# Start services in proper dependency order
echo "🔌 Starting core services..."

# 1. Start database monitoring
python -m omega_ai.db_manager.database &
PID_DB=$!

# 2. Start Schumann resonance monitoring
python -m omega_ai.data_feed.schumann_monitor &
PID_SCHUMANN=$!

# 3. Start BTC price feed
python -m omega_ai.data_feed.btc_live_feed &
PID_BTC_FEED=$!

# Wait for data services to initialize
sleep 5

# 4. Start Grafana metrics reporter
python -m omega_ai.reporting.grafana_reporter &
PID_GRAFANA=$!

# 5. Start Fibonacci detector
python -m omega_ai.mm_trap_detector.fibonacci_detector &
PID_FIBONACCI=$!

# 6. Start WebSocket server
python -m omega_ai.mm_trap_detector.mm_websocket_server &
PID_WS=$!

# 7. Start high-frequency detector
python3 -m omega_ai.mm_trap_detector.high_frequency_detector &
PID_HF_DETECTOR=$!

# 8. Start MM trap detector
python3 -m omega_ai.mm_trap_detector.mm_trap_detector &
PID_PROCESSOR=$!

# 10. Start market monitor
python -m omega_ai.monitor.monitor_market_trends &
PID_MARKET_MONITOR=$!

# 11. Start health check
python health_check.py &
PID_HEALTH_CHECK=$!

# Store all PIDs for proper shutdown
echo "$PID_DB $PID_SCHUMANN $PID_BTC_FEED $PID_GRAFANA $PID_FIBONACCI $PID_WS $PID_HF_DETECTOR $PID_PROCESSOR $PID_MARKET_MONITOR $PID_HEALTH_CHECK" > /app/pids.txt

echo "✅ All services started!"

# Keep container running and handle SIGTERM for clean shutdown
trap 'kill $(cat /app/pids.txt)' SIGTERM SIGINT
wait
