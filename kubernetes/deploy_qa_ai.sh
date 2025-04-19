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


# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}Starting QA AI deployment...${NC}"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl is not installed${NC}"
    exit 1
fi

# Check if we're connected to a Kubernetes cluster
if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Not connected to a Kubernetes cluster${NC}"
    exit 1
fi

# Create namespace if it doesn't exist
echo -e "${YELLOW}Creating QA AI namespace...${NC}"
kubectl create namespace qa-ai --dry-run=client -o yaml | kubectl apply -f -

# Apply the QA AI deployment
echo -e "${YELLOW}Applying QA AI deployment...${NC}"
kubectl apply -f kubernetes/qa_ai_deployment.yaml

# Wait for deployments to be ready
echo -e "${YELLOW}Waiting for deployments to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/qa-ai-dashboard -n qa-ai
kubectl wait --for=condition=available --timeout=300s deployment/qa-ai-metrics -n qa-ai
kubectl wait --for=condition=available --timeout=300s deployment/qa-ai-personas -n qa-ai
kubectl wait --for=condition=available --timeout=300s deployment/qa-ai-cli -n qa-ai

# Get the dashboard service URL
echo -e "${YELLOW}Getting dashboard service URL...${NC}"
DASHBOARD_URL=$(kubectl get service qa-ai-dashboard -n qa-ai -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
if [ -z "$DASHBOARD_URL" ]; then
    DASHBOARD_URL=$(kubectl get service qa-ai-dashboard -n qa-ai -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
fi

if [ -n "$DASHBOARD_URL" ]; then
    echo -e "${GREEN}QA AI Dashboard is available at: http://${DASHBOARD_URL}${NC}"
else
    echo -e "${YELLOW}To access the dashboard, use port forwarding:${NC}"
    echo -e "${YELLOW}kubectl port-forward service/qa-ai-dashboard -n qa-ai 3000:80${NC}"
fi

echo -e "${GREEN}QA AI deployment completed successfully!${NC}" 