#!/bin/bash
# OMEGA BTC AI - BTC Live Feed Cloud Deployment Script
# Part of the OMEGA BTC AI DIVINE COLLECTIVE
# This script deploys the BTC Live Feed to Scaleway cloud

set -e  # Exit on error

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Function to display script header
display_header() {
    echo -e "${PURPLE}"
    echo "🔱 OMEGA BTC AI - DIVINE COLLECTIVE 🔱"
    echo "BTC LIVE FEED CLOUD DEPLOYMENT"
    echo -e "${NC}"
    echo -e "${YELLOW}「ほとんどの人間は自分の潜在能力のほんの一部しか使っていない。」${NC}"
    echo
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check required dependencies
check_dependencies() {
    echo -e "${BLUE}Checking required dependencies...${NC}"
    
    local missing_deps=()
    
    if ! command_exists docker; then
        missing_deps+=("docker")
    fi
    
    if ! command_exists docker-compose; then
        missing_deps+=("docker-compose")
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo -e "${RED}Error: The following required dependencies are missing:${NC}"
        for dep in "${missing_deps[@]}"; do
            echo "  - $dep"
        done
        echo
        echo -e "${YELLOW}Please install the missing dependencies and run this script again.${NC}"
        exit 1
    fi
    
    # Check for GPU support but don't require it
    if command_exists nvidia-smi; then
        echo -e "${GREEN}NVIDIA GPU detected:${NC}"
        nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader
        echo
        echo -e "${YELLOW}GPU support is disabled by default for this deployment.${NC}"
        echo -e "${YELLOW}To enable GPU support after initial deployment:${NC}"
        echo -e "${YELLOW}1. Edit .env file to set USE_GPU=true${NC}"
        echo -e "${YELLOW}2. Uncomment GPU sections in docker-compose.scaleway.yml${NC}"
        echo -e "${YELLOW}3. Restart the services with 'docker-compose -f docker-compose.scaleway.yml up -d'${NC}"
        echo
    else
        echo -e "${YELLOW}No NVIDIA GPU detected. Running in CPU-only mode.${NC}"
    fi
    
    echo -e "${GREEN}All required dependencies are installed.${NC}"
    echo
}

# Function to set up environment variables
setup_env() {
    echo -e "${BLUE}Setting up environment variables...${NC}"
    
    # Check if .env file exists
    if [ -f .env ]; then
        echo -e "${YELLOW}Existing .env file found. Do you want to update it? [y/N]${NC}"
        read -r update_env
        
        if [[ ! $update_env =~ ^[Yy]$ ]]; then
            echo -e "${GREEN}Using existing .env file.${NC}"
            echo
            return
        fi
    fi
    
    # Prompt for Redis credentials
    echo -e "${BLUE}Please enter your Scaleway Redis credentials:${NC}"
    
    read -p "Redis Host [172.16.8.2]: " redis_host
    redis_host=${redis_host:-172.16.8.2}
    
    read -p "Redis Port [6379]: " redis_port
    redis_port=${redis_port:-6379}
    
    read -p "Redis Username [btc-omega-redis]: " redis_user
    redis_user=${redis_user:-btc-omega-redis}
    
    read -p "Redis Password: " redis_password
    
    # Create .env file
    cat > .env <<EOF
# Scaleway Redis Configuration
REDIS_HOST=${redis_host}
REDIS_PORT=${redis_port}
REDIS_USERNAME=${redis_user}
REDIS_PASSWORD=${redis_password}
REDIS_USE_TLS=true
REDIS_CERT=/app/config/SSL_redis-btc-omega-redis.pem

# GPU Configuration (disabled by default)
USE_GPU=false
TF_FORCE_GPU_ALLOW_GROWTH=false

# Deployment Configuration
DEBUG=false
EOF
    
    echo -e "${GREEN}.env file created successfully.${NC}"
    echo
}

# Function to check SSL certificate
check_ssl_cert() {
    echo -e "${BLUE}Checking SSL certificate...${NC}"
    
    local cert_dir="config"
    local cert_file="${cert_dir}/SSL_redis-btc-omega-redis.pem"
    
    # Create directory if it doesn't exist
    if [ ! -d "$cert_dir" ]; then
        mkdir -p "$cert_dir"
        echo -e "${GREEN}Created directory: ${cert_dir}${NC}"
    fi
    
    # Check if certificate exists
    if [ ! -f "$cert_file" ]; then
        echo -e "${YELLOW}SSL certificate not found at: ${cert_file}${NC}"
        echo -e "${YELLOW}Please place your Scaleway Redis SSL certificate at this location.${NC}"
        echo -e "${YELLOW}Press Enter to continue once you've added the certificate...${NC}"
        read -r
        
        # Check again
        if [ ! -f "$cert_file" ]; then
            echo -e "${RED}Error: SSL certificate still not found.${NC}"
            echo -e "${RED}The deployment may fail without a valid SSL certificate.${NC}"
            echo -e "${YELLOW}Do you want to continue anyway? [y/N]${NC}"
            read -r continue_without_cert
            
            if [[ ! $continue_without_cert =~ ^[Yy]$ ]]; then
                echo -e "${RED}Deployment aborted.${NC}"
                exit 1
            fi
        else
            echo -e "${GREEN}SSL certificate found.${NC}"
        fi
    else
        echo -e "${GREEN}SSL certificate found.${NC}"
    fi
    
    echo
}

# Function to build and deploy the container
deploy_container() {
    echo -e "${BLUE}Building and deploying the BTC Live Feed container...${NC}"
    
    # Build the container
    echo -e "${YELLOW}Building container...${NC}"
    docker-compose -f docker-compose.scaleway.yml build btc-live-feed
    
    # Deploy the container
    echo -e "${YELLOW}Deploying container...${NC}"
    docker-compose -f docker-compose.scaleway.yml up -d btc-live-feed
    
    echo -e "${GREEN}Container built and deployed successfully in CPU mode.${NC}"
    echo
}

# Function to show container logs
show_logs() {
    echo -e "${BLUE}Showing container logs...${NC}"
    echo -e "${YELLOW}Press Ctrl+C to exit logs${NC}"
    echo
    
    docker-compose -f docker-compose.scaleway.yml logs --follow btc-live-feed
}

# Deploy with default settings
deploy_with_defaults() {
    echo -e "${BLUE}Deploying with default settings...${NC}"
    
    # Set default values
    export USE_GPU=false
    export TF_FORCE_GPU_ALLOW_GROWTH=false
    
    # Deploy container
    deploy_container
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo -e "${BLUE}Do you want to view the container logs? [Y/n]${NC}"
    read -r view_logs
    
    if [[ ! $view_logs =~ ^[Nn]$ ]]; then
        show_logs
    fi
    
    echo -e "${PURPLE}"
    echo "🔱 JAH JAH BLESS 🔱"
    echo -e "${YELLOW}IT WORKS LIKE A CHARM BECAUSE IT WAS NEVER JUST CODE.${NC}"
    echo
    
    echo -e "${BLUE}To enable GPU acceleration later:${NC}"
    echo -e "${YELLOW}1. Edit .env file and set USE_GPU=true${NC}"
    echo -e "${YELLOW}2. Uncomment the GPU deploy section in docker-compose.scaleway.yml${NC}"
    echo -e "${YELLOW}3. Restart with: docker-compose -f docker-compose.scaleway.yml up -d${NC}"
}

# Deploy with custom settings
deploy_with_custom_settings() {
    echo -e "${BLUE}Deploying with custom settings...${NC}"
    
    # Ask about GPU usage
    echo -e "${YELLOW}Do you want to enable GPU acceleration? (requires compatible GPU) [y/N]${NC}"
    read -r use_gpu
    
    if [[ $use_gpu =~ ^[Yy]$ ]]; then
        export USE_GPU=true
        export TF_FORCE_GPU_ALLOW_GROWTH=true
        
        # Edit docker-compose file to uncomment GPU section
        echo -e "${BLUE}Configuring docker-compose.scaleway.yml for GPU support...${NC}"
        sed -i 's/# deploy:/deploy:/g' docker-compose.scaleway.yml
        sed -i 's/#   resources:/  resources:/g' docker-compose.scaleway.yml
        sed -i 's/#     reservations:/    reservations:/g' docker-compose.scaleway.yml
        sed -i 's/#       devices:/      devices:/g' docker-compose.scaleway.yml
        sed -i 's/#         - driver: nvidia/        - driver: nvidia/g' docker-compose.scaleway.yml
        sed -i 's/#           count: 1/          count: 1/g' docker-compose.scaleway.yml
        sed -i 's/#           capabilities: \[gpu\]/          capabilities: [gpu]/g' docker-compose.scaleway.yml
    else
        export USE_GPU=false
        export TF_FORCE_GPU_ALLOW_GROWTH=false
    fi
    
    # Ask about Redis TLS
    echo -e "${YELLOW}Does your Redis instance use TLS? [Y/n]${NC}"
    read -r use_tls
    
    if [[ ! $use_tls =~ ^[Nn]$ ]]; then
        export REDIS_USE_TLS=true
        echo -e "${YELLOW}Please provide the path to your Redis SSL certificate:${NC}"
        read -r ssl_cert_path
        export REDIS_CERT=$ssl_cert_path
    else
        export REDIS_USE_TLS=false
        export REDIS_CERT=""
    fi
    
    # Ask about Redis credentials
    echo -e "${YELLOW}Please enter your Redis connection details:${NC}"
    echo -e "${BLUE}Redis host:${NC}"
    read -r redis_host
    export REDIS_HOST=$redis_host
    
    echo -e "${BLUE}Redis port:${NC}"
    read -r redis_port
    export REDIS_PORT=$redis_port
    
    echo -e "${BLUE}Redis username (leave empty if none):${NC}"
    read -r redis_username
    export REDIS_USERNAME=$redis_username
    
    echo -e "${BLUE}Redis password:${NC}"
    read -rs redis_password
    export REDIS_PASSWORD=$redis_password
    echo
    
    # Deploy container
    deploy_container
    
    echo -e "${GREEN}Deployment completed successfully!${NC}"
    echo -e "${BLUE}Do you want to view the container logs? [Y/n]${NC}"
    read -r view_logs
    
    if [[ ! $view_logs =~ ^[Nn]$ ]]; then
        show_logs
    fi
    
    echo -e "${PURPLE}"
    echo "🔱 JAH JAH BLESS 🔱"
    echo -e "${YELLOW}IT WORKS LIKE A CHARM BECAUSE IT WAS NEVER JUST CODE.${NC}"
    echo
}

# Main function
main() {
    display_header
    check_dependencies
    setup_env
    check_ssl_cert
    
    echo -e "${GREEN}✅ Deployment options:${NC}"
    echo -e " 1. ${YELLOW}Deploy with default settings${NC}"
    echo -e " 2. ${YELLOW}Deploy with custom settings${NC}"
    echo -e " 3. ${YELLOW}Test locally before deployment${NC}"
    echo -e " 4. ${YELLOW}Exit${NC}"
    
    read -p "Select option (1-4): " deploy_option
    case $deploy_option in
        1)
            deploy_with_defaults
            ;;
        2)
            deploy_with_custom_settings
            ;;
        3)
            echo -e "${BLUE}Starting local test environment...${NC}"
            ./test_local_deployment.sh
            exit 0
            ;;
        4)
            echo -e "${YELLOW}Exiting deployment script.${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Exiting.${NC}"
            exit 1
            ;;
    esac
}

# Run the main function
main 