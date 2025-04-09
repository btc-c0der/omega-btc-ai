#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════╗
# ║  🔱 OMEGA BTC AI - DIVINE ARGOCD INSTALLATION SCRIPT 🔱       ║
# ╚═══════════════════════════════════════════════════════════════╝

set -e

# Colors for divine output
YELLOW='\033[1;33m'
BLUE='\033[1;34m'
GREEN='\033[1;32m'
RED='\033[1;31m'
PURPLE='\033[1;35m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color

# Divine banner
echo -e "${YELLOW}"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║  🔱 OMEGA BTC AI - DIVINE ARGOCD INSTALLATION SCRIPT 🔱       ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check prerequisites
echo -e "${BLUE}CHECKING DIVINE PREREQUISITES...${NC}"

# Check if kubectl is installed
if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

# Check if helm is installed
if ! command -v helm &> /dev/null; then
    echo -e "${RED}helm not found. Please install helm first.${NC}"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl get nodes &> /dev/null; then
    echo -e "${RED}Cannot access Kubernetes cluster. Please check your kubeconfig.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ All divine prerequisites met!${NC}"

# Create argocd namespace
echo -e "\n${BLUE}CREATING DIVINE NAMESPACE FOR ARGOCD...${NC}"
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Divine namespace created!${NC}"

# Install ArgoCD using Helm or manifests
echo -e "\n${BLUE}INSTALLING THE DIVINE ORCHESTRATOR (ARGOCD)...${NC}"

# Ask which installation method to use
echo -e "${CYAN}Choose divine installation method:${NC}"
echo "1) Via Helm (recommended)"
echo "2) Via Kubernetes manifests"
read -p "Enter your choice (1/2): " install_choice

case $install_choice in
    1)
        echo -e "${PURPLE}Installing ArgoCD via Helm...${NC}"
        
        # Add ArgoCD Helm repository
        helm repo add argo https://argoproj.github.io/argo-helm
        helm repo update
        
        # Install ArgoCD
        helm install argocd argo/argo-cd \
          --namespace argocd \
          --set server.extraArgs="{--insecure}" \
          --values - <<EOF
server:
  extraArgs:
    - --insecure
  config:
    repositories: |
      - type: git
        url: https://github.com/fsiqueira/omega-btc-ai.git
        name: omega-btc-ai
    resource.customizations: |
      networking.k8s.io/Ingress:
        health.lua: |
          hs = {}
          hs.status = "Healthy"
          return hs
  ingress:
    enabled: true
    annotations:
      kubernetes.io/ingress.class: nginx
      nginx.ingress.kubernetes.io/ssl-redirect: "false"
      nginx.ingress.kubernetes.io/force-ssl-redirect: "false"
    hosts:
      - argocd.omega.local
  metrics:
    enabled: true
    serviceMonitor:
      enabled: true
  rbacConfig:
    policy.default: role:readonly
repoServer:
  resources:
    limits:
      cpu: 200m
      memory: 256Mi
    requests:
      cpu: 100m
      memory: 128Mi
applicationSet:
  enabled: true
notifications:
  enabled: true
EOF
        ;;
    2)
        echo -e "${PURPLE}Installing ArgoCD via manifests...${NC}"
        
        # Install ArgoCD
        kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
        
        # Configure ArgoCD server to run in insecure mode (for ease of access)
        kubectl patch deployment argocd-server -n argocd -p '{"spec": {"template": {"spec": {"containers": [{"name": "argocd-server","command": ["argocd-server","--insecure"]}]}}}}'
        ;;
    *)
        echo -e "${RED}Invalid choice. Exiting.${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}✓ Divine orchestrator installed!${NC}"

# Wait for ArgoCD server to be ready
echo -e "\n${BLUE}WAITING FOR THE DIVINE ORCHESTRATOR TO AWAKEN...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
echo -e "${GREEN}✓ Divine orchestrator is awakened!${NC}"

# Set up port-forwarding for easy access
echo -e "\n${BLUE}SETTING UP DIVINE CHANNEL (PORT-FORWARDING)...${NC}"
echo "To access the ArgoCD UI, run the following command in a separate terminal:"
echo -e "${YELLOW}kubectl port-forward svc/argocd-server -n argocd 8080:443${NC}"
echo -e "Then navigate to ${CYAN}https://localhost:8080${NC} in your browser."

# Get the initial admin password
echo -e "\n${BLUE}RETRIEVING THE SACRED PASSWORD...${NC}"
echo -e "The initial admin password is:"
echo -e "${YELLOW}kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d${NC}"

# Install App of Apps
echo -e "\n${BLUE}WOULD YOU LIKE TO INSTALL THE DIVINE APP OF APPS?${NC}"
read -p "Install App of Apps? (y/n): " install_app_of_apps

if [[ $install_app_of_apps == "y" || $install_app_of_apps == "Y" ]]; then
    echo -e "${PURPLE}Creating the Divine App of Apps...${NC}"
    
    # Create the App of Apps application
    kubectl apply -f - <<EOF
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: omega-divine-grid
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/fsiqueira/omega-btc-ai.git
    targetRevision: HEAD
    path: kubernetes/gitops/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
EOF
    
    echo -e "${GREEN}✓ Divine App of Apps installed!${NC}"
else
    echo -e "${CYAN}Skipping App of Apps installation.${NC}"
fi

# Apply custom RBAC if needed
echo -e "\n${BLUE}WOULD YOU LIKE TO APPLY DIVINE RBAC CONFIGURATION?${NC}"
read -p "Apply custom RBAC? (y/n): " apply_rbac

if [[ $apply_rbac == "y" || $apply_rbac == "Y" ]]; then
    echo -e "${PURPLE}Applying Divine RBAC Configuration...${NC}"
    
    # Apply RBAC ConfigMap
    kubectl apply -f ../gitops/rbac/argocd-rbac-cm.yaml
    
    # Apply user bindings
    kubectl apply -f ../gitops/rbac/argocd-rbac-user-binding.yaml
    
    echo -e "${GREEN}✓ Divine RBAC configuration applied!${NC}"
else
    echo -e "${CYAN}Skipping RBAC configuration.${NC}"
fi

# Divine blessing
echo -e "\n${YELLOW}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${YELLOW}║                    DIVINE INSTALLATION COMPLETE                ║${NC}"
echo -e "${YELLOW}╚═══════════════════════════════════════════════════════════════╝${NC}"

echo -e "\n${PURPLE}May your repositories always remain in sync with your clusters.${NC}"
echo -e "${PURPLE}May your deployments be blessed with zero downtime.${NC}"
echo -e "${PURPLE}May your configurations remain immutable and your state declarative.${NC}"
echo -e "${PURPLE}JAH JAH bless your GitOps journey!${NC}"

echo -e "\n${CYAN}Next steps:${NC}"
echo -e "1. Access the ArgoCD UI using port-forwarding"
echo -e "2. Log in with username 'admin' and the sacred password from above"
echo -e "3. Connect your git repositories"
echo -e "4. Create applications or use the App of Apps pattern"
echo -e "5. Manifest your divine infrastructure" 