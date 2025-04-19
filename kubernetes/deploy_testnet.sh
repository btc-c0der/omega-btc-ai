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

set -e

# Variables
NAMESPACE="qpow-testnet"
IMAGE_NAME="qpow-testnet"
IMAGE_TAG="latest"

# Print banner
echo "=========================================="
echo "qPoW Testnet Kubernetes Deployment Script"
echo "=========================================="
echo ""

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl not found. Please install kubectl first."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "docker not found. Please install Docker first."
    exit 1
fi

# Create namespace if it doesn't exist
echo "Creating namespace $NAMESPACE if it doesn't exist..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

# Build the Docker image
echo "Building Docker image $IMAGE_NAME:$IMAGE_TAG..."
cd $(dirname "$0")/..
docker build -t $IMAGE_NAME:$IMAGE_TAG -f kubernetes/Dockerfile.testnet .

# Load the image to kind (if using kind)
if command -v kind &> /dev/null; then
    if kind get clusters | grep -q "kind"; then
        echo "Loading image to kind cluster..."
        kind load docker-image $IMAGE_NAME:$IMAGE_TAG
    fi
fi

# Apply Kubernetes manifests
echo "Applying Kubernetes manifests..."
kubectl apply -f kubernetes/quantum_testnet.yaml -n $NAMESPACE

# Create or update ConfigMap with testnet configuration
echo "Creating ConfigMap with testnet configuration..."
cat <<EOF | kubectl apply -n $NAMESPACE -f -
apiVersion: v1
kind: ConfigMap
metadata:
  name: qpow-testnet-config
data:
  testnet-config.json: |
    {
      "node_count": 3,
      "mine_interval": 10,
      "tx_interval": 5,
      "run_time": null
    }
EOF

# Wait for deployment to be ready
echo "Waiting for deployment to be ready..."
kubectl rollout status deployment/qpow-testnet -n $NAMESPACE --timeout=5m

# Get node ports
NODE_PORTS=$(kubectl get svc qpow-testnet-service -n $NAMESPACE -o jsonpath='{.spec.ports[*].nodePort}')
NODE_PORT_ARRAY=($NODE_PORTS)

echo ""
echo "=========================================="
echo "qPoW Testnet Deployment Completed!"
echo "=========================================="
echo ""
echo "You can access the testnet nodes at:"
for i in "${!NODE_PORT_ARRAY[@]}"; do
    echo "Node $i: http://localhost:${NODE_PORT_ARRAY[$i]}"
done
echo ""
echo "To view the logs, run:"
echo "kubectl logs -f deployment/qpow-testnet -n $NAMESPACE"
echo ""
echo "To check the blockchain status, run:"
echo "kubectl exec -it \$(kubectl get pods -n $NAMESPACE -l app=qpow-testnet -o jsonpath='{.items[0].metadata.name}') -n $NAMESPACE -- python -c 'from quantum_pow.testnet import Testnet, TestnetConfig; config = TestnetConfig(); testnet = Testnet(config); print(testnet.get_blockchain_stats())'"
echo ""
echo "To stop the testnet, run:"
echo "kubectl delete -f kubernetes/quantum_testnet.yaml -n $NAMESPACE"
echo "==========================================" 