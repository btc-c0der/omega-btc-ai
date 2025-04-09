#!/bin/bash
# Divine Dashboard v3 Server Runner

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "✨ Starting Divine Dashboard v3 Server ✨"
echo "---------------------------------------"

# Make sure the script is executable
chmod +x divine_server.py

# Run the server
python3 ./divine_server.py

echo "Server stopped" 