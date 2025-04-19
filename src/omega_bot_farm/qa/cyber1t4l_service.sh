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

#
# CyBer1t4L QA Bot Service Controller
# Manages the CyBer1t4L bot as a background service
#

# Configuration
SERVICE_NAME="cyber1t4l_qa_bot"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
LOG_DIR="$SCRIPT_DIR/local_run/logs"
PID_FILE="$SCRIPT_DIR/local_run/cyber1t4l.pid"
SERVICE_LOG="$SCRIPT_DIR/local_run/service.log"

# Default options - can be overridden by editing this file
DEFAULT_MODE="coverage"
DEFAULT_OPTIONS="--mode $DEFAULT_MODE"
DEBUG=false

# Make sure directories exist
mkdir -p "$LOG_DIR"
mkdir -p "$(dirname "$PID_FILE")"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Debug function
debug() {
    if [ "$DEBUG" = true ]; then
        echo -e "${YELLOW}[DEBUG] $1${NC}" >&2
    fi
}

# Banner
show_banner() {
    echo -e "${CYAN}"
    echo "  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗████████╗██╗  ██╗██╗     "
    echo " ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██║  ██║██║     "
    echo " ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██║     "
    echo " ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██╔══██║██║     "
    echo " ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║███████╗"
    echo "  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝"
    echo -e "${GREEN}"
    echo " 🔴 🟡 🟢  SERVICE CONTROLLER  🔴 🟡 🟢"
    echo -e "${NC}"
}

# Check if the bot is running
is_running() {
    # First check if our PID file exists and points to a valid process
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        debug "Found PID file with PID: $PID"
        
        # Only proceed if PID is not empty
        if [ -n "$PID" ]; then
            # Check if process exists
            if ps -p "$PID" > /dev/null 2>&1; then
                # Verify it's our process by checking command line
                CMDLINE=$(ps -p "$PID" -o command= 2>/dev/null)
                debug "Process command line: $CMDLINE"
                
                if echo "$CMDLINE" | grep -q "run_cyber1t4l_locally\|daemon_runner.sh"; then
                    debug "PID $PID confirmed as CyBer1t4L process"
                    return 0 # Running
                else
                    debug "Process with PID $PID exists but is not CyBer1t4L"
                    # Clean up stale PID file
                    rm -f "$PID_FILE"
                fi
            else
                debug "Process with PID $PID not found"
                # Clean up stale PID file
                rm -f "$PID_FILE"
            fi
        else
            debug "PID file exists but contains empty PID"
            rm -f "$PID_FILE"
        fi
    fi
    
    # Second, look for any running processes that match the CyBer1t4L pattern
    debug "Looking for CyBer1t4L processes by pattern"
    
    # Look for both Python modules and shell scripts
    CYBER_PIDS=$(pgrep -f "run_cyber1t4l_locally")
    DAEMON_PIDS=$(pgrep -f "daemon_runner.sh")
    
    # Combine results
    ALL_PIDS="$CYBER_PIDS $DAEMON_PIDS"
    ALL_PIDS=$(echo "$ALL_PIDS" | tr ' ' '\n' | sort -u | tr '\n' ' ' | xargs)
    
    debug "Found PIDs by pattern: '$ALL_PIDS'"
    
    if [ -n "$ALL_PIDS" ]; then
        # Get the first PID (should be the main process)
        MAIN_PID=$(echo "$ALL_PIDS" | awk '{print $1}')
        debug "Using main PID: $MAIN_PID"
        
        # Update PID file only if MAIN_PID is not empty
        if [ -n "$MAIN_PID" ]; then
            echo "$MAIN_PID" > "$PID_FILE"
            debug "Updated PID file with $MAIN_PID"
            return 0 # Running
        else
            debug "Found empty MAIN_PID, not treating as running"
        fi
    fi
    
    debug "No running CyBer1t4L processes found"
    return 1 # Not running
}

# Start the bot using a separate script that will persist
write_daemon_script() {
    DAEMON_SCRIPT="$SCRIPT_DIR/local_run/daemon_runner.sh"
    debug "Creating daemon script at $DAEMON_SCRIPT"
    
    # Get the current Python interpreter path
    PYTHON_PATH=$(which python)
    debug "Using Python path: $PYTHON_PATH"
    
    # Create daemon runner script with improved error handling
    cat > "$DAEMON_SCRIPT" << EOF
#!/bin/bash
# CyBer1t4L QA Bot Daemon Runner
# This script is designed to run in the background and persist even when the terminal closes

# Set error handling
set -e

# Log file for the daemon itself
DAEMON_LOG="$LOG_DIR/daemon_runner_\$(date +%Y%m%d_%H%M%S).log"
echo "Starting daemon at \$(date)" > "\$DAEMON_LOG"

# Navigate to the project root
cd "$PROJECT_ROOT" || { echo "Failed to navigate to project root" >> "\$DAEMON_LOG"; exit 1; }

# Log the command
echo "Running command: $PYTHON_PATH -m src.omega_bot_farm.qa.run_cyber1t4l_locally $DEFAULT_OPTIONS" >> "\$DAEMON_LOG"

# Run with full path to Python to avoid any PATH issues
exec "$PYTHON_PATH" -m src.omega_bot_farm.qa.run_cyber1t4l_locally $DEFAULT_OPTIONS >> "\$DAEMON_LOG" 2>&1
EOF

    chmod +x "$DAEMON_SCRIPT"
    debug "Created daemon script with content:"
    if [ "$DEBUG" = true ]; then
        cat "$DAEMON_SCRIPT" >&2
    fi
    echo "$DAEMON_SCRIPT"
}

