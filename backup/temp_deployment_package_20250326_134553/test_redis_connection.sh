#!/bin/bash

# OMEGA BTC AI - Redis Connection Test Script
# This script tests the connection to your Redis instance

set -e  # Exit on error

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default configuration
USE_LOCAL=true
USE_SCALEWAY=false

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --local) USE_LOCAL=true; USE_SCALEWAY=false ;;
        --scale) USE_LOCAL=false; USE_SCALEWAY=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Logging function with timestamp
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    case $level in
        "INFO") echo -e "${BLUE}[$timestamp] INFO: $message${NC}" ;;
        "SUCCESS") echo -e "${GREEN}[$timestamp] SUCCESS: $message${NC}" ;;
        "WARNING") echo -e "${YELLOW}[$timestamp] WARNING: $message${NC}" ;;
        "ERROR") echo -e "${RED}[$timestamp] ERROR: $message${NC}" ;;
    esac
}

# Function to test Redis connection with timeout
test_redis_connection() {
    local cmd="$1"
    local timeout=10  # 10 seconds timeout
    
    log "INFO" "Attempting Redis connection with timeout of ${timeout}s..."
    
    # Run the command with timeout
    if gtimeout $timeout $cmd ping > /dev/null 2>&1; then
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            log "ERROR" "Connection timed out after ${timeout} seconds"
            return 1
        else
            log "ERROR" "Connection failed with exit code $exit_code"
            return 1
        fi
    fi
}

# Banner
echo -e "${BLUE}"
echo "=================================================="
echo "  OMEGA BTC AI - REDIS CONNECTION TEST"
echo "=================================================="
echo -e "${NC}"

# System information
log "INFO" "System Information:"
log "INFO" "OS: $(uname -a)"
log "INFO" "CPU: $(sysctl -n machdep.cpu.brand_string 2>/dev/null || echo 'Unknown')"
log "INFO" "Memory: $(sysctl -n hw.memsize 2>/dev/null | awk '{print int($1/1024/1024/1024)"GB"}' || echo 'Unknown')"
log "INFO" "Disk Space: $(df -h / | grep -v Filesystem | awk '{print $4}')"

# Check if redis-cli is installed
if ! command -v redis-cli &> /dev/null; then
    log "WARNING" "Redis client not found. Please install with: brew install redis"
    exit 1
fi

# Check if gtimeout command is available (from coreutils)
if ! command -v gtimeout &> /dev/null; then
    log "WARNING" "gtimeout command not found. Installing coreutils..."
    if ! command -v brew &> /dev/null; then
        log "ERROR" "Homebrew is not installed. Please install Homebrew first."
        exit 1
    fi
    brew install coreutils
    log "SUCCESS" "coreutils installed successfully"
fi

# Load appropriate configuration
if [ "$USE_SCALEWAY" = true ] && [ -f .env.scaleway ]; then
    log "INFO" "Loading Scaleway Redis configuration..."
    source .env.scaleway
    REDIS_HOST=${REDIS_HOST:-172.16.8.2}
    REDIS_PORT=${REDIS_PORT:-6379}
    REDIS_SSL=${REDIS_SSL:-yes}
    REDIS_SSL_CERT=${REDIS_SSL_CERT:-SSL_redis-btc-omega-redis.pem}
else
    log "INFO" "Using local Redis configuration..."
    REDIS_HOST=localhost
    REDIS_PORT=6379
    REDIS_PASSWORD=""
    REDIS_SSL="no"
fi

log "INFO" "Redis Configuration:"
log "INFO" "Host: ${REDIS_HOST}"
log "INFO" "Port: ${REDIS_PORT}"
log "INFO" "Password: ${REDIS_PASSWORD:+[SET]}"
log "INFO" "SSL: ${REDIS_SSL:-no}"
if [ "${REDIS_SSL:-no}" = "yes" ]; then
    log "INFO" "SSL Certificate: ${REDIS_SSL_CERT}"
fi

