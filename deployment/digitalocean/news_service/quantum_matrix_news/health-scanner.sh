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


# 💫 Divine Health Scanner for Matrix News Services (Simplified) 💫
# This script automatically detects which ports and endpoints are available

echo -e "\n🔱 DIVINE HEALTH SCANNER INITIATED 🔱\n"

# Host port scan - check which ports are open
echo -e "SCANNING HOST PORTS:"
echo "======================================"

# Ports to check
PORTS_TO_CHECK=(8080 8081 8082 8083 10080 10081 10082 10083 10090 10091)

# Function to check if a port is open
check_port() {
    local port=$1
    if nc -z localhost $port; then
        echo "✅ Port $port is open"
        return 0
    else
        echo "❌ Port $port is closed"
        return 1
    fi
}

# Function to check service health
check_health() {
    local url=$1
    local response=$(curl -s $url)
    if [ $? -eq 0 ]; then
        echo "✅ Health check passed for $url"
        return 0
    else
        echo "❌ Health check failed for $url"
        return 1
    fi
}

# Check all ports
echo "Checking ports..."
for port in "${PORTS_TO_CHECK[@]}"; do
    check_port $port
done

# Check service health
echo -e "\nChecking service health..."
check_health "http://localhost:10091/health"
check_health "http://localhost:10091/ws/health"

echo -e "\nRUNNING CONTAINERS:"
echo "======================================"
docker ps

echo -e "\nTESTING HEALTH ENDPOINTS:"
echo "======================================"

# Define potential health check endpoints
ENDPOINTS=(
    "http://localhost:10091/health"
    "http://localhost:10091/ws/health"
    "http://localhost:10083/health"
    "http://localhost:10083/ws/health"
    "http://localhost:10083/websocket-health/"
    "http://localhost:10083/service-health/"
)

for ENDPOINT in "${ENDPOINTS[@]}"; do
    echo -e "\nTesting $ENDPOINT:"
    curl -s -m 2 $ENDPOINT || echo "Failed to connect"
done

echo -e "\nMANUAL TESTS YOU CAN RUN:"
echo "======================================"
echo "Test WebSocket server health on port 10091:"
echo "  curl http://localhost:10091/health"
echo "  curl http://localhost:10091/ws/health"
echo
echo "Test health endpoint through NGINX proxy:"
echo "  curl http://localhost:10083/ws/health"
echo "  curl http://localhost:10083/websocket-health/"
echo

echo -e "\n🔱 DIVINE HEALTH SCAN COMPLETE 🔱\n" 