# Start the bot
start() {
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "${YELLOW}CyBer1t4L QA Bot is already running (PID: $PID)${NC}"
        return
    fi

    echo -e "${GREEN}Starting CyBer1t4L QA Bot service...${NC}"
    
    # Kill any running instances with the same name just to be safe
    debug "Stopping any existing processes"
    pkill -f "run_cyber1t4l_locally" > /dev/null 2>&1 || debug "No processes to kill"
    pkill -f "daemon_runner.sh" > /dev/null 2>&1 || debug "No daemon runners to kill"
    sleep 1
    
    # Navigate to the project root
    cd "$PROJECT_ROOT" || { echo -e "${RED}Error: Could not navigate to project root${NC}"; exit 1; }
    debug "Changed directory to $PROJECT_ROOT"
    
    # Log the start attempt
    echo "Starting CyBer1t4L QA Bot at $(date)" >> "$SERVICE_LOG"
    
    # Method 1: Create a daemon script that will survive terminal closures
    debug "Creating daemon script"
    DAEMON_SCRIPT=$(write_daemon_script)
    debug "Daemon script path: $DAEMON_SCRIPT"
    
    # Start the daemon directly - run with no hangup and completely detach
    debug "Running daemon script with setsid"
    setsid "$DAEMON_SCRIPT" > /dev/null 2>&1 &
    DAEMON_PID=$!
    debug "Initial setsid process PID: $DAEMON_PID"
    
    # Wait a moment for the process to start
    sleep 3
    
    # Try to find the actual Python process PID - the daemon runner will exec, so it's replaced
    debug "Looking for actual CyBer1t4L Python process"
    CYBER_PID=$(pgrep -f "run_cyber1t4l_locally")
    debug "Found CyBer1t4L process PIDs: $CYBER_PID"
    
    # If we found a running process, note its PID
    if [ -n "$CYBER_PID" ]; then
        echo "$CYBER_PID" > "$PID_FILE"
        echo -e "${GREEN}CyBer1t4L QA Bot service started with PID: $CYBER_PID${NC}"
        echo "Successfully started with PID: $CYBER_PID" >> "$SERVICE_LOG"
        
        # Get the most recent log file
        RECENT_LOG=$(ls -t "$LOG_DIR"/cyber1t4l_*.log 2>/dev/null | head -1)
        if [ -n "$RECENT_LOG" ]; then
            echo -e "${CYAN}Log file: $RECENT_LOG${NC}"
            debug "Most recent log file: $RECENT_LOG"
            
            # If in debug mode, show the beginning of the log
            if [ "$DEBUG" = true ]; then
                echo -e "${YELLOW}Log file contents:${NC}"
                head -20 "$RECENT_LOG" >&2
            fi
        fi
        
        # Verify the process is running after a few seconds
        sleep 2
        if is_running; then
            debug "Service is confirmed running"
            return 0
        else
            echo -e "${RED}Warning: Process started but not detected as running${NC}"
            debug "Process not detected by is_running function"
        fi
    else
        echo -e "${RED}Failed to start CyBer1t4L QA Bot service${NC}"
        echo "Failed to start process" >> "$SERVICE_LOG"
        debug "Process did not start. Checking daemon log"
        
        # Check daemon log for errors
        DAEMON_LOG=$(ls -t "$LOG_DIR"/daemon_runner_*.log 2>/dev/null | head -1)
        if [ -n "$DAEMON_LOG" ]; then
            debug "Daemon log content:"
            cat "$DAEMON_LOG" >&2
        fi
        
        return 1
    fi
}

