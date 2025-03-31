#!/bin/bash

# 💫 Divine Health Scanner for Matrix News Services (Simplified) 💫
# This script automatically detects which ports and endpoints are available

echo -e "\n🔱 DIVINE HEALTH SCANNER INITIATED 🔱\n"

# Host port scan - check which ports are open
echo -e "SCANNING HOST PORTS:"
echo "======================================"

# Common ports to check in our infrastructure
PORTS_TO_CHECK=(8080 8081 8082 8083 10080 10081 10082 10083 10090 10091 10095)

for PORT in "${PORTS_TO_CHECK[@]}"; do
    # Using timeout to avoid hanging on blocked ports
    nc -z -w1 localhost $PORT 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "Port $PORT is OPEN"
    else
        echo "Port $PORT is CLOSED"
    fi
done

echo -e "\nRUNNING CONTAINERS:"
echo "======================================"
docker ps

echo -e "\nTESTING HEALTH ENDPOINTS:"
echo "======================================"

# Define potential health check endpoints
ENDPOINTS=(
    "http://localhost:10091/health"
    "http://localhost:10091/ws/health"
    "http://localhost:10095/health"
    "http://localhost:10095/ws/health"
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
echo
echo "Test WebSocket server health on port 10095:"
echo "  curl http://localhost:10095/health"
echo
echo "Test health endpoint through NGINX proxy:"
echo "  curl http://localhost:10083/ws/health"
echo "  curl http://localhost:10083/websocket-health/"
echo

echo -e "\n🔱 DIVINE HEALTH SCAN COMPLETE 🔱\n" 