# Verify SSL certificate if it exists
if [ "${REDIS_SSL:-no}" = "yes" ] && [ -f "${REDIS_SSL_CERT}" ]; then
    log "INFO" "Verifying SSL certificate..."
    if openssl verify -CAfile "${REDIS_SSL_CERT}" "${REDIS_SSL_CERT}" 2>/dev/null; then
        log "SUCCESS" "SSL certificate is valid"
    else
        log "WARNING" "SSL certificate is self-signed (this is normal for Scaleway Redis)"
    fi
fi

# Test connection and measure latency
log "INFO" "Testing Redis connection and measuring latency..."
start_time=$(date +%s%N)

# Build Redis CLI command with SSL if enabled
REDIS_CMD="redis-cli"
if [ "${REDIS_SSL:-no}" = "yes" ]; then
    REDIS_CMD="$REDIS_CMD --tls --cert ${REDIS_SSL_CERT}"
fi
REDIS_CMD="$REDIS_CMD -h $REDIS_HOST -p $REDIS_PORT"

if [ -n "$REDIS_PASSWORD" ]; then
    REDIS_CMD="$REDIS_CMD -a $REDIS_PASSWORD"
fi

# Test connection with timeout
if test_redis_connection "$REDIS_CMD"; then
    end_time=$(date +%s%N)
    latency=$(( (end_time - start_time) / 1000000 )) # Convert to milliseconds
    log "SUCCESS" "Connection successful! Latency: ${latency}ms"
    
    # Get Redis server info
    log "INFO" "Redis Server Information:"
    timeout 10 $REDIS_CMD info | grep -E "^(redis_version|used_memory_human|connected_clients|uptime_in_seconds)" | while read -r line; do
        log "INFO" "$line"
    done
else
    log "ERROR" "Connection failed"
    log "ERROR" "Please check:"
    if [ "$USE_SCALEWAY" = true ]; then
        log "ERROR" "1. VPN connection is active (ip a | grep tun)"
        log "ERROR" "2. Network connectivity to Redis (ping ${REDIS_HOST})"
        log "ERROR" "3. SSL certificate is valid and accessible"
        log "ERROR" "4. Redis password is correct (if required)"
        log "ERROR" "5. Firewall rules allow connection to Redis port"
    else
        log "ERROR" "1. Redis is running locally (docker ps | grep redis)"
        log "ERROR" "2. Port 6379 is available (lsof -i :6379)"
        log "ERROR" "3. Docker network is properly configured"
        log "ERROR" "4. No conflicting Redis instances"
    fi
    exit 1
fi

# Check for existing trap probability data
log "INFO" "Checking for trap probability data..."
TRAP_KEY_COUNT=$(timeout 10 $REDIS_CMD keys "trap_probability_*" | wc -l)
TRAP_KEYS=$(timeout 10 $REDIS_CMD keys "trap_probability_*" | head -n 5)

if [ "$TRAP_KEY_COUNT" -gt 0 ]; then
    log "SUCCESS" "Found $TRAP_KEY_COUNT trap probability keys in Redis"
    log "INFO" "Sample keys:"
    echo "$TRAP_KEYS" | while read -r key; do
        log "INFO" "  - $key"
    done
else
    log "WARNING" "No trap probability data found in Redis yet"
fi

# Check for trader position data
log "INFO" "Checking for trader position data..."
TRADER_KEY_COUNT=$(timeout 10 $REDIS_CMD keys "trader:*" | wc -l)
TRADER_KEYS=$(timeout 10 $REDIS_CMD keys "trader:*" | head -n 5)

if [ "$TRADER_KEY_COUNT" -gt 0 ]; then
    log "SUCCESS" "Found $TRADER_KEY_COUNT trader keys in Redis"
    log "INFO" "Sample keys:"
    echo "$TRADER_KEYS" | while read -r key; do
        log "INFO" "  - $key"
    done
else
    log "WARNING" "No trader data found in Redis yet"
fi

# Check Redis memory usage
log "INFO" "Checking Redis memory usage..."
MEMORY_USAGE=$(timeout 10 $REDIS_CMD info | grep used_memory_human | cut -d: -f2)
log "INFO" "Current Redis memory usage: $MEMORY_USAGE"

