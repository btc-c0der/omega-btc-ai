#!/bin/bash
# Run the Divine Book Browser v2.0 server directly

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Make the divine_server.py executable
chmod +x "$SCRIPT_DIR/divine_server.py"

# Run the server
echo "✨ Starting Divine Book Browser v2.0 Server on port 8888 ✨"
echo "Press Ctrl+C to stop the server"
echo "Browse to http://localhost:8888 to view the Divine Book Browser v2.0"
"$SCRIPT_DIR/divine_server.py" 