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


# MIT License
#
# Copyright (c) 2024 OMEGA BTC AI Team
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# Market Maker Trap Simulator Daemon
# This script runs the trap simulator as a daemon process
# Usage: ./run_simulator_daemon.sh [start|stop|status]

# Config
PYTHON_PATH="python"
LOG_FILE="$HOME/trap_simulator.log"
PID_FILE="$HOME/trap_simulator.pid"
PROGRAM_PATH="omega_ai.mm_trap_detector.trap_simulation_service"

# Default simulation parameters
VOLATILITY=1.2
FREQUENCY=0.25
SLEEP=0.1

# Colors
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

function start_daemon() {
    echo -e "${YELLOW}Starting Market Maker Trap Simulator Daemon...${RESET}"
    
    # Check if already running
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null; then
            echo -e "${RED}Simulator is already running with PID $PID${RESET}"
            return 1
        else
            echo -e "${YELLOW}Stale PID file found. Removing...${RESET}"
            rm "$PID_FILE"
        fi
    fi
    
    # Start the simulator as a background process
    nohup $PYTHON_PATH -m $PROGRAM_PATH \
        --volatility $VOLATILITY \
        --frequency $FREQUENCY \
        --sleep $SLEEP \
        > "$LOG_FILE" 2>&1 &
    
    # Save the PID
    echo $! > "$PID_FILE"
    echo -e "${GREEN}Simulator started with PID $!${RESET}"
    echo -e "${GREEN}Log file: $LOG_FILE${RESET}"
}

function stop_daemon() {
    echo -e "${YELLOW}Stopping Market Maker Trap Simulator...${RESET}"
    
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${RED}PID file not found. Simulator may not be running.${RESET}"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ! ps -p "$PID" > /dev/null; then
        echo -e "${RED}Process not found. Cleaning up stale PID file.${RESET}"
        rm "$PID_FILE"
        return 1
    fi
    
    echo -e "${YELLOW}Sending SIGTERM to PID $PID...${RESET}"
    kill "$PID"
    
    # Wait for process to end
    for i in {1..5}; do
        if ! ps -p "$PID" > /dev/null; then
            echo -e "${GREEN}Simulator stopped successfully.${RESET}"
            rm "$PID_FILE"
            return 0
        fi
        sleep 1
    done
    
    # Force kill if still running
    echo -e "${RED}Process did not terminate gracefully. Forcing...${RESET}"
    kill -9 "$PID"
    rm "$PID_FILE"
    echo -e "${YELLOW}Simulator forcefully terminated.${RESET}"
}

function status_daemon() {
    if [ ! -f "$PID_FILE" ]; then
        echo -e "${RED}Simulator is not running.${RESET}"
        return 1
    fi
    
    PID=$(cat "$PID_FILE")
    if ps -p "$PID" > /dev/null; then
        echo -e "${GREEN}Simulator is running with PID $PID${RESET}"
        echo -e "${YELLOW}Process details:${RESET}"
        ps -f -p "$PID"
        
        echo -e "\n${YELLOW}Recent log entries:${RESET}"
        tail -n 10 "$LOG_FILE"
        return 0
    else
        echo -e "${RED}PID file exists but process is not running.${RESET}"
        echo -e "${YELLOW}Cleaning up stale PID file...${RESET}"
        rm "$PID_FILE"
        return 1
    fi
}

# Main execution
case "$1" in
    start)
        start_daemon
        ;;
    stop)
        stop_daemon
        ;;
    restart)
        stop_daemon
        sleep 2
        start_daemon
        ;;
    status)
        status_daemon
        ;;
    *)
        echo -e "Usage: $0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0 