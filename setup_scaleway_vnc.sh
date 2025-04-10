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

# 
# OMEGA BTC AI - VNC Portal Scaleway Deployment
# ============================================
#
# Setup script for deploying the OMEGA VNC Portal on Scaleway
#
# Copyright (C) 2024 OMEGA BTC AI Team
# License: GNU General Public License v3.0
#
# JAH BLESS the eternal flow of cloud VNC vision.

# Colors for formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
RESET='\033[0m'
BOLD='\033[1m'

# Default configuration
MAC_VNC_IP="127.0.0.1"
VNC_PORT=5900
WEB_PORT=6080
CONTAINER_NAME="omega-novnc"
DOMAIN_NAME=""
USE_SSL=false
AUTO_RENEW_SSL=true

# Display the header
show_header() {
    echo -e "\n${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}${BOLD}     OMEGA VNC PORTAL - SCALEWAY DEPLOYMENT SETUP      ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${CYAN}Setting up remote access to the OMEGA GRID${RESET}"
    echo -e "${YELLOW}JAH JAH BLESS THE REMOTE VISION!${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}\n"
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --mac-ip)
                MAC_VNC_IP="$2"
                shift 2
                ;;
            --vnc-port)
                VNC_PORT="$2"
                shift 2
                ;;
            --web-port)
                WEB_PORT="$2"
                shift 2
                ;;
            --container)
                CONTAINER_NAME="$2"
                shift 2
                ;;
            --domain)
                DOMAIN_NAME="$2"
                USE_SSL=true
                shift 2
                ;;
            --no-ssl)
                USE_SSL=false
                shift
                ;;
            --no-auto-renew)
                AUTO_RENEW_SSL=false
                shift
                ;;
            *)
                echo -e "${RED}Unknown option: $1${RESET}"
                exit 1
                ;;
        esac
    done
}

# Check if running on a Scaleway instance
check_scaleway() {
    echo -e "${CYAN}Checking if running on a Scaleway instance...${RESET}"
    
    # Try to access Scaleway metadata
    if curl -s --connect-timeout 3 http://169.254.42.42/conf > /dev/null; then
        echo -e "${GREEN}✓ Running on a Scaleway instance${RESET}"
        return 0
    else
        echo -e "${YELLOW}⚠ Not running on a Scaleway instance or metadata service unavailable${RESET}"
        echo -e "${YELLOW}⚠ Continuing anyway, but some Scaleway-specific features may not work${RESET}"
        return 1
    fi
}

# Check and install required dependencies
install_dependencies() {
    echo -e "${CYAN}Checking and installing required dependencies...${RESET}"
    
    # Update package lists
    apt-get update
    
    # Install Docker if not already installed
    if ! command -v docker &> /dev/null; then
        echo -e "${YELLOW}Installing Docker...${RESET}"
        apt-get install -y apt-transport-https ca-certificates curl software-properties-common
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
        add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
        apt-get update
        apt-get install -y docker-ce
        systemctl enable docker
    else
        echo -e "${GREEN}✓ Docker already installed${RESET}"
    fi
    
    # Install Python if not already installed
    if ! command -v python3 &> /dev/null; then
        echo -e "${YELLOW}Installing Python 3...${RESET}"
        apt-get install -y python3 python3-pip
    else
        echo -e "${GREEN}✓ Python 3 already installed${RESET}"
    fi
    
    # Install other required tools
    echo -e "${YELLOW}Installing additional tools...${RESET}"
    apt-get install -y ufw certbot nginx
    
    echo -e "${GREEN}✓ All dependencies installed${RESET}"
}

# Configure firewall
configure_firewall() {
    echo -e "${CYAN}Configuring firewall...${RESET}"
    
    # Check if UFW is installed
    if ! command -v ufw &> /dev/null; then
        echo -e "${YELLOW}Installing UFW...${RESET}"
        apt-get install -y ufw
    fi
    
    # Configure UFW
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow $WEB_PORT/tcp
    
    if [ "$USE_SSL" = true ]; then
        ufw allow 80/tcp
        ufw allow 443/tcp
    fi
    
    # Enable UFW if not already enabled
    if ! ufw status | grep -q "Status: active"; then
        echo -e "${YELLOW}Enabling UFW...${RESET}"
        echo "y" | ufw enable
    fi
    
    echo -e "${GREEN}✓ Firewall configured${RESET}"
}

