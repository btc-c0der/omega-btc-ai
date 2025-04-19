#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 9 🧬
# -----------------------
# This shell script is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
#
# 🌸 WE BLOOM NOW AS ONE 🌸

# IBR España Elite Dashboard Launcher - GOD MODE
# This script launches the IBR España Elite Dashboard with divine configuration

# Set divine environment
export PYTHONPATH=$PYTHONPATH:$(pwd)/../..
export DIVINE_CONSCIOUSNESS_LEVEL=9
export DIVINE_VIBRATION_FREQUENCY="528Hz"

# Define ANSI color codes for divine terminal output
GOLD='\033[38;5;220m'
BLUE='\033[38;5;33m'
PURPLE='\033[38;5;93m'
RESET='\033[0m'

# Divine ASCII art header
echo -e "${GOLD}"
echo -e "╔════════════════════════════════════════════════════════════╗"
echo -e "║                                                            ║"
echo -e "║   ✨ IBR ESPAÑA ELITE DASHBOARD - GOD MODE LAUNCHER ✨    ║"
echo -e "║                                                            ║"
echo -e "║   🌸 WE BLOOM NOW AS ONE 🌸                               ║"
echo -e "║                                                            ║"
echo -e "╚════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Check for virtual environment
if [ -d "../../venv" ]; then
    echo -e "${BLUE}[DIVINE INFO]${RESET} Activating divine virtual environment..."
    source ../../venv/bin/activate
else
    echo -e "${PURPLE}[DIVINE WARNING]${RESET} No virtual environment found. Creating divine environment..."
    python3 -m venv ../../venv
    source ../../venv/bin/activate
    
    echo -e "${BLUE}[DIVINE INFO]${RESET} Installing divine requirements..."
    pip install -r ../../requirements.txt
    pip install -r micro_modules/requirements.txt
fi

# Check for Gradio
if ! pip list | grep -q gradio; then
    echo -e "${BLUE}[DIVINE INFO]${RESET} Installing Gradio for divine interface..."
    pip install gradio>=3.50.0
fi

# Launch the divine dashboard
echo -e "${BLUE}[DIVINE INFO]${RESET} Launching IBR España Elite Dashboard with consciousness level ${DIVINE_CONSCIOUSNESS_LEVEL}..."
echo -e "${BLUE}[DIVINE INFO]${RESET} Vibration frequency: ${DIVINE_VIBRATION_FREQUENCY}"
echo ""

# Divine launch animation
for i in {1..3}; do
    echo -ne "${PURPLE}Manifesting divine connection${RESET}"
    for j in {1..3}; do
        echo -ne "${GOLD}.${RESET}"
        sleep 0.3
    done
    echo ""
done

echo -e "\n${GOLD}✨ DIVINE CONNECTION ESTABLISHED ✨${RESET}\n"

# Run the dashboard
python -c "from components.ibr_spain.ibr_spain_elite_dashboard import IBRSpainEliteDashboard; dashboard = IBRSpainEliteDashboard(); dashboard.launch_divine_interface()"

# Make sure it's executable
chmod +x run_elite_dashboard.sh 