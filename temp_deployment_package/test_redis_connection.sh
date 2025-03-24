#!/bin/bash

# OMEGA BTC AI - Redis Connection Test Script
# This script tests the connection to your Cloud Redis instance

set -e  # Exit on error

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "=================================================="
echo "  OMEGA BTC AI - REDIS CONNECTION TEST"
echo "=================================================="
echo -e "${NC}"

# Check if redis-cli is installed
if ! command -v redis-cli &> /dev/null; then
    echo -e "${YELLOW}Redis client not found. Installing...${NC}"
    apt-get update
    apt-get install -y redis-tools
fi

# Load environment variables from .env.scaleway if it exists
if [ -f .env.scaleway ]; then
    echo -e "${YELLOW}Loading Redis configuration from .env.scaleway...${NC}"
    source .env.scaleway
else
    echo -e "${YELLOW}Using default Redis configuration...${NC}"
    # Default values if .env.scaleway doesn't exist
    REDIS_HOST=172.16.8.2
    REDIS_PORT=6379
    REDIS_PASSWORD=""
fi

echo -e "${YELLOW}Testing Redis connection...${NC}"
echo -e "Host: ${REDIS_HOST}"
echo -e "Port: ${REDIS_PORT}"

# Test connection without password first
if [ -z "$REDIS_PASSWORD" ]; then
    echo -e "${YELLOW}Trying to connect without password...${NC}"
    if redis-cli -h $REDIS_HOST -p $REDIS_PORT ping > /dev/null; then
        echo -e "${GREEN}Connection successful!${NC}"
    else
        echo -e "${RED}Connection failed without password.${NC}"
        echo -e "${YELLOW}Password might be required...${NC}"
    fi
else
    echo -e "${YELLOW}Trying to connect with password...${NC}"
    if redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD ping > /dev/null; then
        echo -e "${GREEN}Connection successful!${NC}"
    else
        echo -e "${RED}Connection failed with provided password.${NC}"
        echo -e "Please check your Redis host, port, and password settings."
    fi
fi

# Check for existing trap probability data
echo -e "${YELLOW}Checking for trap probability data...${NC}"
if [ -z "$REDIS_PASSWORD" ]; then
    TRAP_KEY_COUNT=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT keys "trap_probability_*" | wc -l)
else
    TRAP_KEY_COUNT=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD keys "trap_probability_*" | wc -l)
fi

if [ "$TRAP_KEY_COUNT" -gt 0 ]; then
    echo -e "${GREEN}Found $TRAP_KEY_COUNT trap probability keys in Redis.${NC}"
else
    echo -e "${YELLOW}No trap probability data found in Redis yet.${NC}"
fi

# Check for trader position data
echo -e "${YELLOW}Checking for trader position data...${NC}"
if [ -z "$REDIS_PASSWORD" ]; then
    TRADER_KEY_COUNT=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT keys "trader:*" | wc -l)
else
    TRADER_KEY_COUNT=$(redis-cli -h $REDIS_HOST -p $REDIS_PORT -a $REDIS_PASSWORD keys "trader:*" | wc -l)
fi

if [ "$TRADER_KEY_COUNT" -gt 0 ]; then
    echo -e "${GREEN}Found $TRADER_KEY_COUNT trader keys in Redis.${NC}"
else
    echo -e "${YELLOW}No trader data found in Redis yet.${NC}"
fi

echo -e "${GREEN}"
echo "=================================================="
echo "  CONNECTION TEST COMPLETE!"
echo "=================================================="
echo -e "${NC}"

# Provide some recommendations based on results
if [ "$TRAP_KEY_COUNT" -eq 0 ] && [ "$TRADER_KEY_COUNT" -eq 0 ]; then
    echo -e "${YELLOW}Recommendations:${NC}"
    echo "1. If this is a fresh setup, no data is expected."
    echo "2. If you're migrating from another system, you may need to run data import scripts."
    echo "3. Once your containers are running, data will start populating automatically."
fi 