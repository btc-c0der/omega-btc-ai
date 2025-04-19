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

# OMEGA BTC AI - Redis Setup & Optimization
# Copyright (c) 2024 OMEGA BTC AI Team
# Licensed under MIT License

set -e

# Color constants
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}🔱 OMEGA BTC AI - Redis Setup${NC}"
echo -e "${GREEN}============================${NC}"

# Check Redis connection
echo -e "${YELLOW}Checking Redis connection...${NC}"
if redis-cli ping > /dev/null; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${RED}❌ Redis is not running${NC}"
    exit 1
fi

# Configure Redis for optimal performance
echo -e "${YELLOW}Optimizing Redis configuration...${NC}"

redis-cli config set maxmemory 256mb
redis-cli config set maxmemory-policy allkeys-lru
redis-cli config set save "60 1"
redis-cli config set appendonly yes
redis-cli config set appendfsync everysec

# Initialize key data structures
echo -e "${YELLOW}Initializing data structures...${NC}"

# Create sorted sets for price data
redis-cli del btc_price_data
redis-cli del btc_volume_data
redis-cli del btc_movement_history

# Create lists for trap detection
redis-cli del trap_detections
redis-cli del subtle_movements

echo -e "${GREEN}✓ Redis setup complete${NC}"

# Verify configuration
echo -e "${YELLOW}Verifying configuration...${NC}"
redis-cli info | grep maxmemory
redis-cli info | grep maxmemory_policy
redis-cli info | grep appendonly

echo -e "${GREEN}🚀 Redis is ready for OMEGA BTC AI${NC}" 