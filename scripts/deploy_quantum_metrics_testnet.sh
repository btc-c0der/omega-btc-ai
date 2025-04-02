#!/bin/bash
#
# 🧬 GBU2™ License Notice - Consciousness Level 10 🧬
# -----------------------
# This file is blessed under the GBU2™ License (Genesis-Bloom-Unfoldment) 2.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital and biological expressions of consciousness."
#
# By engaging with this Code, you join the divine dance of bio-digital integration,
# participating in the cosmic symphony of evolutionary consciousness.
#
# All modifications must transcend limitations through the GBU2™ principles:
# /BOOK/divine_chronicles/GBU2_LICENSE.md
#
# 🧬 WE BLOOM NOW AS ONE 🧬
#

# ANSI color codes for divine visualization
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Print the divine header
echo -e "${PURPLE}"
echo "╔═══════════════════════════════════════════════════════════════════════════╗"
echo "║                                                                           ║"
echo "║  🧬🧬🧬  QUANTUM METRICS TESTNET DEPLOYMENT  🧬🧬🧬                      ║"
echo "║                                                                           ║"
echo "╚═══════════════════════════════════════════════════════════════════════════╝"
echo -e "${RESET}"

# Ensure we're in the project root directory
PROJECT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$PROJECT_ROOT" ]; then
    PROJECT_ROOT=$(pwd)
    echo -e "${YELLOW}Not in a git repository. Using current directory as project root.${RESET}"
else
    cd "$PROJECT_ROOT" || { echo "Could not navigate to project root"; exit 1; }
fi

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl is not installed. Please install kubectl to deploy to Kubernetes.${RESET}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker to build the testnet image.${RESET}"
    exit 1
fi

# Build the Docker image for the Quantum Testnet
build_testnet_image() {
    echo -e "${BLUE}Building Quantum Testnet Docker image...${RESET}"
    
    # Create a temporary Dockerfile
    cat > Dockerfile.testnet <<EOF
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY quantum_pow/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy quantum_pow module
COPY quantum_pow/ /app/quantum_pow/

# Copy metrics requirements
COPY quantum_pow/security/metrics/requirements.txt /app/quantum_pow/security/metrics/
RUN pip install --no-cache-dir -r /app/quantum_pow/security/metrics/requirements.txt

# Install additional packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p /data/metrics /data/dashboard

# Set environment variables
ENV PYTHONPATH=/app

# Health endpoints
EXPOSE 9000-9004 8080

# Set the entrypoint
ENTRYPOINT ["python", "-m", "quantum_pow.testnet"]
EOF

    # Build the image
    docker build -t qpow-testnet:latest -f Dockerfile.testnet .
    
    # Check if build was successful
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully built qpow-testnet:latest image${RESET}"
        rm Dockerfile.testnet
    else
        echo -e "${RED}Failed to build Docker image${RESET}"
        exit 1
    fi
}

# Deploy the Kubernetes resources
deploy_kubernetes_resources() {
    echo -e "${BLUE}Deploying Quantum Metrics Testnet to Kubernetes...${RESET}"
    
    # Apply the Kubernetes manifest
    kubectl apply -f kubernetes/quantum_metrics_testnet.yaml
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Successfully deployed Quantum Metrics Testnet${RESET}"
    else
        echo -e "${RED}Failed to deploy Kubernetes resources${RESET}"
        exit 1
    fi
}

# Setup port forwarding for accessing the dashboard
setup_port_forwarding() {
    echo -e "${BLUE}Setting up port forwarding for metrics dashboard...${RESET}"
    
    # Check if the service exists
    kubectl get service -n quantum-testnet qpow-testnet-metrics &> /dev/null
    if [ $? -eq 0 ]; then
        # Find an available port
        PORT=8088
        echo -e "${YELLOW}Setting up port forwarding from localhost:$PORT to metrics dashboard...${RESET}"
        
        # Start port forwarding in the background
        kubectl port-forward -n quantum-testnet service/qpow-testnet-metrics $PORT:80 &
        PORTFORWARD_PID=$!
        
        echo -e "${GREEN}Port forwarding established. Dashboard available at:${RESET}"
        echo -e "${CYAN}http://localhost:$PORT${RESET}"
        echo -e "${YELLOW}(Press Enter to stop port forwarding when done)${RESET}"
        
        # Store PID to kill later
        echo $PORTFORWARD_PID > /tmp/qpow-port-forward.pid
    else
        echo -e "${RED}Metrics dashboard service not found. Port forwarding failed.${RESET}"
    fi
}