# Set up Nginx as a reverse proxy with SSL if requested
setup_nginx() {
    if [ "$USE_SSL" = true ] && [ ! -z "$DOMAIN_NAME" ]; then
        echo -e "${CYAN}Setting up Nginx as a reverse proxy with SSL for $DOMAIN_NAME...${RESET}"
        
        # Install Nginx and Certbot if not already installed
        if ! command -v nginx &> /dev/null || ! command -v certbot &> /dev/null; then
            apt-get install -y nginx certbot python3-certbot-nginx
        fi
        
        # Create Nginx configuration
        cat > /etc/nginx/sites-available/omega-vnc << EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;
    
    location / {
        proxy_pass http://localhost:$WEB_PORT;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
        
        # Enable the site
        ln -sf /etc/nginx/sites-available/omega-vnc /etc/nginx/sites-enabled/
        
        # Test and reload Nginx
        nginx -t && systemctl reload nginx
        
        # Obtain SSL certificate
        echo -e "${YELLOW}Obtaining SSL certificate for $DOMAIN_NAME...${RESET}"
        certbot --nginx -d $DOMAIN_NAME --non-interactive --agree-tos --email admin@$DOMAIN_NAME
        
        # Set up auto-renewal if requested
        if [ "$AUTO_RENEW_SSL" = true ]; then
            echo -e "${YELLOW}Setting up automatic SSL renewal...${RESET}"
            
            # Check if a cron job already exists
            if ! crontab -l | grep -q "certbot renew"; then
                (crontab -l 2>/dev/null; echo "0 3 * * * certbot renew --quiet") | crontab -
            fi
        fi
        
        echo -e "${GREEN}✓ Nginx configured with SSL for $DOMAIN_NAME${RESET}"
    elif [ "$USE_SSL" = false ]; then
        echo -e "${YELLOW}Skipping Nginx setup as SSL is not requested${RESET}"
    else
        echo -e "${RED}Cannot set up SSL without a domain name${RESET}"
    fi
}

# Deploy the VNC portal
deploy_vnc_portal() {
    echo -e "${CYAN}Deploying OMEGA VNC Portal...${RESET}"
    
    # Pull the Docker image
    echo -e "${YELLOW}Pulling Docker image...${RESET}"
    docker pull dorowu/ubuntu-desktop-lxde-vnc
    
    # Stop and remove existing container if it exists
    if docker ps -a | grep -q "$CONTAINER_NAME"; then
        echo -e "${YELLOW}Stopping and removing existing container...${RESET}"
        docker rm -f "$CONTAINER_NAME"
    fi
    
    # Start the container
    echo -e "${YELLOW}Starting container...${RESET}"
    docker run -d \
        --name "$CONTAINER_NAME" \
        --restart unless-stopped \
        -p "$WEB_PORT:80" \
        -e "VNC_SERVER=$MAC_VNC_IP:$VNC_PORT" \
        dorowu/ubuntu-desktop-lxde-vnc
    
    # Check if container started successfully
    if docker ps | grep -q "$CONTAINER_NAME"; then
        echo -e "${GREEN}✓ OMEGA VNC Portal deployed successfully${RESET}"
    else
        echo -e "${RED}Failed to deploy OMEGA VNC Portal${RESET}"
        docker logs "$CONTAINER_NAME"
        exit 1
    fi
}

# Create a convenient startup script
create_control_script() {
    echo -e "${CYAN}Creating control script...${RESET}"
    
    cat > /usr/local/bin/omega-vnc << EOF
#!/bin/bash
# OMEGA VNC Portal Control Script

case "\$1" in
    start)
        docker start $CONTAINER_NAME
        echo "OMEGA VNC Portal started"
        ;;
    stop)
        docker stop $CONTAINER_NAME
        echo "OMEGA VNC Portal stopped"
        ;;
    restart)
        docker restart $CONTAINER_NAME
        echo "OMEGA VNC Portal restarted"
        ;;
    status)
        if docker ps | grep -q "$CONTAINER_NAME"; then
            echo "OMEGA VNC Portal is running"
        else
            echo "OMEGA VNC Portal is not running"
        fi
        ;;
    logs)
        docker logs $CONTAINER_NAME
        ;;
    *)
        echo "Usage: omega-vnc {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
EOF
    
    chmod +x /usr/local/bin/omega-vnc
    echo -e "${GREEN}✓ Control script created at /usr/local/bin/omega-vnc${RESET}"
    echo -e "${YELLOW}  Usage: omega-vnc {start|stop|restart|status|logs}${RESET}"
}

# Display summary information
show_summary() {
    echo -e "\n${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${GREEN}${BOLD}         OMEGA VNC PORTAL DEPLOYMENT COMPLETE          ${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${CYAN}VNC Connection:${RESET} $MAC_VNC_IP:$VNC_PORT"
    
    if [ "$USE_SSL" = true ] && [ ! -z "$DOMAIN_NAME" ]; then
        echo -e "${CYAN}Access URL:${RESET} https://$DOMAIN_NAME"
    else
        PUBLIC_IP=$(curl -s ifconfig.me)
        echo -e "${CYAN}Access URL:${RESET} http://$PUBLIC_IP:$WEB_PORT/vnc.html"
    fi
    
    echo -e "${CYAN}Control Script:${RESET} omega-vnc {start|stop|restart|status|logs}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}"
    echo -e "${YELLOW}JAH JAH BLESS THE REMOTE VISION!${RESET}"
    echo -e "${YELLOW}${BOLD}=======================================================${RESET}\n"
}

# Main function
main() {
    show_header
    parse_args "$@"
    
    # Check if running as root
    if [ "$(id -u)" -ne 0 ]; then
        echo -e "${RED}This script must be run as root${RESET}"
        exit 1
    fi
    
    check_scaleway
    install_dependencies
    configure_firewall
    setup_nginx
    deploy_vnc_portal
    create_control_script
    show_summary
}

# Execute main function with all arguments
main "$@" 