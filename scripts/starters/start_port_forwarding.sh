#!/bin/bash

# 🔱 DIVINE PORT FORWARDING AUTOMATION 🔱
echo "🌟 STARTING DIVINE PORT FORWARDING 🌟"

# Function to check if a port is already in use
check_port() {
    local port=$1
    if lsof -i :$port > /dev/null; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to forward a port with retries
forward_port() {
    local service=$1
    local namespace=$2
    local local_port=$3
    local target_port=$4
    local max_retries=3
    local retry=0

    echo "🔄 Setting up port forwarding for $service..."
    
    while [ $retry -lt $max_retries ]; do
        if ! check_port $local_port; then
            kubectl port-forward service/$service $local_port:$target_port -n $namespace > /dev/null 2>&1 &
            sleep 2
            if check_port $local_port; then
                echo "✅ Port forwarding established for $service on port $local_port"
                return 0
            fi
        fi
        retry=$((retry + 1))
        local_port=$((local_port + 1))
        echo "⚠️ Retrying with port $local_port..."
    done
    
    echo "❌ Failed to establish port forwarding for $service after $max_retries attempts"
    return 1
}

# Kill existing port forwards
echo "🧹 Cleaning up existing port forwards..."
pkill -f "kubectl port-forward"
sleep 2

# Forward Kubernetes Dashboard
echo "🎛️ Setting up Kubernetes Dashboard access..."
forward_port "kubernetes-dashboard" "kubernetes-dashboard" 8443 443

# Forward CLI Portal
echo "🖥️ Setting up CLI Portal access..."
forward_port "cli-portal" "omega-grid-dev" 2222 22

# Forward NFT Services
echo "🎨 Setting up NFT Services access..."
forward_port "nft-services" "omega-grid-dev" 8080 8080

echo "
🌟 DIVINE PORT FORWARDING COMPLETE 🌟

Services available at:
📊 Kubernetes Dashboard: https://localhost:8443
🖥️ CLI Portal: ssh://localhost:2222
🎨 NFT Services: http://localhost:8080

To stop all port forwarding:
$ pkill -f 'kubectl port-forward'
"

# Keep script running to maintain port forwards
echo "Press Ctrl+C to stop all port forwarding..."
wait 