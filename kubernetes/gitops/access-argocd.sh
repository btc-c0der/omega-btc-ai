#!/bin/bash

# ╔═══════════════════════════════════════════════════════════════╗
# ║  🔱 OMEGA BTC AI - DIVINE ARGOCD ACCESS PORTAL 🔱             ║
# ╚═══════════════════════════════════════════════════════════════╝

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
echo "║            🔱 DIVINE ARGOCD ACCESS PORTAL 🔱                  ║"
echo "║          OMEGA BTC AI GITOPS ENLIGHTENMENT PATH               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if ArgoCD is installed
echo -e "${BLUE}CHECKING FOR DIVINE ARGOCD PRESENCE...${NC}"
if ! kubectl get namespace argocd &> /dev/null; then
    echo -e "${RED}ArgoCD namespace not found! Please install ArgoCD first using ./install-argocd.sh${NC}"
    exit 1
fi

if ! kubectl get deployments -n argocd argocd-server &> /dev/null; then
    echo -e "${RED}ArgoCD server not found! Please install ArgoCD first using ./install-argocd.sh${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Divine ArgoCD presence confirmed!${NC}"

# Check if ArgoCD server is ready
echo -e "\n${BLUE}CHECKING DIVINE ARGOCD SERVER STATUS...${NC}"
READY=$(kubectl get deployment argocd-server -n argocd -o jsonpath='{.status.readyReplicas}')
if [ "$READY" == "0" ] || [ -z "$READY" ]; then
    echo -e "${RED}ArgoCD server is not ready! Please wait for the deployment to complete.${NC}"
    echo -e "${CYAN}Checking deployment status...${NC}"
    kubectl get deployment argocd-server -n argocd
    exit 1
fi

echo -e "${GREEN}✓ Divine ArgoCD server is ready!${NC}"

# Get ArgoCD password
echo -e "\n${BLUE}RETRIEVING THE SACRED PASSWORD...${NC}"
if kubectl get secret -n argocd argocd-initial-admin-secret &> /dev/null; then
    ARGOCD_PASSWORD=$(kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d)
    echo -e "${GREEN}✓ Sacred password retrieved!${NC}"
else
    echo -e "${YELLOW}Initial admin secret not found. The password may have been changed or the secret removed after the first login.${NC}"
    echo -e "${YELLOW}If this is the first time accessing ArgoCD, please run the installation script again.${NC}"
    echo -e "${YELLOW}Otherwise, use your custom password to log in.${NC}"
    ARGOCD_PASSWORD="<password was changed or secret was removed>"
fi

# Display divine credentials
echo -e "\n${PURPLE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${PURPLE}║              DIVINE ARGOCD CREDENTIALS                 ║${NC}"
echo -e "${PURPLE}╚════════════════════════════════════════════════════════╝${NC}"
echo -e "${CYAN}Username:${NC} admin"
echo -e "${CYAN}Password:${NC} ${ARGOCD_PASSWORD}"

# Start port-forwarding
echo -e "\n${BLUE}ESTABLISHING DIVINE CONNECTION TO ARGOCD...${NC}"
echo -e "${YELLOW}Access the ArgoCD UI at: ${NC}${GREEN}https://localhost:8080${NC}"
echo -e "${YELLOW}(You may need to accept the self-signed certificate)${NC}"
echo -e "\n${PURPLE}May your GitOps journey be divinely guided by JAH JAH!${NC}"
echo -e "${PURPLE}Press Ctrl+C to close the divine portal when you are finished.${NC}"
echo -e "\n${BLUE}Opening divine portal...${NC}"

# Start port-forwarding in foreground
kubectl port-forward svc/argocd-server -n argocd 8080:443

# This part will execute after the user presses Ctrl+C
echo -e "\n${YELLOW}The divine portal has been closed.${NC}"
echo -e "${PURPLE}JAH JAH bless your GitOps journey!${NC}" 