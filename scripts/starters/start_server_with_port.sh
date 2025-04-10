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


# 🔱 Divine Server Starter with Port Detection 🔱
# This script starts a server with automatic port detection

# Default values
DEFAULT_START_PORT=8000
DEFAULT_MAX_ATTEMPTS=100
PYTHON_SCRIPT="find_available_port.py"

# Help message
show_help() {
    echo "Usage: $0 [options] -- <server_command>"
    echo
    echo "Options:"
    echo "  -p, --port         Starting port number (default: 8000)"
    echo "  -m, --max-attempts Maximum number of ports to try (default: 100)"
    echo "  -h, --help         Show this help message"
    echo
    echo "Example:"
    echo "  $0 -p 3000 -- npm start"
    echo "  $0 -p 8080 -- python server.py"
}

# Parse arguments
START_PORT=$DEFAULT_START_PORT
MAX_ATTEMPTS=$DEFAULT_MAX_ATTEMPTS

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--port)
            START_PORT="$2"
            shift 2
            ;;
        -m|--max-attempts)
            MAX_ATTEMPTS="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

if [ $# -eq 0 ]; then
    echo "Error: No server command provided"
    show_help
    exit 1
fi

# Find the directory containing this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Find an available port
echo "🔍 Finding available port starting from $START_PORT..."
PORT=$(python3 "$SCRIPT_DIR/$PYTHON_SCRIPT" --start-port "$START_PORT" --max-attempts "$MAX_ATTEMPTS")

if [ $? -ne 0 ]; then
    echo "❌ Failed to find available port"
    exit 1
fi

echo "✨ Found available port: $PORT"

# Export the port for the server to use
export PORT="$PORT"
export REACT_APP_PORT="$PORT"  # For React applications
export NODE_PORT="$PORT"       # For Node.js applications
export FLASK_RUN_PORT="$PORT"  # For Flask applications
export SERVER_PORT="$PORT"     # Generic server port

echo "🚀 Starting server on port $PORT..."
echo "📜 Command: $@"

# Execute the server command
"$@" 