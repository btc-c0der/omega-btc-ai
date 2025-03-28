#!/bin/bash

# Script to set up local Redis instance for BTC Live Feed v3 failover
# This script installs and configures Redis locally for use as a failover instance

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up local Redis instance for BTC Live Feed v3 failover...${NC}"

# Check if Redis is installed
if ! command -v redis-server &> /dev/null; then
    echo -e "${YELLOW}Redis is not installed. Installing Redis...${NC}"
    
    # Detect OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        brew install redis
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        sudo apt-get update
        sudo apt-get install -y redis-server
    else
        echo -e "${RED}Unsupported operating system${NC}"
        exit 1
    fi
fi

# Create Redis configuration directory if it doesn't exist
REDIS_CONF_DIR="/etc/redis"
if [ ! -d "$REDIS_CONF_DIR" ]; then
    sudo mkdir -p "$REDIS_CONF_DIR"
fi

# Create Redis configuration file
cat << EOF | sudo tee "$REDIS_CONF_DIR/redis.conf"
port 6379
bind 127.0.0.1
requirepass omega_failover_redis
maxmemory 512mb
maxmemory-policy allkeys-lru
appendonly yes
appendfilename "appendonly.aof"
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
EOF

# Set proper permissions
sudo chown -R redis:redis "$REDIS_CONF_DIR"
sudo chmod 644 "$REDIS_CONF_DIR/redis.conf"

# Start Redis service
if [[ "$OSTYPE" == "darwin"* ]]; then
    brew services start redis
else
    sudo systemctl enable redis-server
    sudo systemctl start redis-server
fi

# Test Redis connection
echo -e "${YELLOW}Testing Redis connection...${NC}"
redis-cli -a omega_failover_redis ping

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Local Redis instance is ready for failover!${NC}"
    echo -e "${YELLOW}Configuration:${NC}"
    echo -e "Host: localhost"
    echo -e "Port: 6379"
    echo -e "Password: omega_failover_redis"
    echo -e "SSL: disabled"
    echo -e "TLS: disabled"
else
    echo -e "${RED}Failed to connect to Redis. Please check the configuration.${NC}"
    exit 1
fi 