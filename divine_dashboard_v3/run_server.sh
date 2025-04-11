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

# Divine Dashboard v3 Server Runner

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "✨ Starting Divine Dashboard v3 Server ✨"
echo "---------------------------------------"

# Check if virtual environment exists, activate or create it
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Make sure dependencies are installed
pip install -q uvicorn fastapi gradio huggingface_hub schedule requests pydantic tenacity python-dotenv python-json-logger

# Make sure the script is executable
chmod +x divine_server.py

# Display available dashboards
echo "📊 Divine Dashboard v3 Ecosystem:"
echo "• Main Dashboard: http://localhost:8889"
echo "• Cybertruck QA Dashboard: http://localhost:7860"
echo "• Dashboard Metrics: http://localhost:7861"
echo "• NFT Dashboard: http://localhost:7862"
echo "• IBR España Dashboard: http://localhost:7863"
echo "---------------------------------------"

# Check for deploy flag
if [[ "$1" == "--local" ]]; then
    # Run the server locally without deploying
    python3 ./divine_server.py
else
    # Deploy to Hugging Face Spaces
    echo "🚀 Deploying to Hugging Face Spaces..."
    
    # Check if huggingface-cli is installed
    if ! command -v huggingface-cli &> /dev/null; then
        pip install -q huggingface_hub
    fi
    
    # Set Hugging Face Space name
    SPACE_NAME="divine-dashboard-v3"
    
    # Login to Hugging Face (will request token if not already logged in)
    huggingface-cli login
    
    # Run with deployment option
    export HF_DEPLOY=1
    python3 ./divine_server.py
fi

echo "Server stopped" 