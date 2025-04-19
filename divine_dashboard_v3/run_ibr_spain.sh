#!/bin/bash

# ✨ IBR España Dashboard Runner
# ------------------------------
# This script runs the IBR España component for Divine Dashboard v3

# Exit on error with debugging
set -e
set -o pipefail

# Set environment variables
export IBR_ENV="production"
export IBR_LOG_LEVEL="INFO"
export PYTHONPATH="$PYTHONPATH:$(pwd)"

# Define paths
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
DASHBOARD_DIR="${SCRIPT_DIR}"
IBR_COMPONENT_DIR="${DASHBOARD_DIR}/components/ibr_spain"
CONFIG_DIR="${DASHBOARD_DIR}/config"
LOG_FILE="${DASHBOARD_DIR}/ibr_spain_dashboard.log"

# Display banner
echo "======================================================="
echo "      IBR España Instagram Manager Dashboard"
echo "======================================================="
echo "Starting dashboard component..."
echo "Working directory: $(pwd)"
echo "Script directory: ${SCRIPT_DIR}"
echo "IBR Component directory: ${IBR_COMPONENT_DIR}"

# Check if IBR component directory exists
if [ ! -d "${IBR_COMPONENT_DIR}" ]; then
    echo "ERROR: IBR España component directory not found at ${IBR_COMPONENT_DIR}"
    echo "Please make sure the component is installed correctly."
    exit 1
fi

# Create config directory if it doesn't exist
mkdir -p "${CONFIG_DIR}"
echo "Created/verified config directory at ${CONFIG_DIR}"

# Check if config file exists, create default if not
if [ ! -f "${CONFIG_DIR}/ibr_spain.json" ]; then
    echo "Creating default configuration..."
    cat > "${CONFIG_DIR}/ibr_spain.json" << EOF
{
  "instagram_manager": {
    "data_dir": "${HOME}/ibr_data/instagram_manager",
    "account_name": "ibrespana",
    "logging_level": "INFO"
  }
}
EOF
    echo "Default configuration created at ${CONFIG_DIR}/ibr_spain.json"
fi

# Read configuration
if [ -f "${CONFIG_DIR}/ibr_spain.json" ]; then
    echo "Configuration found at ${CONFIG_DIR}/ibr_spain.json"
else
    echo "ERROR: Configuration file not found at ${CONFIG_DIR}/ibr_spain.json"
    exit 1
fi

# Ensure data directory exists
DATA_DIR=$(grep -o '"data_dir": *"[^"]*"' "${CONFIG_DIR}/ibr_spain.json" | cut -d'"' -f4)
if [ -n "$DATA_DIR" ]; then
    mkdir -p "$DATA_DIR"
    echo "Ensuring data directory exists at $DATA_DIR"
else
    echo "WARNING: No data_dir found in configuration. Using default."
    mkdir -p "${HOME}/ibr_data/instagram_manager"
    DATA_DIR="${HOME}/ibr_data/instagram_manager"
fi

# Check if virtual environment exists
if [ ! -d "${DASHBOARD_DIR}/venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "${DASHBOARD_DIR}/venv"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "${DASHBOARD_DIR}/venv/bin/activate"

# Verify Python version
PYTHON_VERSION=$(python --version)
echo "Using Python: $PYTHON_VERSION"

# Check if gradio is installed
if ! pip list | grep -q "gradio"; then
    echo "Installing gradio..."
    pip install gradio
fi

# Install requirements
echo "Installing dependencies..."
if [ -f "${DASHBOARD_DIR}/requirements.txt" ]; then
    pip install -r "${DASHBOARD_DIR}/requirements.txt"
else
    echo "WARNING: requirements.txt not found at ${DASHBOARD_DIR}/requirements.txt"
fi

if [ -f "${IBR_COMPONENT_DIR}/micro_modules/requirements.txt" ]; then
    pip install -r "${IBR_COMPONENT_DIR}/micro_modules/requirements.txt"
else
    echo "WARNING: requirements.txt not found at ${IBR_COMPONENT_DIR}/micro_modules/requirements.txt"
    echo "Installing default required packages..."
    pip install requests pydantic tenacity python-dotenv python-json-logger gradio
fi

# Check if the component directory structure is correct
if [ ! -f "${IBR_COMPONENT_DIR}/ibr_dashboard.py" ]; then
    echo "ERROR: ibr_dashboard.py not found at ${IBR_COMPONENT_DIR}/ibr_dashboard.py"
    echo "Please make sure the component is installed correctly."
    exit 1
fi

# Initialize Instagram Manager if needed
echo "Initializing Instagram Manager..."
python -c "
try:
    import sys
    sys.path.append('${DASHBOARD_DIR}')
    from components.ibr_spain.micro_modules.instagram_manager import InstagramManager
    manager = InstagramManager()
    print('Instagram Manager initialized successfully')
except Exception as e:
    print(f'ERROR initializing Instagram Manager: {e}')
    sys.exit(1)
"

# Check if the initialization was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to initialize Instagram Manager."
    echo "Please check the component installation and try again."
    exit 1
fi

# Run IBR Spain Dashboard
echo "Starting IBR España Dashboard..."
cd "${DASHBOARD_DIR}"

# Start the server directly in foreground mode for easier debugging
python -c "
try:
    import sys
    sys.path.append('${DASHBOARD_DIR}')
    import gradio as gr
    from components.ibr_spain.ibr_dashboard import create_ibr_interface
    
    # Create the interface
    interface = create_ibr_interface()
    
    # Launch the interface
    interface.launch(
        server_name='0.0.0.0',
        server_port=7860,
        share=False,
        debug=True,
        quiet=False
    )
except Exception as e:
    print(f'ERROR starting IBR España Dashboard: {e}')
    sys.exit(1)
" 2>&1 | tee -a "${LOG_FILE}"

# The script will continue running until the user terminates it 