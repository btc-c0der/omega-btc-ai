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

# Installation script for Divine Book Browser Server v2.0

# Determine the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
FULL_PATH=$(realpath "$SCRIPT_DIR")
PLIST_PATH="$HOME/Library/LaunchAgents/com.omega.divinebrowser.v2.plist"

echo "✨ Installing Divine Book Browser v2.0 Service ✨"
echo "Service will run on port 8888 (or next available port)"

# Make the scripts executable
chmod +x "$SCRIPT_DIR/divine_server.py"
chmod +x "$SCRIPT_DIR/install_service.sh"
chmod +x "$SCRIPT_DIR/run_server.sh"

# Check if the service is already installed
if [ -f "$PLIST_PATH" ]; then
    echo "Service is already installed at: $PLIST_PATH"
    
    read -p "Do you want to reinstall the service? (y/n) " choice
    case "$choice" in 
        y|Y )
            echo "Unloading existing service..."
            launchctl unload "$PLIST_PATH" 2>/dev/null || true
            echo "Removing existing service file..."
            rm "$PLIST_PATH"
            ;;
        * )
            echo "Installation aborted. You can still run the server manually using ./run_server.sh"
            exit 0
            ;;
    esac
fi

# Create a temporary file with the correct paths
TMP_PLIST=$(mktemp)
cat "$SCRIPT_DIR/com.omega.divinebrowser.plist" | sed "s|REPLACE_WITH_FULL_PATH|$FULL_PATH|g" > "$TMP_PLIST"

# Ensure LaunchAgents directory exists
mkdir -p "$HOME/Library/LaunchAgents"

# Copy the plist to LaunchAgents
cp "$TMP_PLIST" "$PLIST_PATH"
rm "$TMP_PLIST"

echo "Service file installed at: $PLIST_PATH"

# Load the service
echo "Loading service..."
launchctl load -w "$PLIST_PATH"

echo "Service installed and started!"
echo "Divine Book Browser v2.0 is now available at: http://localhost:8888"
echo "The root URL (/) automatically redirects to index.html"
echo 
echo "Management commands:"
echo "  - Stop service:    launchctl unload $PLIST_PATH"
echo "  - Start service:   launchctl load -w $PLIST_PATH"
echo "  - Check status:    launchctl list | grep com.omega.divinebrowser.v2"
echo "  - View logs:       $SCRIPT_DIR/divine_server.log"
echo "  - Run manually:    $SCRIPT_DIR/run_server.sh"
echo
echo "You can access the Divine Book Browser v2.0 at: http://localhost:8888 (or next available port)" 