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
#!/bin/bash
# Run Live Discord Bot Tests
# This script checks if the bot is running and executes the live Discord integration tests

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../../" && pwd)"

# ANSI color codes
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# ASCII art header
echo -e "${CYAN}"
echo "  ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗████████╗██╗  ██╗██╗     "
echo " ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║╚══██╔══╝██║  ██║██║     "
echo " ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝██║   ██║   ███████║██║     "
echo " ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██║   ██║   ██╔══██║██║     "
echo " ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║   ██║   ██║  ██║███████╗"
echo "  ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝"
echo -e "${YELLOW}                                                                       "
echo " ░█▀█░█▀█░░░█▀▄░█▀█░▀█▀░░░█░█░█▀█░█▀▄░█▀▄░▀█▀░█▀█░█▀▄                  "
echo " ░█▀▀░█▀█░░░█▀▄░█░█░░█░░░░█▀█░█▀█░█▀▄░█▀▄░░█░░█░█░█▀▄                  "
echo " ░▀░░░▀░▀░░░▀▀░░▀▀▀░░▀░░░░▀░▀░▀░▀░▀░▀░▀░▀░▀▀▀░▀░▀░▀░▀                  "
echo -e "${NC}"
echo -e "${MAGENTA}🔴 🟡 🟢 RASTA HEART ON F1R3 🔴 🟡 🟢${NC}"
echo -e "${GREEN}LIVE DISCORD INTEGRATION TESTS${NC}"
echo -e "${BLUE}-----------------------------------${NC}"

# Check if the bot is running
echo -e "${YELLOW}Checking if CyBer1t4L QA Bot is running...${NC}"
BOT_PID=$(pgrep -f "cyber1t4l_qa_bot|run_cyber1t4l")

if [ -z "$BOT_PID" ]; then
    echo -e "${RED}❌ CyBer1t4L QA Bot is not running.${NC}"
    echo -e "${YELLOW}Starting the bot using daemon_runner.sh...${NC}"
    
    # Check if daemon_runner.sh exists
    DAEMON_SCRIPT="$PROJECT_ROOT/src/omega_bot_farm/qa/daemon_runner.sh"
    if [ -f "$DAEMON_SCRIPT" ]; then
        # Make it executable if it's not already
        chmod +x "$DAEMON_SCRIPT"
        
        # Run the daemon script
        "$DAEMON_SCRIPT"
        
        # Wait for the bot to start
        echo -e "${YELLOW}Waiting for bot to start...${NC}"
        sleep 10
        
        # Check again if the bot is running
        BOT_PID=$(pgrep -f "cyber1t4l_qa_bot|run_cyber1t4l")
        
        if [ -z "$BOT_PID" ]; then
            echo -e "${RED}❌ Failed to start the bot. Please start it manually:${NC}"
            echo -e "${CYAN}   ./src/omega_bot_farm/qa/daemon_runner.sh${NC}"
            exit 1
        else
            echo -e "${GREEN}✅ Bot successfully started with PID: $BOT_PID${NC}"
        fi
    else
        echo -e "${RED}❌ Daemon runner script not found at: $DAEMON_SCRIPT${NC}"
        echo -e "${YELLOW}Please start the bot manually before running this script.${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✅ CyBer1t4L QA Bot is running with PID: $BOT_PID${NC}"
fi

# Install dependencies if not already installed
echo -e "${YELLOW}Checking for required dependencies...${NC}"
if ! python -c "import httpx" 2>/dev/null; then
    echo -e "${YELLOW}Installing required dependencies...${NC}"
    "$SCRIPT_DIR/install_test_deps.sh" > /dev/null
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to install dependencies${NC}"
        exit 1
    fi
fi

# Run the live tests
echo -e "${GREEN}Running live Discord integration tests...${NC}"
echo -e "${BLUE}-----------------------------------${NC}"

# Create the reports directory if it doesn't exist
mkdir -p "$SCRIPT_DIR/reports"

# Run the tests with the live flag
cd "$PROJECT_ROOT"
python -m src.omega_bot_farm.qa.tests.run_discord_tests --live --html

# Check the test result
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ All live tests passed!${NC}"
    
    # Show report location
    HTML_PATH="$SCRIPT_DIR/reports/html/index.html"
    if [ -f "$HTML_PATH" ]; then
        echo -e "${BLUE}HTML Report: $HTML_PATH${NC}"
    fi
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo -e "${YELLOW}Check the output above for details${NC}"
fi

echo -e "${BLUE}-----------------------------------${NC}"
echo -e "${MAGENTA}🔴 🟡 🟢 TESTING COMPLETE 🔴 🟡 🟢${NC}" 