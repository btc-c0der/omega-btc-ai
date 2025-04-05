#!/bin/bash

# Run Tech Debt V001D3R in Docker - CYBERITAL™ Edition
# -----------------------------------------------------------------

# Color output
GREEN='\033[0;32m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo -e "${BOLD}${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                                                            ║"
echo "║   🧩 T3CH D3BT V001D3R - DOCKER EDITION - 0m3g4_k1ng       ║"
echo "║                                                            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${SCRIPT_DIR}"

# Create directories if they don't exist
mkdir -p logs reports

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is required but not installed.${NC}"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is required but not installed.${NC}"
    exit 1
fi

# Check if .env file exists
if [ ! -f ../../../../.env ]; then
    echo -e "${YELLOW}Warning: No .env file found in project root. Creating a sample one...${NC}"
    
    # Create a sample .env file
    cat > ../../../../.env.v001d3r << EOF
# Tech Debt V001D3R - Discord Bot Settings
DISCORD_BOT_TOKEN=your_discord_bot_token
TECH_DEBT_APP_ID=your_discord_app_id
EOF
    
    echo -e "${YELLOW}Created sample .env.v001d3r file. Please edit it with your Discord bot credentials.${NC}"
fi

# Function to display help
function show_help {
    echo -e "${GREEN}Available commands:${NC}"
    echo -e "${BLUE}start${NC}       - Start the Docker container"
    echo -e "${BLUE}stop${NC}        - Stop the Docker container"
    echo -e "${BLUE}restart${NC}     - Restart the Docker container"
    echo -e "${BLUE}logs${NC}        - View container logs"
    echo -e "${BLUE}build${NC}       - Build the Docker image"
    echo -e "${BLUE}rebuild${NC}     - Rebuild the Docker image from scratch"
    echo -e "${BLUE}shell${NC}       - Get a shell in the container"
    echo -e "${BLUE}help${NC}        - Display this help message"
}

# Process command line arguments
if [ $# -eq 0 ]; then
    show_help
    exit 0
fi

case "$1" in
    start)
        echo -e "${GREEN}Starting T3CH D3BT V001D3R in Docker...${NC}"
        docker-compose up -d
        ;;
    stop)
        echo -e "${YELLOW}Stopping T3CH D3BT V001D3R...${NC}"
        docker-compose down
        ;;
    restart)
        echo -e "${YELLOW}Restarting T3CH D3BT V001D3R...${NC}"
        docker-compose restart
        ;;
    logs)
        echo -e "${BLUE}Viewing T3CH D3BT V001D3R logs...${NC}"
        docker-compose logs -f
        ;;
    build)
        echo -e "${GREEN}Building T3CH D3BT V001D3R Docker image...${NC}"
        docker-compose build
        ;;
    rebuild)
        echo -e "${GREEN}Rebuilding T3CH D3BT V001D3R Docker image from scratch...${NC}"
        docker-compose build --no-cache
        ;;
    shell)
        echo -e "${GREEN}Opening shell in T3CH D3BT V001D3R container...${NC}"
        docker-compose exec tech-debt-v001d3r /bin/bash
        ;;
    help)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac

echo -e "${GREEN}✅ Command completed successfully${NC}" 