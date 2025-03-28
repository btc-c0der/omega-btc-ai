#!/bin/bash

# 🔱 OMEGA BTC AI - Database Performance Monitor
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
    echo -e "${PURPLE}🔱 OMEGA BTC AI - Database Performance Monitor${ENDC}"
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

# Function to get system metrics (using only basic tools)
get_system_metrics() {
    echo -e "\n${BOLD}System Metrics:${ENDC}"
    
    # CPU usage using ps
    cpu_usage=$(ps -eo pcpu | awk 'NR>1 {sum+=$1} END {print sum}')
    echo "CPU Usage: ${cpu_usage}%"
    
    # Memory usage using ps
    mem_usage=$(ps -eo pmem | awk 'NR>1 {sum+=$1} END {print sum}')
    echo "Memory Usage: ${mem_usage}%"
    
    # Network I/O using netstat
    echo "Network I/O: $(netstat -i 2>/dev/null | grep -v "Kernel" | grep -v "Iface" | awk '{print $1, $3, $7}')"
}

# Function to get Redis metrics using Python
get_redis_metrics() {
    echo -e "\n${BOLD}Redis Metrics:${ENDC}"
    
    python3 -c '
import redis
import sys

try:
    r = redis.Redis(
        host="localhost",
        port=6379,
        password="omega_failover_redis",
        socket_timeout=5
    )
    
    info = r.info()
    print(f"Connected Clients: {info["connected_clients"]}")
    print(f"Memory Used: {info["used_memory_human"]}")
    print(f"Commands Processed: {info["total_commands_processed"]}")
    print(f"Keyspace Hits: {info["keyspace_hits"]}")
    print(f"Keyspace Misses: {info["keyspace_misses"]}")
    
except Exception as e:
    print(f"Error connecting to Redis: {str(e)}", file=sys.stderr)
    sys.exit(1)
'
}

# Function to get MongoDB metrics using Python
get_mongodb_metrics() {
    echo -e "\n${BOLD}MongoDB Metrics:${ENDC}"
    
    python3 -c '
from pymongo import MongoClient
import sys

try:
    client = MongoClient(
        "mongodb+srv://omega_mongo:omega_mongo_password@omega-mongo-cluster.mongodb.net/omega_db?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000
    )
    
    db = client.omega_db
    stats = db.command("dbStats")
    
    print(f"Collections: {stats["collections"]}")
    print(f"Data Size: {stats["dataSize"] / 1024 / 1024:.2f} MB")
    print(f"Storage Size: {stats["storageSize"] / 1024 / 1024:.2f} MB")
    print(f"Indexes: {stats["indexes"]}")
    print(f"Index Size: {stats["indexSize"] / 1024 / 1024:.2f} MB")
    
except Exception as e:
    print(f"Error connecting to MongoDB: {str(e)}", file=sys.stderr)
    sys.exit(1)
'
}

# Function to perform Redis benchmark
run_redis_benchmark() {
    echo -e "\n${BOLD}Running Redis Benchmark:${ENDC}"
    
    python3 -c '
import redis
import time
import sys

try:
    r = redis.Redis(
        host="localhost",
        port=6379,
        password="omega_failover_redis",
        socket_timeout=5
    )
    
    start_time = time.time()
    for i in range(100):
        r.set(f"test_key_{i}", f"test_value_{i}")
        r.get(f"test_key_{i}")
    end_time = time.time()
    
    ops_per_second = 200 / (end_time - start_time)
    print(f"Operations per second: {ops_per_second:.2f}")
    
except Exception as e:
    print(f"Error during Redis benchmark: {str(e)}", file=sys.stderr)
    sys.exit(1)
'
}

# Function to perform MongoDB benchmark
run_mongodb_benchmark() {
    echo -e "\n${BOLD}Running MongoDB Benchmark:${ENDC}"
    
    python3 -c '
from pymongo import MongoClient
import time
import sys

try:
    client = MongoClient(
        "mongodb+srv://omega_mongo:omega_mongo_password@omega-mongo-cluster.mongodb.net/omega_db?retryWrites=true&w=majority",
        serverSelectionTimeoutMS=5000
    )
    
    db = client.omega_db
    collection = db.test_collection
    
    start_time = time.time()
    for i in range(100):
        collection.insert_one({"key": f"test_key_{i}", "value": f"test_value_{i}"})
        collection.find_one({"key": f"test_key_{i}"})
    end_time = time.time()
    
    ops_per_second = 200 / (end_time - start_time)
    print(f"Operations per second: {ops_per_second:.2f}")
    
    # Cleanup
    collection.delete_many({})
    
except Exception as e:
    print(f"Error during MongoDB benchmark: {str(e)}", file=sys.stderr)
    sys.exit(1)
'
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
        get_mongodb_metrics
        sleep $interval
    done
}

# Main execution
print_header

# Step 1: Check system before databases
print_step "1" "Checking system performance before databases..."
get_system_metrics

# Step 2: Check Redis connection
print_step "2" "Checking Redis connection..."
if ! python3 -c 'import redis; redis.Redis(host="localhost", port=6379, password="omega_failover_redis", socket_timeout=5).ping()'; then
    print_error "Cannot connect to Redis"
    exit 1
fi
print_success "Redis connection successful"

# Step 3: Check MongoDB connection
print_step "3" "Checking MongoDB connection..."
if ! python3 -c 'from pymongo import MongoClient; MongoClient("mongodb+srv://omega_mongo:omega_mongo_password@omega-mongo-cluster.mongodb.net/omega_db?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000).server_info()'; then
    print_error "Cannot connect to MongoDB"
    exit 1
fi
print_success "MongoDB connection successful"

# Step 4: Run initial benchmarks
print_step "4" "Running initial benchmarks..."
run_redis_benchmark
run_mongodb_benchmark

# Step 5: Monitor performance for 5 minutes
print_step "5" "Monitoring performance for 5 minutes..."
monitor_performance 300 30

# Step 6: Run final benchmarks
print_step "6" "Running final benchmarks..."
run_redis_benchmark
run_mongodb_benchmark

print_success "Performance monitoring completed!"
echo -e "${BLUE}Check the results above for any performance degradation${ENDC}" 