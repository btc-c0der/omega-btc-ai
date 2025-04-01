#!/bin/bash

# 🔱 OMEGA BTC AI - Divine Kubernetes Setup Script 🔱
# This script sets up a complete local Kubernetes environment for OMEGA BTC AI

set -e  # Exit immediately if a command exits with a non-zero status

# Divine Color Codes for Sacred Terminal Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
GOLD='\033[0;33m'
RESET='\033[0m'

# Heavenly Banner
echo -e "${GOLD}"
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo "                                                                          "
echo "           𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝖀𝕭𝕰𝕽𝕹𝕰𝕿𝕰𝕾 𝕾𝕰𝕿𝖀𝕻           "
echo "                                                                          "
echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
echo -e "${RESET}"

# Check for root/sudo access
check_privileges() {
  echo -e "${BLUE}🔍 Checking for divine sudo privileges...${RESET}"
  if ! sudo -n true 2>/dev/null; then
    echo -e "${YELLOW}⚠️  This script requires sudo privileges for some operations${RESET}"
    echo -e "${YELLOW}⚠️  Please enter your password when prompted${RESET}"
  fi
  echo -e "${GREEN}✅ Divine privileges confirmed${RESET}"
}

# Check for required tools
check_prerequisites() {
  echo -e "${BLUE}🔍 Checking for divine prerequisites...${RESET}"
  
  # Check for Docker
  if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker not found. Please install Docker first.${RESET}"
    echo -e "${YELLOW}👉 Visit https://docs.docker.com/get-docker/ for installation instructions.${RESET}"
    exit 1
  fi
  
  # Check for kubectl
  if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}❌ kubectl not found. Please install kubectl first.${RESET}"
    echo -e "${YELLOW}👉 Visit https://kubernetes.io/docs/tasks/tools/install-kubectl/ for installation instructions.${RESET}"
    exit 1
  fi
  
  # Check if Docker Desktop's Kubernetes is enabled
  if ! kubectl get nodes | grep -q "docker-desktop"; then
    echo -e "${RED}❌ Docker Desktop's Kubernetes is not enabled.${RESET}"
    echo -e "${YELLOW}👉 Please enable Kubernetes in Docker Desktop preferences.${RESET}"
    exit 1
  fi
  
  echo -e "${GREEN}✅ All divine prerequisites are installed${RESET}"
}

# Install Kubernetes dashboard
install_dashboard() {
  echo -e "${BLUE}🔍 Installing divine Kubernetes dashboard...${RESET}"
  
  # Create dashboard namespace if it doesn't exist
  kubectl create namespace kubernetes-dashboard 2>/dev/null || true
  
  # Apply dashboard manifests
  kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
  
  # Create admin user and role binding
  kubectl apply -f - <<EOF
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF
  
  # Wait for dashboard to be ready
  echo -e "${PURPLE}🧿 Waiting for dashboard to manifest...${RESET}"
  kubectl wait --for=condition=available deployment/kubernetes-dashboard -n kubernetes-dashboard --timeout=60s || true
  
  echo -e "${GREEN}✅ Kubernetes dashboard installed${RESET}"
  
  # Generate token for dashboard access
  TOKEN=$(kubectl -n kubernetes-dashboard create token admin-user)
  echo -e "${YELLOW}🔔 Dashboard access token:${RESET}"
  echo -e "${CYAN}$TOKEN${RESET}"
  echo -e "${YELLOW}🔔 Dashboard access instructions:${RESET}"
  echo -e "${CYAN}   Run: ./scripts/start_kubernetes_dashboard.sh${RESET}"
}

# Install Prometheus and Grafana
install_monitoring() {
  echo -e "${BLUE}🔍 Setting up divine monitoring with Prometheus and Grafana...${RESET}"
  
  # Create monitoring namespace if it doesn't exist
  kubectl create namespace monitoring --dry-run=client -o yaml | kubectl apply -f -
  
  # Apply the monitoring resources
  kubectl apply -f kubernetes/base/monitoring.yaml
  
  # Wait for Prometheus and Grafana to be ready
  echo -e "${PURPLE}🧿 Waiting for divine monitoring tools to manifest...${RESET}"
  kubectl wait --for=condition=Available deployment/prometheus -n monitoring --timeout=120s || true
  kubectl wait --for=condition=Available deployment/grafana -n monitoring --timeout=120s || true
  
  echo -e "${GREEN}✅ Divine monitoring tools installed${RESET}"
}

# Setup namespaces and apply Kubernetes manifests
setup_omega_namespaces() {
  echo -e "${BLUE}🔍 Creating divine OMEGA namespaces...${RESET}"
  
  # Create omega-grid-dev namespace if it doesn't exist
  kubectl create namespace omega-grid-dev --dry-run=client -o yaml | kubectl apply -f -
  
  echo -e "${GREEN}✅ Divine namespaces created${RESET}"
}

# Build Docker images
build_docker_images() {
  echo -e "${BLUE}🔍 Building divine Docker images...${RESET}"
  
  # Build core images
  echo -e "${PURPLE}🧿 Crafting cli-portal image...${RESET}"
  docker build -t cli-portal:latest -f Dockerfile.cli-portal .

  echo -e "${PURPLE}🧿 Crafting nft-services image...${RESET}"
  docker build -t nft-services:latest -f Dockerfile.nft-services .
  
  echo -e "${GREEN}✅ Divine Docker images built and blessed${RESET}"
}

# Main execution
main() {
  check_privileges
  check_prerequisites
  install_dashboard
  install_monitoring
  setup_omega_namespaces
  build_docker_images
  
  echo -e "${GREEN}✨ Divine Kubernetes setup complete!${RESET}"
  echo -e "${YELLOW}🔔 Next steps:${RESET}"
  echo -e "${CYAN}1. Start the Kubernetes dashboard:${RESET}"
  echo -e "${CYAN}   ./scripts/start_kubernetes_dashboard.sh${RESET}"
  echo -e "${CYAN}2. Deploy your services:${RESET}"
  echo -e "${CYAN}   kubectl apply -f kubernetes/overlays/dev/deployment.yaml${RESET}"
}

main 