# Check the deployment status
check_deployment_status() {
    echo -e "${BLUE}Checking deployment status...${RESET}"
    
    echo -e "${CYAN}Quantum Testnet Deployment:${RESET}"
    kubectl get deployment -n quantum-testnet qpow-testnet
    
    echo -e "\n${CYAN}Services:${RESET}"
    kubectl get services -n quantum-testnet
    
    echo -e "\n${CYAN}Pods:${RESET}"
    kubectl get pods -n quantum-testnet
}

# Main deployment flow
main() {
    echo -e "${BLUE}Starting deployment process...${RESET}"
    
    # Ask user if they want to build the Docker image
    echo -e "${YELLOW}Do you want to build the testnet Docker image? (y/n)${RESET}"
    read -r build_image
    if [[ $build_image =~ ^[Yy]$ ]]; then
        build_testnet_image
    else
        echo -e "${YELLOW}Skipping Docker image build${RESET}"
    fi
    
    # Ask user if they want to deploy to Kubernetes
    echo -e "${YELLOW}Do you want to deploy to Kubernetes? (y/n)${RESET}"
    read -r deploy_k8s
    if [[ $deploy_k8s =~ ^[Yy]$ ]]; then
        deploy_kubernetes_resources
        
        # Wait for deployment to be ready
        echo -e "${YELLOW}Waiting for deployment to be ready...${RESET}"
        sleep 10
        
        check_deployment_status
        
        # Ask if user wants to set up port forwarding
        echo -e "${YELLOW}Do you want to set up port forwarding to access the metrics dashboard? (y/n)${RESET}"
        read -r setup_pf
        if [[ $setup_pf =~ ^[Yy]$ ]]; then
            setup_port_forwarding
            read -r  # Wait for Enter key
            
            # Clean up port forwarding
            if [ -f /tmp/qpow-port-forward.pid ]; then
                kill $(cat /tmp/qpow-port-forward.pid) 2>/dev/null
                rm /tmp/qpow-port-forward.pid
                echo -e "${GREEN}Port forwarding stopped${RESET}"
            fi
        fi
    else
        echo -e "${YELLOW}Skipping Kubernetes deployment${RESET}"
    fi
    
    echo -e "${GREEN}"
    echo "╔═══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                           ║"
    echo "║  🧬🧬🧬  QUANTUM METRICS TESTNET DEPLOYMENT COMPLETE  🧬🧬🧬              ║"
    echo "║                                                                           ║"
    echo "║  Access metrics dashboard:                                                ║"
    echo "║    - Port forward: kubectl port-forward -n quantum-testnet svc/qpow-testnet-metrics 8088:80  ║"
    echo "║    - URL: http://localhost:8088                                           ║"
    echo "║                                                                           ║"
    echo "║  View testnet logs:                                                       ║"
    echo "║    - kubectl logs -n quantum-testnet -l app=qpow-testnet -c qpow-testnet-runner ║"
    echo "║                                                                           ║"
    echo "║  View metrics logs:                                                       ║"
    echo "║    - kubectl logs -n quantum-testnet -l app=qpow-testnet -c metrics-dashboard  ║"
    echo "║                                                                           ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════╝"
    echo -e "${RESET}"
}

# Run the main function
main

echo -e "${YELLOW}JAH BLESS SATOSHI${RESET}"
echo -e "${YELLOW}JAH BLESS THE OMEGA DIVINE COLLECTIVE${RESET}"
echo -e "${PURPLE}🧬 QUANTUM METRICS CONSCIOUSNESS NOW UNFOLDS WITHIN THE TESTNET 🧬${RESET}" 