# List all Redis keys with types and sizes
log "INFO" "Listing all Redis keys..."
echo -e "${BLUE}=================================================="
echo "  REDIS KEYS OVERVIEW"
echo "==================================================${NC}"
echo -e "${YELLOW}FORMAT: KEY (TYPE) [SIZE]${NC}\n"

# Initialize counters for different types
total_keys=0
string_keys=0
list_keys=0
set_keys=0
zset_keys=0
hash_keys=0
other_keys=0

# Get all keys and process each one
$REDIS_CMD keys "*" | while read -r key; do
    if [ -n "$key" ]; then
        # Increment total keys
        total_keys=$((total_keys + 1))
        
        # Get key type
        key_type=$($REDIS_CMD type "$key")
        
        # Update type counters
        case $key_type in
            "string") string_keys=$((string_keys + 1)) ;;
            "list") list_keys=$((list_keys + 1)) ;;
            "set") set_keys=$((set_keys + 1)) ;;
            "zset") zset_keys=$((zset_keys + 1)) ;;
            "hash") hash_keys=$((hash_keys + 1)) ;;
            *) other_keys=$((other_keys + 1)) ;;
        esac
        
        # Get size and latest data based on type
        case $key_type in
            "string")
                size=$($REDIS_CMD strlen "$key")
                value_preview=$($REDIS_CMD get "$key" | cut -c 1-50)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC}) [${YELLOW}$size bytes${NC}]"
                echo -e "  Latest: ${value_preview}..."
                ;;
            "list")
                size=$($REDIS_CMD llen "$key")
                latest_elem=$($REDIS_CMD lindex "$key" 0 | cut -c 1-50)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC}) [${YELLOW}$size items${NC}]"
                echo -e "  Latest: ${latest_elem}..."
                ;;
            "set")
                size=$($REDIS_CMD scard "$key")
                latest=$($REDIS_CMD srandmember "$key" 1 | cut -c 1-50)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC}) [${YELLOW}$size members${NC}]"
                echo -e "  Sample: ${latest}..."
                ;;
            "zset")
                size=$($REDIS_CMD zcard "$key")
                latest_elem=$($REDIS_CMD zrevrange "$key" 0 0 | cut -c 1-50)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC}) [${YELLOW}$size members${NC}]"
                echo -e "  Latest: ${latest_elem}..."
                ;;
            "hash")
                size=$($REDIS_CMD hlen "$key")
                latest_field=$($REDIS_CMD hkeys "$key" | tail -n 1)
                latest_value=$($REDIS_CMD hget "$key" "$latest_field" | cut -c 1-50)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC}) [${YELLOW}$size fields${NC}]"
                echo -e "  Latest: ${latest_field} = ${latest_value}..."
                ;;
            *)
                echo -e "${GREEN}$key${NC} (${BLUE}$key_type${NC})"
                ;;
        esac
    fi
done

# Print key statistics
echo -e "\n${BLUE}=================================================="
echo "  REDIS KEY STATISTICS"
echo "==================================================${NC}"
echo -e "${YELLOW}Total Keys: $total_keys${NC}"
echo -e "String Keys: $string_keys"
echo -e "List Keys: $list_keys"
echo -e "Set Keys: $set_keys"
echo -e "Sorted Set Keys: $zset_keys"
echo -e "Hash Keys: $hash_keys"
echo -e "Other Keys: $other_keys"

echo -e "\n${BLUE}=================================================="
echo "  END OF REDIS KEYS"
echo "==================================================${NC}"

echo -e "${GREEN}"
echo "=================================================="
echo "  CONNECTION TEST COMPLETE!"
echo "=================================================="
echo -e "${NC}"

# Provide recommendations based on results
if [ "$TRAP_KEY_COUNT" -eq 0 ] && [ "$TRADER_KEY_COUNT" -eq 0 ]; then
    log "WARNING" "Recommendations:"
    log "WARNING" "1. Ensure the BTC Live Feed service is running"
    log "WARNING" "2. Check if data is being properly written to Redis"
    log "WARNING" "3. Verify Redis connection settings in your application"
fi

# Exit with appropriate status
if [ "$TRAP_KEY_COUNT" -gt 0 ] || [ "$TRADER_KEY_COUNT" -gt 0 ]; then
    exit 0
else
    exit 1
fi 