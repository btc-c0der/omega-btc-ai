#!/bin/bash

# 🔱 OMEGA BTC AI - Redis Performance Monitor
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
    echo -e "${PURPLE}🔱 OMEGA BTC AI - Redis Performance Monitor${ENDC}"
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

# Function to get system metrics
get_system_metrics() {
    echo -e "\n${BOLD}System Metrics:${ENDC}"
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}')%"
    echo "Memory Usage: $(free -m | grep Mem | awk '{print $3/$2 * 100.0}')%"
    echo "Disk I/O: $(iostat -x 1 1 | grep -A 1 avg-cpu | tail -n 1 | awk '{print $6, $7}')"
    echo "Network I/O: $(netstat -i | grep -v "Kernel" | grep -v "Iface" | awk '{print $1, $3, $7}')"
}

# Function to get Redis metrics
get_redis_metrics() {
    if ! command -v redis-cli &> /dev/null; then
        print_error "Redis CLI not found"
        return 1
    }

    echo -e "\n${BOLD}Redis Metrics:${ENDC}"
    echo "Connected Clients: $(redis-cli -a omega_failover_redis info clients | grep connected_clients | cut -d: -f2)"
    echo "Memory Used: $(redis-cli -a omega_failover_redis info memory | grep used_memory_human | cut -d: -f2)"
    echo "Commands Processed: $(redis-cli -a omega_failover_redis info stats | grep total_commands_processed | cut -d: -f2)"
    echo "Keyspace Hits: $(redis-cli -a omega_failover_redis info stats | grep keyspace_hits | cut -d: -f2)"
    echo "Keyspace Misses: $(redis-cli -a omega_failover_redis info stats | grep keyspace_misses | cut -d: -f2)"
}

# Function to perform Redis benchmark
run_redis_benchmark() {
    echo -e "\n${BOLD}Running Redis Benchmark:${ENDC}"
    redis-benchmark -a omega_failover_redis -n 1000 -c 50 -P 16 -q
}

# Main monitoring loop
monitor_performance() {
    local duration=$1
    local interval=$2
    local iterations=$((duration / interval))
    
    for ((i=0; i<iterations; i++)); do
        echo -e "\n${BOLD}Iteration $((i+1))/$iterations${ENDC}"
        get_system_metrics
        get_redis_metrics
        sleep $interval
    done
}

# Main execution
print_header

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use sudo)"
    exit 1
fi

# Step 1: Check system before Redis
print_step "1" "Checking system performance before Redis..."
get_system_metrics

# Step 2: Check if Redis is running
print_step "2" "Checking Redis status..."
if systemctl is-active --quiet redis-server; then
    print_warning "Redis is already running. Stopping for clean test..."
    systemctl stop redis-server
    sleep 5
fi

# Step 3: Start Redis
print_step "3" "Starting Redis..."
systemctl start redis-server
sleep 5

# Step 4: Verify Redis is running
print_step "4" "Verifying Redis..."
if ! redis-cli -a omega_failover_redis ping; then
    print_error "Redis failed to start"
    exit 1
fi
print_success "Redis is running"

# Step 5: Run initial benchmark
print_step "5" "Running initial Redis benchmark..."
run_redis_benchmark

# Step 6: Monitor performance for 5 minutes
print_step "6" "Monitoring performance for 5 minutes..."
monitor_performance 300 30

# Step 7: Run final benchmark
print_step "7" "Running final Redis benchmark..."
run_redis_benchmark

print_success "Performance monitoring completed!"
echo -e "${BLUE}Check the results above for any performance degradation${ENDC}" 