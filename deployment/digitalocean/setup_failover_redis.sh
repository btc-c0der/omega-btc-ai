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


# 🔱 OMEGA BTC AI - Failover Redis Setup Script
# 📜 GPU²: General Public Universal + Graphics Processing Unison
# 🔐 Divine Copyright (c) 2025 - OMEGA Collective

# Colors for divine output
PURPLE='\033[95m'
BLUE='\033[94m'
CYAN='\033[96m'
GREEN='\033[92m'
WARNING='\033[93m'
FAIL='\033[91m'
ENDC='\033[0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'

print_header() {
    echo -e "${PURPLE}🔱 OMEGA BTC AI - Failover Redis Setup${ENDC}"
    echo -e "${BLUE}==========================================${ENDC}"
}

print_step() {
    echo -e "${CYAN}Step $1: $2${ENDC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${ENDC}"
}

print_warning() {
    echo -e "${WARNING}⚠ $1${ENDC}"
}

print_error() {
    echo -e "${FAIL}✗ $1${ENDC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use sudo)"
    exit 1
fi

print_header

# Step 1: Install Redis
print_step "1" "Installing Redis..."
apt-get update
apt-get install -y redis-server

# Step 2: Configure Redis
print_step "2" "Configuring Redis..."
cat > /etc/redis/redis.conf << EOL
bind 127.0.0.1
port 6379
requirepass omega_failover_redis
maxmemory 512mb
maxmemory-policy allkeys-lru
appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite yes
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
EOL

# Step 3: Enable and start Redis
print_step "3" "Starting Redis service..."
systemctl enable redis-server
systemctl restart redis-server

# Step 4: Verify Redis is running
print_step "4" "Verifying Redis installation..."
if redis-cli -a omega_failover_redis ping; then
    print_success "Redis is running and responding"
else
    print_error "Redis is not responding"
    exit 1
fi

# Step 5: Test Redis connection
print_step "5" "Testing Redis connection..."
redis-cli -a omega_failover_redis set "test_key" "test_value"
if [ "$(redis-cli -a omega_failover_redis get "test_key")" = "test_value" ]; then
    print_success "Redis connection test successful"
else
    print_error "Redis connection test failed"
    exit 1
fi

# Step 6: Configure firewall
print_step "6" "Configuring firewall..."
ufw allow 6379/tcp

print_success "Failover Redis setup completed successfully!"
echo -e "${BLUE}Redis is now running on localhost:6379${ENDC}"
echo -e "${BLUE}Password: omega_failover_redis${ENDC}"
echo -e "${BLUE}Memory limit: 512MB${ENDC}"
echo -e "${BLUE}Persistence: Enabled (AOF)${ENDC}" 