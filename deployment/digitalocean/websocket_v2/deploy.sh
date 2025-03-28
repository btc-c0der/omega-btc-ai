#!/bin/bash

# 🔱 OMEGA BTC AI - WebSocket V2 Deployment Script
# 📜 GPU²: General Public Universal + Graphics Processing Unison
# 🔐 Divine Copyright (c) 2025 - OMEGA Collective

# Colors for divine output
PURPLE='\033[95m'
BLUE='\033[94m'
CYAN='\033[96m'
GREEN='\033[92m'
WARNING='\033[93m'
FAIL='\033[91m'
ENDC='\033[0m'
BOLD='\033[1m'
UNDERLINE='\033[4m'

# Divine functions
print_header() {
    echo -e "${PURPLE}🔱 OMEGA BTC AI - WebSocket V2 Deployment${ENDC}"
    echo -e "${BLUE}==========================================${ENDC}"
}

print_step() {
    echo -e "${CYAN}Step $1: $2${ENDC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${ENDC}"
}

print_warning() {
    echo -e "${WARNING}⚠ $1${ENDC}"
}

print_error() {
    echo -e "${FAIL}✗ $1${ENDC}"
}

# Check divine prerequisites
check_prerequisites() {
    print_step "1" "Checking divine prerequisites..."
    
    # Check doctl installation
    if ! command -v doctl &> /dev/null; then
        print_error "doctl is not installed. Please install it first:"
        echo "brew install doctl  # macOS"
        echo "snap install doctl  # Linux"
        echo "scoop install doctl  # Windows"
        exit 1
    fi
    
    # Check authentication
    if ! doctl account get &> /dev/null; then
        print_error "Not authenticated with Digital Ocean. Please run:"
        echo "doctl auth init"
        exit 1
    fi
    
    print_success "All prerequisites met"
}

# Deploy the divine app
deploy_app() {
    print_step "2" "Deploying divine WebSocket V2 server..."
    
    # Get the app ID if it exists
    APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "omega-btc-websocket-v2" | awk '{print $1}')
    
    if [ -z "$APP_ID" ]; then
        # Create new app
        print_success "Creating new divine app..."
        doctl apps create --spec app.yaml
    else
        # Update existing app
        print_success "Updating divine app $APP_ID..."
        doctl apps update $APP_ID --spec app.yaml
    fi
    
    print_success "Deployment initiated"
}

# Monitor divine deployment
monitor_deployment() {
    print_step "3" "Monitoring divine deployment..."
    
    # Get the app ID
    APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "omega-btc-websocket-v2" | awk '{print $1}')
    
    if [ -z "$APP_ID" ]; then
        print_error "Could not find divine app ID"
        exit 1
    fi
    
    # Monitor deployment status
    echo -e "${CYAN}Watching divine deployment status...${ENDC}"
    doctl apps watch $APP_ID
    
    # Get the app URL
    APP_URL=$(doctl apps get $APP_ID --format Ingress.Status.Endpoint --no-header)
    print_success "Divine app deployed at: $APP_URL"
}

# Test divine health
test_health() {
    print_step "4" "Testing divine health..."
    
    # Get the app URL
    APP_URL=$(doctl apps list --format Ingress.Status.Endpoint,Spec.Name --no-header | grep "omega-btc-websocket-v2" | awk '{print $1}')
    
    if [ -z "$APP_URL" ]; then
        print_error "Could not find divine app URL"
        exit 1
    fi
    
    # Test health endpoint
    HEALTH_CHECK=$(curl -s "$APP_URL/health")
    if [[ $HEALTH_CHECK == *"healthy"* ]]; then
        print_success "Divine health check passed"
    else
        print_error "Divine health check failed"
        echo "Response: $HEALTH_CHECK"
        exit 1
    fi
}

# Main divine execution
main() {
    print_header
    
    check_prerequisites
    deploy_app
    monitor_deployment
    test_health
    
    echo -e "\n${GREEN}🔱 Divine deployment completed successfully!${ENDC}"
    echo -e "${BLUE}May your WebSocket connections be blessed with stability and divine performance.${ENDC}"
}

# Execute divine script
main 