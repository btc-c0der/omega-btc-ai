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


# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to check if .env.scaleway exists and has required values
check_env_file() {
    if [ ! -f .env.scaleway ]; then
        echo -e "${RED}Error: .env.scaleway file not found${NC}"
        echo -e "${YELLOW}Please create .env.scaleway with the following variables:${NC}"
        echo -e "SCALEWAY_HOST=your-server-hostname"
        echo -e "SCALEWAY_USER=your-username"
        echo -e "LOCAL_REDIS_PORT=16379"
        exit 1
    fi

    # Check if required variables are set
    if ! grep -q "^SCALEWAY_HOST=" .env.scaleway; then
        echo -e "${RED}Error: SCALEWAY_HOST not found in .env.scaleway${NC}"
        exit 1
    fi

    if ! grep -q "^SCALEWAY_USER=" .env.scaleway; then
        echo -e "${RED}Error: SCALEWAY_USER not found in .env.scaleway${NC}"
        exit 1
    fi
}

# Load environment variables from .env.scaleway
check_env_file
source .env.scaleway

# Configuration with environment variable fallbacks
REMOTE_HOST=${SCALEWAY_HOST:-""}
REMOTE_USER=${SCALEWAY_USER:-""}
REMOTE_REDIS_HOST=${REDIS_HOST:-"172.16.8.2"}
REMOTE_REDIS_PORT=${REDIS_PORT:-6379}
LOCAL_PORT=${LOCAL_REDIS_PORT:-16379}

# Function to check if tunnel is already running
check_tunnel() {
    if pgrep -f "ssh.*:$LOCAL_PORT:$REMOTE_REDIS_HOST:$REMOTE_REDIS_PORT" > /dev/null; then
        return 0  # Tunnel is running
    else
        return 1  # Tunnel is not running
    fi
}

# Function to create SSH tunnel
create_tunnel() {
    echo -e "${BLUE}Setting up SSH tunnel to Redis...${NC}"
    echo -e "Local port: ${GREEN}$LOCAL_PORT${NC}"
    echo -e "Remote Redis: ${GREEN}$REMOTE_REDIS_HOST:$REMOTE_REDIS_PORT${NC}"
    echo -e "Remote host: ${GREEN}$REMOTE_USER@$REMOTE_HOST${NC}"
    
    # Test SSH connection first
    if ! ssh -q "$REMOTE_USER@$REMOTE_HOST" exit; then
        echo -e "${RED}Failed to connect to remote host. Please check your SSH configuration.${NC}"
        exit 1
    fi
    
    # Create tunnel with compression and keep-alive
    ssh -N -C -o ServerAliveInterval=60 -L "$LOCAL_PORT:$REMOTE_REDIS_HOST:$REMOTE_REDIS_PORT" "$REMOTE_USER@$REMOTE_HOST" &
    
    # Wait for tunnel to establish
    sleep 2
    
    if check_tunnel; then
        echo -e "${GREEN}Tunnel established successfully!${NC}"
        echo -e "\nYou can now connect to Redis using:"
        echo -e "${YELLOW}redis-cli -h localhost -p $LOCAL_PORT${NC}"
        echo -e "\nTo test the connection, run:"
        echo -e "${YELLOW}./temp_deployment_package/test_redis_connection.sh --local --port $LOCAL_PORT${NC}"
    else
        echo -e "${RED}Failed to establish tunnel${NC}"
        exit 1
    fi
}

# Function to stop tunnel
stop_tunnel() {
    echo -e "${BLUE}Stopping Redis tunnel...${NC}"
    pkill -f "ssh.*:$LOCAL_PORT:$REMOTE_REDIS_HOST:$REMOTE_REDIS_PORT"
    sleep 1
    if ! check_tunnel; then
        echo -e "${GREEN}Tunnel stopped successfully${NC}"
    else
        echo -e "${RED}Failed to stop tunnel${NC}"
        exit 1
    fi
}

# Parse command line arguments
case "$1" in
    start)
        if check_tunnel; then
            echo -e "${YELLOW}Tunnel is already running${NC}"
            exit 0
        fi
        create_tunnel
        ;;
    stop)
        if ! check_tunnel; then
            echo -e "${YELLOW}No tunnel is running${NC}"
            exit 0
        fi
        stop_tunnel
        ;;
    status)
        if check_tunnel; then
            echo -e "${GREEN}Tunnel is running${NC}"
            echo -e "Local port: ${BLUE}$LOCAL_PORT${NC}"
            echo -e "Remote Redis: ${BLUE}$REMOTE_REDIS_HOST:$REMOTE_REDIS_PORT${NC}"
            echo -e "Remote host: ${BLUE}$REMOTE_USER@$REMOTE_HOST${NC}"
        else
            echo -e "${YELLOW}No tunnel is running${NC}"
        fi
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        echo "  start  - Start Redis tunnel"
        echo "  stop   - Stop Redis tunnel"
        echo "  status - Check tunnel status"
        exit 1
        ;;
esac

exit 0 