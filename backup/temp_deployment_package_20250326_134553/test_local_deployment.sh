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


# OMEGA BTC AI - Local Testing Script
# This script simulates a Scaleway deployment in a local Docker environment

set -e  # Exit on error

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to display script header
display_header() {
    echo -e "${PURPLE}"
    echo "🔱 OMEGA BTC AI - DIVINE COLLECTIVE 🔱"
    echo "LOCAL DEPLOYMENT TEST ENVIRONMENT"
    echo -e "${NC}"
    echo -e "${YELLOW}「テストは信頼の源泉」- Testing is the source of trust${NC}"
    echo
}

# Function to echo with color
echo_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check required dependencies
check_dependencies() {
    echo_color "$BLUE" "Checking required dependencies..."
    
    local missing_deps=0
    
    if ! command_exists docker; then
        echo_color "$RED" "❌ Docker is required but not installed."
        missing_deps=1
    else
        echo_color "$GREEN" "✅ Docker is installed."
    fi
    
    if ! command_exists docker-compose; then
        echo_color "$RED" "❌ Docker Compose is required but not installed."
        missing_deps=1
    else
        echo_color "$GREEN" "✅ Docker Compose is installed."
    fi
    
    if ! command_exists python3; then
        echo_color "$RED" "❌ Python 3 is required but not installed."
        missing_deps=1
    else
        echo_color "$GREEN" "✅ Python 3 is installed."
    fi
    
    if [ $missing_deps -eq 1 ]; then
        echo_color "$RED" "Please install missing dependencies and try again."
        exit 1
    fi
}

# Function to set up test environment variables
setup_test_env() {
    echo_color "$BLUE" "Setting up test environment..."
    
    # Generate a random password for Redis
    REDIS_PASSWORD="omega$(date +%s | sha256sum | base64 | head -c 12)"
    
    # Export environment variables for docker-compose
    export REDIS_PASSWORD=$REDIS_PASSWORD
    export USE_GPU=false
    export TF_FORCE_GPU_ALLOW_GROWTH=false
    
    echo_color "$GREEN" "✅ Test environment configured."
    echo_color "$YELLOW" "Redis password: $REDIS_PASSWORD"
}

# Function to set up directories
setup_directories() {
    echo_color "$BLUE" "Setting up directories..."
    
    # Create temp directories
    mkdir -p ./temp/data/redis
    
    echo_color "$GREEN" "✅ Directories created."
}

# Function to build and deploy the test containers
deploy_test_containers() {
    echo_color "$BLUE" "Building and deploying test containers..."
    
    # Use docker-compose.local.yml to build and start containers
    if docker-compose -f docker-compose.local.yml up -d; then
        echo_color "$GREEN" "✅ Test containers deployed successfully."
        sleep 5 # Give some time for containers to start
        return 0
    else
        echo_color "$RED" "❌ Failed to deploy test containers."
        return 1
    fi
}

# Function to show container status
show_status() {
    echo_color "$BLUE" "Container status:"
    docker-compose -f docker-compose.local.yml ps
}

# Function to show container logs
show_logs() {
    echo_color "$BLUE" "Container logs:"
    docker-compose -f docker-compose.local.yml logs
}

# Function to run Redis test data population
populate_test_data() {
    echo_color "$BLUE" "Populating Redis with test data..."
    
    # Set environment variables for the test script
    export REDIS_HOST=localhost
    export REDIS_PORT=6379
    export REDIS_PASSWORD=$REDIS_PASSWORD
    export REDIS_USE_TLS=false
    
    # Run the test data script
    if python3 ./test_redis_data.py; then
        echo_color "$GREEN" "✅ Test data populated successfully."
        return 0
    else
        echo_color "$RED" "❌ Failed to populate test data."
        return 1
    fi
}

# Function to test Redis data
test_redis_data() {
    echo_color "$BLUE" "Testing Redis data..."
    
    # Create a temporary script to check Redis data
    cat > /tmp/check_redis.sh << EOF
#!/bin/bash
echo "Connecting to Redis..."
redis-cli -h localhost -p 6379 -a "${REDIS_PASSWORD}" ping
echo "Latest BTC price:"
redis-cli -h localhost -p 6379 -a "${REDIS_PASSWORD}" get btc:latest_price
echo "Price prediction:"
redis-cli -h localhost -p 6379 -a "${REDIS_PASSWORD}" get btc:price_prediction
echo "Number of price history entries:"
redis-cli -h localhost -p 6379 -a "${REDIS_PASSWORD}" llen btc:price_history
EOF
    
    chmod +x /tmp/check_redis.sh
    
    # Execute Redis check inside the container
    docker-compose -f docker-compose.local.yml exec mock-scaleway-redis sh -c "sh /tmp/check_redis.sh"
}

# Monitor Redis data in real-time
monitor_redis() {
    echo_color "$BLUE" "Monitoring Redis data in real-time..."
    
    # Set environment variables for the monitor script
    export REDIS_HOST=localhost
    export REDIS_PORT=6379
    export REDIS_PASSWORD=$REDIS_PASSWORD
    export REDIS_USE_TLS=false
    
    # Run the monitor script
    python3 ./monitor_redis.py
}

# Function to clean up
cleanup() {
    echo_color "$BLUE" "Cleaning up test environment..."
    
    read -p "Do you want to stop and remove the test containers? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker-compose -f docker-compose.local.yml down
        rm -rf ./temp
        echo_color "$GREEN" "✅ Test environment cleaned up."
    else
        echo_color "$YELLOW" "Cleanup skipped. Containers are still running."
    fi
}

# Main function
main() {
    echo_color "$BLUE" "=== BTC Live Feed Local Test Environment ==="
    echo_color "$BLUE" "This script will set up a local test environment that simulates the Scaleway deployment."
    
    # Check dependencies
    check_dependencies
    
    # Setup test environment
    setup_test_env
    
    # Setup directories
    setup_directories
    
    # Deploy test containers
    if ! deploy_test_containers; then
        echo_color "$RED" "Exiting due to deployment failure."
        exit 1
    fi
    
    # Show container status
    show_status
    
    # Populate test data
    echo_color "$YELLOW" "Do you want to populate Redis with test data? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if ! populate_test_data; then
            echo_color "$RED" "Warning: Test data population failed."
        fi
    fi
    
    # Ask if user wants to see logs
    echo_color "$YELLOW" "Do you want to see the container logs? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        show_logs
    fi
    
    # Ask if user wants to test Redis data
    echo_color "$YELLOW" "Do you want to test Redis data? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        test_redis_data
    fi
    
    # Ask if user wants to monitor Redis data
    echo_color "$YELLOW" "Do you want to monitor Redis data in real-time? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        monitor_redis
    else
        echo_color "$GREEN" "✅ Test environment is now running."
        echo_color "$GREEN" "The BTC Live Feed is connecting to the mock Scaleway Redis."
        echo_color "$YELLOW" "To stop the test environment and clean up, press any key..."
        read -n 1 -r
    fi
    
    # Cleanup
    cleanup
}

# Run the main function
main 