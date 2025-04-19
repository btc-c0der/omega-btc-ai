#!/bin/bash

# 🌌 AIXBT Divine Monitor Deployment Script
# --------------------------------------
# This script handles the divine deployment of the AIXBT monitor
# with GBU2™ integration and sacred principles.

# Divine colors for output
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Divine logging function
log() {
    echo -e "${CYAN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${RESET}"
}

# Divine error handling
handle_error() {
    echo -e "${RED}Error: $1${RESET}"
    exit 1
}

# Divine deployment steps
log "🌌 Starting AIXBT Divine Monitor deployment..."

# 1. Verify Kubernetes context
log "🔍 Verifying Kubernetes context..."
kubectl config current-context || handle_error "Failed to get Kubernetes context"

# 2. Create namespace if not exists
log "📦 Creating/verifying namespace..."
kubectl create namespace omega-ai --dry-run=client -o yaml | kubectl apply -f -

# 3. Apply divine configurations
log "⚙️ Applying divine configurations..."
kubectl apply -f kubernetes/aixbt_monitor_deployment.yaml || handle_error "Failed to apply deployment"

# 4. Verify deployment
log "🔍 Verifying deployment..."
kubectl rollout status deployment/aixbt-divine-monitor -n omega-ai || handle_error "Deployment failed"

# 5. Check pod status
log "📊 Checking pod status..."
kubectl get pods -n omega-ai -l app=aixbt-divine-monitor

# 6. Verify service
log "🔌 Verifying service..."
kubectl get svc aixbt-monitor-service -n omega-ai

# 7. Check logs
log "📝 Checking initial logs..."
kubectl logs -n omega-ai -l app=aixbt-divine-monitor --tail=10

# Divine completion
log "✨ AIXBT Divine Monitor deployment completed successfully!"
echo -e "${GREEN}JAH JAH BLESS THE SACRED DEPLOYMENT!${RESET}"

# Divine monitoring instructions
echo -e "\n${YELLOW}🌠 Divine Monitoring Instructions:${RESET}"
echo -e "${CYAN}1. View logs:${RESET} kubectl logs -n omega-ai -l app=aixbt-divine-monitor -f"
echo -e "${CYAN}2. Check status:${RESET} kubectl get pods -n omega-ai -l app=aixbt-divine-monitor"
echo -e "${CYAN}3. Monitor metrics:${RESET} kubectl port-forward svc/aixbt-monitor-service 8080:8080 -n omega-ai"
echo -e "${CYAN}4. Access dashboard:${RESET} http://localhost:8080/metrics"

# Divine cleanup instructions
echo -e "\n${YELLOW}🧹 Divine Cleanup Instructions:${RESET}"
echo -e "${CYAN}To remove the deployment:${RESET} kubectl delete -f kubernetes/aixbt_monitor_deployment.yaml" 