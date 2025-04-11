#!/bin/bash

# ✨ IBR España Integration Runner
# ------------------------------
# This script runs the Divine Server v3 with the IBR España component integrated

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set the root directory of the project
ROOT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$ROOT_DIR"

echo "======================================================="
echo "      Divine Dashboard v3 with IBR España Integration"
echo "======================================================="
echo "Starting all components together..."

# Ensure the config directory exists
mkdir -p config

# Check if the IBR Spain config file exists, create default if not
if [ ! -f "config/ibr_spain.json" ]; then
    echo "Creating default IBR Spain configuration..."
    cat > "config/ibr_spain.json" << EOF
{
  "instagram_manager": {
    "data_dir": "${HOME}/ibr_data/instagram_manager",
    "account_name": "ibrespana",
    "logging_level": "INFO"
  }
}
EOF
    echo "Default configuration created at config/ibr_spain.json"
fi

# Ensure the data directory exists
DATA_DIR=$(grep -o '"data_dir": *"[^"]*"' "config/ibr_spain.json" | cut -d'"' -f4)
if [ -n "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo "Ensuring data directory exists at $DATA_DIR"
else
    mkdir -p "${HOME}/ibr_data/instagram_manager"
    echo "Created default data directory at ${HOME}/ibr_data/instagram_manager"
fi

# Check if virtual environment exists, activate or create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q uvicorn fastapi gradio huggingface_hub schedule requests pydantic tenacity python-dotenv python-json-logger beautifulsoup4

# Make sure the script is executable
chmod +x divine_server.py

# Display available dashboards
echo "======================================================="
echo "📊 Divine Dashboard v3 Ecosystem:"
echo "• Main Dashboard: http://localhost:8889"
echo "• Cybertruck QA Dashboard: http://localhost:7860"
echo "• Dashboard Metrics: http://localhost:7861"
echo "• NFT Dashboard: http://localhost:7862"
echo "• IBR España Dashboard: http://localhost:7863"
echo "• Divine Book Dashboard: http://localhost:7864"
echo "• Omega Orb Temple: http://localhost:7865"
echo "• Hacker Archive Dashboard: http://localhost:7866"
echo "• SHA256 Omega Dashboard: http://localhost:7867"
echo "• SHA356 Sacred Dashboard: http://localhost:7868"
echo "======================================================="

# Run the server
echo "Starting Divine Server with IBR España integration..."
python3 ./divine_server.py

echo "Server stopped" 