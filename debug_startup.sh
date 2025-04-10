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


# OMEGA BTC AI - Startup Debugging Script
# This script runs diagnostic checks and tests to help identify startup issues

echo "=========================================================="
echo "= OMEGA BTC AI - Startup Debugging Script                ="
echo "=========================================================="
echo ""

# Check environment and system status
echo "Checking environment..."
echo "Python version: $(python --version 2>&1)"
echo "Python path: $(which python)"
echo "Working directory: $(pwd)"
echo ""

# Check if Redis is running
echo "Checking Redis status..."
if command -v redis-cli > /dev/null; then
    redis_ping=$(redis-cli ping 2>/dev/null)
    if [ "$redis_ping" = "PONG" ]; then
        echo "✅ Redis is running and responding to PING"
    else
        echo "❌ Redis is not responding to PING. Make sure Redis is running."
        echo "   Try starting Redis with: redis-server"
    fi
    
    echo "Redis info:"
    redis-cli info | grep -E 'redis_version|connected_clients|used_memory_human|used_memory_peak_human'
else
    echo "❌ redis-cli not found. Please install Redis or add it to your PATH."
fi
echo ""

# Check environment variables
echo "Checking required environment variables..."
required_vars=(
    "BITGET_API_KEY"
    "BITGET_SECRET_KEY"
    "BITGET_PASSPHRASE"
    "REDIS_HOST"
    "REDIS_PORT"
)

for var in "${required_vars[@]}"; do
    if [ -n "${!var}" ]; then
        echo "✅ $var is set"
        if [[ "$var" == *"KEY"* || "$var" == *"PASSPHRASE"* ]]; then
            echo "   Value: ${!var:0:5}... (hidden for security)"
        elif [[ "$var" == *"HOST"* || "$var" == *"PORT"* ]]; then
            echo "   Value: ${!var}"
        fi
    else
        echo "❌ $var is not set"
    fi
done
echo ""

# Check for required files
echo "Checking required files..."
critical_files=(
    "omega_ai/trading/strategies/trap_aware_dual_traders.py"
    "omega_ai/trading/exchanges/dual_position_traders.py"
    "omega_ai/trading/exchanges/bitget_ccxt.py"
    "omega_ai/tools/trap_probability_meter.py"
    "run_trap_aware_traders.sh"
)

for file in "${critical_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file is missing"
    fi
done
echo ""

# Run Python module imports test
echo "Testing Python module imports..."
python -c "
import sys
try:
    import redis
    print('✅ redis module imported successfully')
except ImportError as e:
    print('❌ Failed to import redis:', e)

try:
    from omega_ai.trading.exchanges.bitget_ccxt import BitGetCCXT
    print('✅ BitGetCCXT imported successfully')
except ImportError as e:
    print('❌ Failed to import BitGetCCXT:', e)

try:
    from omega_ai.trading.exchanges.dual_position_traders import BitGetDualPositionTraders
    print('✅ BitGetDualPositionTraders imported successfully')
except ImportError as e:
    print('❌ Failed to import BitGetDualPositionTraders:', e)

try:
    from omega_ai.trading.strategies.trap_aware_dual_traders import TrapAwareDualTraders
    print('✅ TrapAwareDualTraders imported successfully')
except ImportError as e:
    print('❌ Failed to import TrapAwareDualTraders:', e)
"
echo ""

# Test Redis connectivity directly
echo "Testing Redis connectivity from Python..."
python -c "
import redis
try:
    r = redis.Redis(host='localhost', port=6379, socket_connect_timeout=2.0)
    response = r.ping()
    if response:
        print('✅ Connected to Redis successfully')
    else:
        print('❌ Redis ping returned:', response)
except Exception as e:
    print('❌ Redis connection error:', e)
"
echo ""

# Get available RAM and disk space
echo "Checking system resources..."
if command -v free > /dev/null; then
    echo "Memory usage:"
    free -h
else
    # If free is not available (e.g., on macOS)
    echo "Memory info:"
    if command -v vm_stat > /dev/null; then
        # macOS memory info
        vm_stat | perl -ne '/page size of (\d+)/ and $size=$1; /Pages\s+([^:]+)[^\d]+(\d+)/ and printf("%-16s % 16.2f MB\n", "$1:", $2 * $size / 1048576);'
    else
        echo "Unable to get memory information (vm_stat not available)"
    fi
fi

echo "Disk space:"
df -h .
echo ""

# Run with verbose mode and capture output
echo "Running the trap-aware dual traders with verbose logging..."
echo "This will take a few seconds. Press Ctrl+C after you see ERROR or STOPPED status."
echo ""

# Create temp files for output
STDOUT_LOG="trap_startup_debug_stdout.log"
STDERR_LOG="trap_startup_debug_stderr.log"

# Function to clean up on exit
cleanup() {
    echo "Stopping processes..."
    if [ -n "$PID" ]; then
        kill "$PID" 2>/dev/null
    fi
    echo "Debug completed. Check the logs for more information:"
    echo "  - $STDOUT_LOG (Standard output)"
    echo "  - $STDERR_LOG (Error output)"
    exit 0
}

# Set up trap
trap cleanup INT TERM

# Run the trap-aware traders with debug output
python -m omega_ai.trading.strategies.trap_aware_dual_traders \
    --symbol BTCUSDT \
    --long-capital 150.0 \
    --short-capital 200.0 \
    --long-leverage 11 \
    --short-leverage 11 \
    --min-free-balance 0.0 \
    > "$STDOUT_LOG" 2> "$STDERR_LOG" &

PID=$!

echo "Process started with PID: $PID"
echo "Waiting for output..."

# Wait for a few seconds
sleep 5

# Check if process is still running
if kill -0 $PID 2>/dev/null; then
    echo "Process is still running."
else
    echo "Process exited quickly. Checking logs..."
fi

# Show the most recent logs
echo "Most recent standard output:"
tail -n 20 "$STDOUT_LOG"
echo ""
echo "Most recent error output:"
tail -n 20 "$STDERR_LOG"
echo ""

echo "Analyzing logs for common errors..."
# Look for specific error patterns
if grep -q "Error getting trap probability" "$STDOUT_LOG"; then
    echo "⚠️ Trap probability error detected. This could indicate Redis issues."
fi

if grep -q "Redis connectivity test: FAILED" "$STDOUT_LOG"; then
    echo "⚠️ Redis connectivity test failed. Make sure Redis is running."
fi

if grep -q "Account limit check failed" "$STDOUT_LOG"; then
    echo "⚠️ Account limit check failed. Check your balance settings."
fi

if grep -q "CRITICAL ERROR during initialization" "$STDOUT_LOG" || grep -q "CRITICAL ERROR during initialization" "$STDERR_LOG"; then
    echo "⚠️ Critical initialization error detected. Check detailed logs."
fi

if grep -q "Error in main:" "$STDOUT_LOG"; then
    echo "⚠️ Main function error detected. Check detailed logs."
fi

echo ""
echo "Debug complete. Press Enter to continue monitoring, or Ctrl+C to exit."
echo "You can use 'tail -f $STDOUT_LOG' to continuously monitor the output."

read -r

# Start continuous monitoring of the logs
tail -f "$STDOUT_LOG" 