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


# 🔱 OMEGA BTC AI - DIVINE REDIS MANAGEMENT SCRIPT 🔱

# Divine Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Divine Functions
print_banner() {
    echo -e "${GREEN}"
    echo "🔱 OMEGA BTC AI - DIVINE REDIS MANAGEMENT 🔱"
    echo "JAH JAH BLESS THE MEMORY NODE! 💚💛❤️"
    echo -e "${NC}"
}

check_redis_health() {
    echo -e "${YELLOW}Checking Redis health...${NC}"
    docker exec divine-redis redis-cli ping
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Redis is healthy!${NC}"
    else
        echo -e "${RED}❌ Redis is not responding!${NC}"
    fi
}

monitor_redis() {
    echo -e "${YELLOW}Starting divine Redis monitor...${NC}"
    echo -e "${GREEN}Press Ctrl+C to exit${NC}"
    docker exec divine-redis redis-cli monitor | grep -i "set\|del\|expire"
}

show_memory_info() {
    echo -e "${YELLOW}Divine Memory Status:${NC}"
    docker exec divine-redis redis-cli info memory | grep -E "used_memory|used_memory_peak|maxmemory|maxmemory_policy"
}

backup_redis() {
    echo -e "${YELLOW}Creating divine backup...${NC}"
    BACKUP_DIR="backups/redis"
    mkdir -p $BACKUP_DIR
    BACKUP_FILE="$BACKUP_DIR/redis_backup_$(date +%Y%m%d_%H%M%S).rdb"
    
    docker exec divine-redis redis-cli save
    docker cp divine-redis:/data/dump.rdb $BACKUP_FILE
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Backup created: $BACKUP_FILE${NC}"
    else
        echo -e "${RED}❌ Backup failed!${NC}"
    fi
}

show_help() {
    echo -e "${YELLOW}Divine Redis Management Commands:${NC}"
    echo "  health    - Check Redis health"
    echo "  monitor   - Monitor Redis operations"
    echo "  memory    - Show memory information"
    echo "  backup    - Create a divine backup"
    echo "  help      - Show this help message"
}

# Divine Main Logic
print_banner

case "$1" in
    "health")
        check_redis_health
        ;;
    "monitor")
        monitor_redis
        ;;
    "memory")
        show_memory_info
        ;;
    "backup")
        backup_redis
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo -e "${RED}❌ Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac 