#!/bin/bash

# OMEGA BTC AI - Divine Test Runner 🧪🌟
# ------------------------------------------
# "Run thy tests and visualize the quality of thy codebase."
# - Rastafarian Software Engineering Wisdom

set -e  # Exit on any error

# Terminal colors for divine output
RED="\033[91m"
GREEN="\033[92m"
YELLOW="\033[93m"
CYAN="\033[96m"
RESET="\033[0m"

# Create a timestamp for this test run
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
echo -e "\n${CYAN}🌈 OMEGA BTC AI - Divine Test Runner 🌈${RESET}"
echo -e "${YELLOW}Test run started at: $(date)${RESET}\n"

# Ensure we have the required dependencies
echo -e "${CYAN}📦 Installing test dependencies...${RESET}"
pip install -q -r test-requirements.txt

# Create output directories
mkdir -p qa_reports
mkdir -p qa_reports/history

# Create a new branch for QA if specified
if [ "$1" == "--branch" ] || [ "$1" == "-b" ]; then
    BRANCH_NAME="qa/test-coverage-$TIMESTAMP"
    echo -e "${CYAN}🌿 Creating new branch: ${GREEN}$BRANCH_NAME${RESET}"
    git checkout -b "$BRANCH_NAME"
fi

# Run the QA visualization tool
echo -e "\n${CYAN}🧪 Running tests with divine QA visualization...${RESET}"
python -m omega_ai.tools.qa_status

# Save a copy of the QA report with timestamp
if [ -f "qa_reports/qa_visualization.png" ]; then
    cp "qa_reports/qa_visualization.png" "qa_reports/history/qa_visualization_$TIMESTAMP.png"
    echo -e "${GREEN}✅ QA report saved to history: qa_reports/history/qa_visualization_$TIMESTAMP.png${RESET}"
fi

# Display the final QA report if available
if [ -f "qa_reports/qa_visualization.png" ]; then
    echo -e "${GREEN}✅ Opening QA visualization...${RESET}"
    
    # Try different commands based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then  # macOS
        open "qa_reports/qa_visualization.png"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then  # Linux
        if command -v xdg-open &> /dev/null; then
            xdg-open "qa_reports/qa_visualization.png"
        elif command -v display &> /dev/null; then
            display "qa_reports/qa_visualization.png"
        else
            echo -e "${YELLOW}⚠️ Could not open image automatically. Please view it at: qa_reports/qa_visualization.png${RESET}"
        fi
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then  # Windows
        start "qa_reports/qa_visualization.png"
    else
        echo -e "${YELLOW}⚠️ Could not open image automatically. Please view it at: qa_reports/qa_visualization.png${RESET}"
    fi
else
    echo -e "${RED}❌ QA visualization was not generated. Check for errors above.${RESET}"
fi

echo -e "\n${GREEN}🎉 Divine test run completed at: $(date)${RESET}"
echo -e "${YELLOW}JAH BLESS THE TEST COVERAGE! 🙏🌟${RESET}\n" 