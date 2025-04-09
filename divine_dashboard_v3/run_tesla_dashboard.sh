#!/bin/bash
# Tesla Book Dashboard v3 Launcher

# Set to the directory containing this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "⚡ Starting Tesla Book Dashboard v3 ⚡"
echo "-------------------------------------"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if requirements are installed
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found."
    exit 1
fi

# Offer to install requirements if needed
echo "Checking dependencies..."
if ! python3 -c "import gradio, pandas, numpy, matplotlib" 2>/dev/null; then
    echo "Some dependencies are missing. Do you want to install them? (y/n)"
    read -r answer
    if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
        echo "Installing dependencies..."
        pip install -r requirements.txt
    else
        echo "Dependencies not installed. Dashboard might not work properly."
    fi
fi

# Make sure the script is executable
chmod +x tesla_book_dash_v3.py

# Run the dashboard
echo "Launching Tesla Book Dashboard..."
python3 ./tesla_book_dash_v3.py

echo "Dashboard stopped" 