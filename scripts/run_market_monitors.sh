#!/bin/bash

# OMEGA BTC AI - Market Trend Monitors Runner
# This script runs both the original and AI-enhanced market trend monitors in tmux sessions
# Located in: /scripts/run_market_monitors.sh

# Terminal colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${MAGENTA}${BOLD}
╔════════════════════════════════════════════════════════════╗
║        OMEGA BTC AI - DIVINE MARKET TREND MONITORS         ║
║           🧠 FIBONACCI PATTERN RECOGNITION 🧠             ║
╚════════════════════════════════════════════════════════════╝${NC}"

# Check if tmux is installed
if ! command -v tmux &> /dev/null; then
    echo -e "${RED}Error: tmux is not installed. Please install tmux to run monitors.${NC}"
    exit 1
fi

# Check if Redis is running (required for Fibonacci data)
if ! redis-cli ping > /dev/null 2>&1; then
    echo -e "${RED}Warning: Redis server not running. Fibonacci levels may not be available.${NC}"
    echo -e "${YELLOW}Starting Redis server...${NC}"
    # Try to start Redis if possible
    if command -v redis-server &> /dev/null; then
        redis-server --daemonize yes
        sleep 2
        if redis-cli ping > /dev/null 2>&1; then
            echo -e "${GREEN}Redis server started successfully.${NC}"
        else
            echo -e "${RED}Failed to start Redis server. Fibonacci levels may not appear.${NC}"
        fi
    else
        echo -e "${RED}Redis-server not found. Please install Redis for full functionality.${NC}"
    fi
fi

# Check if Fibonacci levels already exist in Redis
echo -e "${CYAN}Checking Fibonacci levels...${NC}"
# Run a Python command to check and initialize Fibonacci levels
python3 -c "
import sys
import json
from datetime import datetime, timedelta
try:
    import redis
    r = redis.Redis()
    
    # Check if complete fibonacci levels exist
    fib_levels_json = r.get('fibonacci_levels')
    current_time = datetime.now()
    
    if fib_levels_json:
        # Fibonacci levels exist, check if they're recent enough
        fib_levels = json.loads(fib_levels_json)
        last_update = datetime.fromisoformat(fib_levels.get('timestamp', '2000-01-01T00:00:00+00:00'))
        time_diff = current_time - last_update
        
        if time_diff < timedelta(hours=6):
            print('Using cached Fibonacci levels from: ' + fib_levels.get('timestamp', 'unknown'))
            sys.exit(0)
        else:
            print('Cached Fibonacci levels too old, recalculating...')
    
    # Get current BTC price
    current_price = r.get('last_btc_price')
    if not current_price:
        current_price = '60000.0'  # Fallback price
    
    price = float(current_price)
    
    # Calculate Fibonacci levels
    # For an uptrend (assuming base_price is swing high)
    swing_high = price
    swing_low = price * 0.9  # Assuming swing low is 10% below current price
    
    fib_levels = {
        'base_price': price,
        'direction': 'up',
        'levels': {
            '0': swing_high,
            '0.236': swing_high - (0.236 * (swing_high - swing_low)),
            '0.382': swing_high - (0.382 * (swing_high - swing_low)),
            '0.5': swing_high - (0.5 * (swing_high - swing_low)),
            '0.618': swing_high - (0.618 * (swing_high - swing_low)),
            '0.786': swing_high - (0.786 * (swing_high - swing_low)),
            '1.0': swing_low,
            '1.618': swing_low - (0.618 * (swing_high - swing_low)),
            '2.618': swing_low - (1.618 * (swing_high - swing_low))
        },
        'swing_high': swing_high,
        'swing_low': swing_low,
        'timestamp': current_time.isoformat()
    }
    
    # Store complete fib levels in Redis
    r.set('fibonacci_levels', json.dumps(fib_levels))
    r.set('fib_base_price', str(price))
    r.set('fib_last_update', current_time.isoformat())
    
    # Set TTL for 6 hours to ensure they're refreshed periodically
    r.expire('fibonacci_levels', 21600)  # 6 hours in seconds
    
    print(f'Fibonacci levels calculated and cached based on price: {price}')
except Exception as e:
    print(f'Error with Fibonacci levels: {e}')
    sys.exit(1)
"

# Kill existing tmux sessions if they exist
tmux kill-session -t "market_monitors" &> /dev/null

# Create new tmux session
echo -e "${BLUE}Creating tmux session for market monitors...${NC}"
tmux new-session -d -s "market_monitors"

# Split window horizontally 50/50
tmux split-window -h -t "market_monitors"

# Set window names
tmux rename-window -t "market_monitors" "MARKET_TREND_MONITORS"

# Configure tmux status bar
tmux set -g status-style "bg=black,fg=green"
tmux set -g status-left "#[fg=green,bold][OMEGA BTC AI] #[fg=cyan]Market Monitors #[fg=yellow]| "
tmux set -g status-right "#[fg=cyan]%H:%M:%S #[fg=yellow]| #[fg=green,bold]FIBONACCI ACTIVE #[fg=default]"
tmux set -g status-left-length 50
tmux set -g status-right-length 50

# Start original market trend monitor in the left pane with FIXED_DISPLAY mode
echo -e "${YELLOW}Starting original market trend monitor...${NC}"
tmux send-keys -t "market_monitors:0.0" "cd $(pwd) && FIXED_DISPLAY=true python -m omega_ai.monitor.monitor_market_trends_fixed" C-m

# Start AI-enhanced market trend monitor in the right pane with FIXED_DISPLAY mode
echo -e "${CYAN}Starting AI-enhanced market trend monitor...${NC}"
tmux send-keys -t "market_monitors:0.1" "cd $(pwd) && FIXED_DISPLAY=true python -m omega_ai.monitor.market_trends_monitor_ai" C-m

# Attach to the tmux session
echo -e "${GREEN}${BOLD}Monitors started successfully! Attaching to tmux session...${NC}"
echo -e "${YELLOW}Press Ctrl+B then D to detach from the session${NC}"
sleep 2
tmux attach-session -t "market_monitors"

# If we get here, the session has been detached
echo -e "${GREEN}Session detached. The monitors continue to run in the background.${NC}"
echo -e "${CYAN}To reattach: tmux attach -t market_monitors${NC}" 