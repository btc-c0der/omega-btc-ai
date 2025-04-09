#!/bin/bash

# OMEGA BTC AI React Dashboard launcher script

# Colors for pretty output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== OMEGA BTC AI React Dashboard Launcher ===${NC}"
echo

# Check for dependencies
echo -e "${YELLOW}Checking for http-server...${NC}"
if ! command -v http-server &> /dev/null; then
    echo -e "${YELLOW}http-server not found, installing...${NC}"
    npm install -g http-server
fi

# Choose startup method
echo -e "${GREEN}Choose how to start the dashboard:${NC}"
echo "1) Simple mode (http-server, more reliable)"
echo "2) Development mode (Vite, with hot reloading)"
echo "3) Full reset and reinstall (if having issues)"
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo -e "${YELLOW}Starting in simple mode...${NC}"
        http-server -p 3000 .
        ;;
    2)
        echo -e "${YELLOW}Starting in development mode...${NC}"
        npm run dev
        ;;
    3)
        echo -e "${YELLOW}Performing full reset and reinstall...${NC}"
        rm -rf node_modules package-lock.json
        npm cache clean --force
        echo -e "${YELLOW}Installing dependencies with legacy-peer-deps...${NC}"
        npm install --legacy-peer-deps
        echo -e "${YELLOW}Starting in development mode...${NC}"
        npm run dev
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac 