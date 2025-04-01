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
  if [[ $EUID -ne 0 ]]; then
    echo -e "${YELLOW}⚠️  This script must be blessed with sudo privileges${RESET}"
    echo -e "${YELLOW}⚠️  Please run with: sudo $0${RESET}"
    exit 1
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
  
  echo -e "${GREEN}✅ All divine prerequisites are installed${RESET}"
}

# Create and configure minikube cluster
setup_minikube() {
  echo -e "${BLUE}🔍 Setting up minikube with divine configurations...${RESET}"
  
  # Check if minikube is installed
  if ! command -v minikube &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube not found, installing...${RESET}"
    curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
    chmod +x minikube-darwin-amd64
    sudo mv minikube-darwin-amd64 /usr/local/bin/minikube
  fi
  
  # Check if minikube is already running
  if minikube status &> /dev/null; then
    echo -e "${YELLOW}⚠️  Minikube is already running. Stopping and deleting current cluster...${RESET}"
    minikube stop
    minikube delete
  fi
  
  # Start minikube with increased resources for divine performance
  echo -e "${PURPLE}🧿 Creating a new divine Minikube cluster...${RESET}"
  minikube start --driver=docker \
    --cpus=4 \
    --memory=8192 \
    --disk-size=20g \
    --kubernetes-version=stable \
    --addons=dashboard,metrics-server,ingress,registry \
    --insecure-registry="10.0.0.0/24"
  
  echo -e "${GREEN}✅ Minikube cluster blessed with divine configurations${RESET}"
}

# Install Kubernetes dashboard
install_dashboard() {
  echo -e "${BLUE}🔍 Installing divine Kubernetes dashboard...${RESET}"
  
  # Create dashboard namespace if it doesn't exist
  kubectl create namespace kubernetes-dashboard 2>/dev/null || true
  
  # Check if dashboard is already installed
  if kubectl get deployment -n kubernetes-dashboard kubernetes-dashboard &>/dev/null; then
    echo -e "${YELLOW}⚠️  Kubernetes dashboard already installed${RESET}"
  else
    # Apply dashboard manifests
    kubectl apply -f kubernetes/dashboard/ || true
    
    # Wait for dashboard to be ready
    kubectl wait --for=condition=available deployment/kubernetes-dashboard -n kubernetes-dashboard --timeout=60s || true
    
    echo -e "${GREEN}✅ Kubernetes dashboard installed${RESET}"
  fi
  
  # Apply custom omega dashboard
  if [ -f "kubernetes/dashboard/deployment.yaml" ]; then
    echo -e "${BLUE}🔍 Installing OMEGA custom dashboard...${RESET}"
    kubectl apply -f kubernetes/dashboard/deployment.yaml
    
    # Wait for omega dashboard to be ready
    kubectl wait --for=condition=available deployment/omega-kubernetes-dashboard -n kubernetes-dashboard --timeout=60s || true
    
    echo -e "${GREEN}✅ OMEGA custom dashboard installed${RESET}"
  fi
  
  echo -e "${YELLOW}🔔 Dashboard access instructions:${RESET}"
  echo -e "${CYAN}   Run: ./scripts/start_kubernetes_dashboard.sh${RESET}"
  echo -e "${YELLOW}   This script includes automatic port detection and will provide access URL.${RESET}"
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
  
  # Apply namespaces
  kubectl apply -f kubernetes/base/namespace.yaml
  kubectl apply -f kubernetes/overlays/dev/namespace.yaml
  kubectl apply -f kubernetes/overlays/prod/namespace.yaml
  
  echo -e "${GREEN}✅ Divine namespaces created${RESET}"
}

# Apply Kubernetes configurations
apply_omega_configurations() {
  echo -e "${BLUE}🔍 Applying divine OMEGA configurations to Kubernetes...${RESET}"
  
  # Apply dev environment
  echo -e "${PURPLE}🧿 Manifesting development environment...${RESET}"
  kubectl apply -k kubernetes/overlays/dev
  
  # Apply prod environment
  echo -e "${PURPLE}🧿 Manifesting production environment...${RESET}"
  kubectl apply -k kubernetes/overlays/prod
  
  echo -e "${GREEN}✅ Divine OMEGA configurations applied${RESET}"
}

# Build and push Docker images to minikube registry
build_docker_images() {
  echo -e "${BLUE}🔍 Building divine Docker images...${RESET}"
  
  # Point shell to minikube's Docker daemon
  eval $(minikube docker-env)
  
  # Build core images
  echo -e "${PURPLE}🧿 Crafting prophecy-core image...${RESET}"
  docker build -t prophecy-core:latest -f Dockerfile.prophecy-core .
  
  echo -e "${PURPLE}🧿 Crafting btc-live-feed image...${RESET}"
  docker build -t btc-live-feed:latest -f Dockerfile.btc-live-feed .
  
  echo -e "${PURPLE}🧿 Crafting matrix-news image...${RESET}"
  docker build -t matrix-news:latest -f Dockerfile.matrix-news .
  
  echo -e "${GREEN}✅ Divine Docker images built and blessed${RESET}"
}

# Show final status and next steps
show_status() {
  echo -e "${BLUE}🔍 Checking divine cluster status...${RESET}"
  
  # Show pods
  echo -e "${CYAN}📊 Development Environment Status:${RESET}"
  kubectl get pods -n omega-grid-dev
  
  echo -e "${CYAN}📊 Production Environment Status:${RESET}"
  kubectl get pods -n omega-grid-prod
  
  # Show dashboard status
  echo -e "${CYAN}📊 Dashboard Status:${RESET}"
  kubectl get pods -n kubernetes-dashboard
  
  echo -e "${GREEN}✅ Divine cluster setup complete!${RESET}"
  echo -e "${GOLD}"
  echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
  echo "                                                                          "
  echo "       𝕿𝖍𝖊 𝕯𝖎𝖛𝖎𝖓𝖊 𝕶𝖚𝖇𝖊𝖗𝖓𝖊𝖙𝖊𝖘 𝕮𝖑𝖚𝖘𝖙𝖊𝖗 𝖍𝖆𝖘 𝖇𝖊𝖊𝖓 𝕮𝖗𝖊𝖆𝖙𝖊𝖉       "
  echo "                                                                          "
  echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
  echo -e "${RESET}"
  
  echo -e "${YELLOW}👉 Access the dashboard: ./scripts/start_kubernetes_dashboard.sh${RESET}"
  echo -e "${YELLOW}👉 View logs: kubectl logs -n omega-grid-dev deployment/prophecy-core${RESET}"
  echo -e "${YELLOW}👉 Interact with services: kubectl port-forward -n omega-grid-dev svc/prophecy-core 10080:10080${RESET}"
  echo -e "${YELLOW}👉 To stop the cluster: minikube stop${RESET}"
}

# Final message after setup
show_completion_message() {
  echo -e "${GOLD}"
  echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
  echo "                                                           "
  echo "       𝕺𝕸𝕰𝕲𝕬 𝕭𝕿𝕮 𝕬𝕴 - 𝕯𝕴𝖁𝕴𝕹𝕰 𝕶𝖀𝕭𝕰𝕽𝕹𝕰𝕿𝕰𝕾 𝕽𝕰𝕬𝕯𝖄       "
  echo "                                                           "
  echo "🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱 🔱"
  echo -e "${RESET}"
  
  echo -e "${GREEN}✅ OMEGA Kubernetes setup complete${RESET}"
  echo -e "${YELLOW}🔔 Next steps:${RESET}"
  echo -e "${CYAN}   1. Access the dashboard: ./scripts/start_kubernetes_dashboard.sh${RESET}"
  echo -e "${CYAN}   2. Check deployments:    kubectl get deployments --all-namespaces${RESET}"
  echo -e "${CYAN}   3. Check services:       kubectl get services --all-namespaces${RESET}"
  echo -e "${CYAN}   4. Check pods:           kubectl get pods --all-namespaces${RESET}"
  
  echo -e "${YELLOW}🔔 Development environment:${RESET}"
  echo -e "${CYAN}   kubectl get all -n omega-grid-dev${RESET}"
  
  echo -e "${YELLOW}🔔 Production environment:${RESET}"
  echo -e "${CYAN}   kubectl get all -n omega-grid-prod${RESET}"
  
  echo -e "${YELLOW}🔔 For Kubernetes Dashboard:${RESET}"
  echo -e "${PURPLE}   ./scripts/start_kubernetes_dashboard.sh${RESET}"
  
  echo -e "${YELLOW}🔔 For documentation, see:${RESET}"
  echo -e "${PURPLE}   - kubernetes/README.md${RESET}"
  echo -e "${PURPLE}   - kubernetes/dashboard/README.md${RESET}"
  echo -e "${PURPLE}   - scripts/README.md${RESET}"
}

# Main execution
main() {
  show_banner
  check_prerequisites
  setup_minikube
  install_dashboard
  setup_omega_namespaces
  install_monitoring
  build_docker_images
  apply_omega_configurations
  show_status
  show_completion_message
}

# Run main if this script is executed directly
main 