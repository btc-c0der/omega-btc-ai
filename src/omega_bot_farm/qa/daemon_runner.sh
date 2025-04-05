#!/bin/bash
# CyBer1t4L QA Bot Standalone Daemon Runner
# This script starts the CyBer1t4L bot in a persistent screen session

# Configuration
PROJECT_ROOT="/Users/fsiqueira/Desktop/GitHub/omega-btc-ai"
LOG_DIR="$PROJECT_ROOT/src/omega_bot_farm/qa/local_run/logs"
DAEMON_LOG="$LOG_DIR/daemon_standalone_$(date +%Y%m%d_%H%M%S).log"
PID_FILE="$PROJECT_ROOT/src/omega_bot_farm/qa/local_run/cyber1t4l.pid"
PYTHON_PATH="$PROJECT_ROOT/venv/bin/python"
SCREEN_NAME="cyber1t4l_bot"

# Make sure directories exist
mkdir -p "$LOG_DIR"

# Log startup
echo "Starting standalone daemon at $(date)" > "$DAEMON_LOG"
echo "Project root: $PROJECT_ROOT" >> "$DAEMON_LOG"
echo "Python path: $PYTHON_PATH" >> "$DAEMON_LOG"

# Check if screen is installed
if ! command -v screen >/dev/null 2>&1; then
    echo "Error: 'screen' is not installed. Please install screen to run the daemon." | tee -a "$DAEMON_LOG"
    exit 1
fi

# Navigate to project root
cd "$PROJECT_ROOT" || { 
    echo "Failed to navigate to project root" | tee -a "$DAEMON_LOG"
    exit 1
}

# Kill any existing screen sessions with the same name
screen -ls | grep "$SCREEN_NAME" | cut -d. -f1 | awk '{print $1}' | xargs -I{} screen -XS {} quit >/dev/null 2>&1

# Start a new screen session
COMMAND="cd $PROJECT_ROOT && $PYTHON_PATH -m src.omega_bot_farm.qa.run_cyber1t4l_locally --mode coverage"
echo "Starting command: $COMMAND" >> "$DAEMON_LOG"

# Launch the bot in a detached screen session
screen -dmS "$SCREEN_NAME" bash -c "$COMMAND"

# Check if screen session started
if screen -ls | grep -q "$SCREEN_NAME"; then
    echo "Screen session $SCREEN_NAME started successfully" | tee -a "$DAEMON_LOG"
    
    # Get the PID of the screen session (this is not the Python process PID)
    SCREEN_PID=$(screen -ls | grep "$SCREEN_NAME" | cut -d. -f1 | awk '{print $1}')
    echo "Screen session PID: $SCREEN_PID" >> "$DAEMON_LOG"
    
    # Wait a few seconds for the Python process to start
    sleep 5
    
    # Find the Python process
    PYTHON_PID=$(pgrep -f "python.*run_cyber1t4l_locally")
    
    if [ -n "$PYTHON_PID" ]; then
        echo "Python process started with PID: $PYTHON_PID" | tee -a "$DAEMON_LOG"
        echo "$PYTHON_PID" > "$PID_FILE"
        echo "Updated PID file: $PID_FILE" >> "$DAEMON_LOG"
        echo "Success!" | tee -a "$DAEMON_LOG"
        exit 0
    else
        echo "Python process not found after waiting. Check logs for errors." | tee -a "$DAEMON_LOG"
        # Print recent logs for debugging
        RECENT_LOG=$(ls -t "$LOG_DIR"/cyber1t4l_*.log 2>/dev/null | head -1)
        if [ -n "$RECENT_LOG" ]; then
            echo "Recent log file: $RECENT_LOG" >> "$DAEMON_LOG"
            echo "Last 20 lines of log:" >> "$DAEMON_LOG"
            tail -20 "$RECENT_LOG" >> "$DAEMON_LOG"
        fi
        exit 1
    fi
else
    echo "Failed to start screen session" | tee -a "$DAEMON_LOG"
    exit 1
fi 