# Stop the bot
stop() {
    if ! is_running; then
        echo -e "${YELLOW}CyBer1t4L QA Bot is not running${NC}"
        return
    fi
    
    PID=$(cat "$PID_FILE")
    echo -e "${GREEN}Stopping CyBer1t4L QA Bot service (PID: $PID)...${NC}"
    echo "Stopping CyBer1t4L QA Bot (PID: $PID) at $(date)" >> "$SERVICE_LOG"
    
    # Try graceful shutdown first
    kill -15 "$PID" 2>/dev/null
    
    # Wait for process to terminate
    TIMEOUT=10
    for ((i=0; i<TIMEOUT; i++)); do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    
    # If still running, force kill
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}Graceful shutdown timed out, forcing termination...${NC}"
        echo "Forcing termination of PID: $PID" >> "$SERVICE_LOG"
        kill -9 "$PID" 2>/dev/null
        sleep 1
    fi
    
    # Also look for any other instances
    CYBER_PIDS=$(pgrep -f "run_cyber1t4l_locally")
    if [ -n "$CYBER_PIDS" ]; then
        echo -e "${YELLOW}Found additional CyBer1t4L processes, killing them...${NC}"
        echo "Killing additional processes: $CYBER_PIDS" >> "$SERVICE_LOG"
        pkill -9 -f "run_cyber1t4l_locally" 2>/dev/null
    fi
    
    # Also try to kill any daemon scripts
    pkill -f "daemon_runner.sh" 2>/dev/null
    
    # Remove PID file
    rm -f "$PID_FILE"
    echo -e "${GREEN}CyBer1t4L QA Bot service stopped${NC}"
    echo "Service stopped successfully" >> "$SERVICE_LOG"
}

# Restart the bot
restart() {
    echo -e "${GREEN}Restarting CyBer1t4L QA Bot service...${NC}"
    echo "Restarting service at $(date)" >> "$SERVICE_LOG"
    stop
    sleep 2
    start
}

# Show bot status
status() {
    if is_running; then
        PID=$(cat "$PID_FILE")
        # For MacOS, the format is different from Linux
        if [ "$(uname)" == "Darwin" ]; then
            RUNNING_TIME=$(ps -o etime= -p "$PID")
        else
            RUNNING_TIME=$(ps -o etime= -p "$PID")
        fi
        echo -e "${GREEN}CyBer1t4L QA Bot is running${NC}"
        echo -e "${CYAN}PID: $PID${NC}"
        echo -e "${CYAN}Running time: $RUNNING_TIME${NC}"
        
        # Show process details
        echo -e "${CYAN}Process details:${NC}"
        ps -p "$PID" -o pid,ppid,command
        
        # Show most recent log file
        RECENT_LOG=$(ls -t "$LOG_DIR"/cyber1t4l_*.log 2>/dev/null | head -1)
        if [ -n "$RECENT_LOG" ]; then
            echo -e "${CYAN}Recent log file: $RECENT_LOG${NC}"
            echo -e "${CYAN}Last 5 log entries:${NC}"
            tail -5 "$RECENT_LOG"
        fi
        
        # Check Discord connection
        if grep -q "discord.*connected" "$RECENT_LOG" 2>/dev/null; then
            echo -e "${GREEN}Discord connection: Connected${NC}"
        else
            echo -e "${YELLOW}Discord connection: Status unknown${NC}"
        fi
    else
        echo -e "${YELLOW}CyBer1t4L QA Bot is not running${NC}"
        
        # Check if there are any processes that might be related
        CYBER_PROCESSES=$(ps aux | grep -i "cyber1t4l\|run_cyber1t4l_locally" | grep -v grep)
        if [ -n "$CYBER_PROCESSES" ]; then
            echo -e "${YELLOW}Found potential related processes:${NC}"
            echo "$CYBER_PROCESSES"
        fi
    fi
}

# Display usage information
usage() {
    echo "Usage: $0 {start|stop|restart|status|help|debug}"
    echo
    echo "Commands:"
    echo "  start    - Start the CyBer1t4L QA Bot as a service"
    echo "  stop     - Stop the running CyBer1t4L QA Bot service"
    echo "  restart  - Restart the CyBer1t4L QA Bot service"
    echo "  status   - Show the status of the CyBer1t4L QA Bot service"
    echo "  debug    - Enable debug mode for a specific command"
    echo "  help     - Display this help message"
    echo
    echo "Configuration:"
    echo "  Edit this script to change DEFAULT_MODE and DEFAULT_OPTIONS"
    echo "  Current settings: $DEFAULT_OPTIONS"
    echo
    echo "Files:"
    echo "  PID file: $PID_FILE"
    echo "  Log directory: $LOG_DIR"
    echo "  Service log: $SERVICE_LOG"
}

# Main command handler
show_banner

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    debug)
        DEBUG=true
        echo -e "${YELLOW}Enabling debug mode${NC}"
        shift
        if [ -z "$1" ]; then
            echo -e "${RED}Please specify a command to run in debug mode${NC}"
            usage
            exit 1
        fi
        case "$1" in
            start|stop|restart|status)
                "$1"
                ;;
            *)
                echo -e "${RED}Invalid command: $1${NC}"
                usage
                exit 1
                ;;
        esac
        ;;
    help|--help|-h)
        usage
        ;;
    *)
        usage
        exit 1
        ;;
esac

exit 0 