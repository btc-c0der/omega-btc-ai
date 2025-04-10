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

# OMEGA BTC AI - Service Startup Script
# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under MIT License
# SECURITY NOTICE: This script handles sensitive service initialization

set -e  # Exit on error

# Color constants for better visibility
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'  # No Color

echo -e "${BLUE}🔱 OMEGA BTC AI - Service Startup Script${NC}"
echo -e "${BLUE}======================================${NC}"

# Create necessary directories
echo -e "${YELLOW}Creating required directories...${NC}"
mkdir -p /app/logs /app/data /app/redis_data /app/postgres_data

# Function to check if Redis is ready
check_redis() {
    echo -e "${YELLOW}Checking Redis connection...${NC}"
    for i in {1..30}; do
        if redis-cli -h ${REDIS_HOST:-redis} -p ${REDIS_PORT:-6379} ping > /dev/null 2>&1; then
            echo -e "${GREEN}✓ Redis is ready${NC}"
            return 0
        fi
        echo -e "${YELLOW}Waiting for Redis... (${i}/30)${NC}"
        sleep 1
    done
    echo -e "${RED}❌ Redis connection failed${NC}"
    return 1
}

# Function to check if PostgreSQL is ready
check_postgres() {
    echo -e "${YELLOW}Checking PostgreSQL connection...${NC}"
    for i in {1..30}; do
        if pg_isready -h ${POSTGRES_HOST:-postgres} -p ${POSTGRES_PORT:-5432} > /dev/null 2>&1; then
            echo -e "${GREEN}✓ PostgreSQL is ready${NC}"
            return 0
        fi
        echo -e "${YELLOW}Waiting for PostgreSQL... (${i}/30)${NC}"
        sleep 1
    done
    echo -e "${RED}❌ PostgreSQL connection failed${NC}"
    return 1
}

# Check for required environment variables
echo -e "${YELLOW}Checking environment variables...${NC}"
required_vars=(
    "REDIS_HOST"
    "POSTGRES_HOST"
    "POSTGRES_DB"
    "POSTGRES_USER"
    "POSTGRES_PASSWORD"
)

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}❌ Required environment variable $var is not set${NC}"
        exit 1
    fi
done
echo -e "${GREEN}✓ Environment variables verified${NC}"

# Wait for services to be ready
check_redis || exit 1
check_postgres || exit 1

# Initialize log files
echo -e "${YELLOW}Initializing log files...${NC}"
touch /app/logs/omega_btc_ai.log
touch /app/logs/mm_trap_detector.log
touch /app/logs/btc_live_feed.log
echo -e "${GREEN}✓ Log files initialized${NC}"

# Set Python path
export PYTHONPATH=/app:$PYTHONPATH

# Start the main application with proper logging
echo -e "${GREEN}🚀 Starting OMEGA BTC AI...${NC}"
exec python /app/run_omega_btc_ai.py 2>&1 | tee -a /app/logs/omega_btc_ai.log 