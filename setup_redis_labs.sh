#!/bin/bash

# OMEGA BTC AI - Redis Labs Setup Script
# This script helps set up Redis Labs connection

set -e  # Exit on error

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if redis-cli is installed
check_redis_cli() {
    if ! command -v redis-cli &> /dev/null; then
        echo -e "${YELLOW}Redis CLI not found. Installing with Homebrew...${NC}"
        if ! command -v brew &> /dev/null; then
            echo -e "${RED}Homebrew is not installed. Please install Homebrew first.${NC}"
            exit 1
        fi
        brew install redis
        echo -e "${GREEN}Redis CLI installed successfully${NC}"
    fi
}

# Function to create .env file
create_env_file() {
    echo -e "${BLUE}Creating .env file for Redis Labs connection...${NC}"
    
    # Prompt for Redis Labs credentials
    echo -e "${YELLOW}Please enter your Redis Labs credentials:${NC}"
    read -p "Redis Host: " REDIS_HOST
    read -p "Redis Port: " REDIS_PORT
    read -p "Redis Password: " REDIS_PASSWORD
    read -p "Redis Username (default: default): " REDIS_USERNAME
    REDIS_USERNAME=${REDIS_USERNAME:-default}
    
    # Create .env file
    cat > .env << EOL
REDIS_HOST=${REDIS_HOST}
REDIS_PORT=${REDIS_PORT}
REDIS_PASSWORD=${REDIS_PASSWORD}
REDIS_USERNAME=${REDIS_USERNAME}
REDIS_SSL=yes
EOL
    
    echo -e "${GREEN}.env file created successfully${NC}"
}

# Function to test Redis connection
test_connection() {
    echo -e "${BLUE}Testing Redis connection...${NC}"
    
    # Source the .env file
    source .env
    
    # Test connection with redis-cli
    if redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD --tls ping; then
        echo -e "${GREEN}Redis connection successful!${NC}"
        echo -e "\nYou can now connect to Redis using:"
        echo -e "${YELLOW}redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD --tls${NC}"
        echo -e "\nTo test the connection, run:"
        echo -e "${YELLOW}./test_redis_connection.sh --scale${NC}"
    else
        echo -e "${RED}Redis connection failed. Please check your credentials.${NC}"
        exit 1
    fi
}

# Main script
echo -e "${BLUE}Setting up Redis Labs connection...${NC}"

# Check for redis-cli
check_redis_cli

# Create .env file
create_env_file

# Test connection
test_connection

echo -e "${GREEN}Setup complete!${NC}" 