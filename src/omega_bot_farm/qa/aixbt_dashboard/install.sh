#!/bin/bash
#
# AIXBT Dashboard Installation Script
# ----------------------------------
#
# This script sets up the AIXBT Dashboard with real-time price feed
# on an Ubuntu server, configuring Nginx as a reverse proxy.

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../../../.." && pwd )"

# Configuration variables
PYTHON_VERSION="3.9"
DOMAIN="aixbt.omegaven.xyz"
PORT=8055
USE_TESTNET="true"  # Set to "false" for mainnet

echo -e "${BLUE}=== AIXBT Dashboard Installation ===${NC}"
echo "Project root: $PROJECT_ROOT"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo -e "${RED}Please run as root${NC}"
  exit 1
fi

echo -e "${BLUE}=== Installing dependencies ===${NC}"
apt-get update
apt-get install -y python3-pip python3-venv nginx certbot python3-certbot-nginx

# Create virtual environment if it doesn't exist
echo -e "${BLUE}=== Setting up Python environment ===${NC}"
if [ ! -d "$PROJECT_ROOT/venv" ]; then
  python$PYTHON_VERSION -m venv "$PROJECT_ROOT/venv"
fi

# Activate virtual environment and install dependencies
source "$PROJECT_ROOT/venv/bin/activate"
pip install --upgrade pip
pip install -r "$PROJECT_ROOT/src/omega_bot_farm/requirements.txt"
pip install gunicorn ccxt dash dash-bootstrap-components

# Create directory for config files if it doesn't exist
echo -e "${BLUE}=== Setting up configuration ===${NC}"
mkdir -p /etc/nixbt

# Copy configuration files
cp "$SCRIPT_DIR/nginx/aixbt.conf" /etc/nginx/sites-available/aixbt.conf

# Enable site
ln -sf /etc/nginx/sites-available/aixbt.conf /etc/nginx/sites-enabled/

# Check Nginx configuration
nginx -t

# Setup SSL certificate if needed
echo -e "${BLUE}=== Setting up SSL certificate ===${NC}"
if [ ! -d "/etc/letsencrypt/live/$DOMAIN" ]; then
  certbot --nginx -d $DOMAIN
fi

# Setup systemd service
echo -e "${BLUE}=== Setting up systemd service ===${NC}"
cp "$SCRIPT_DIR/systemd/aixbt-dashboard.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable aixbt-dashboard

# Set appropriate permissions
chown -R ubuntu:ubuntu "$PROJECT_ROOT"

# Create .env file if it doesn't exist
if [ ! -f "$PROJECT_ROOT/.env" ]; then
  echo -e "${YELLOW}Creating .env file${NC}"
  cat > "$PROJECT_ROOT/.env" << EOF
# AIXBT Dashboard Environment Variables
BITGET_API_KEY=""
BITGET_SECRET_KEY=""
BITGET_PASSPHRASE=""
USE_TESTNET=$USE_TESTNET
EOF
  echo -e "${YELLOW}Please edit $PROJECT_ROOT/.env to add your API credentials${NC}"
fi

# Restart services
echo -e "${BLUE}=== Restarting services ===${NC}"
systemctl restart aixbt-dashboard
systemctl restart nginx

echo -e "${GREEN}=== Installation complete! ===${NC}"
echo -e "The AIXBT Dashboard is now available at: https://$DOMAIN"
echo -e "To check the status: systemctl status aixbt-dashboard"
echo -e "To view logs: journalctl -u aixbt-dashboard -f"
echo ""
echo -e "${YELLOW}Don't forget to:${NC}"
echo -e "1. Add your exchange API credentials to $PROJECT_ROOT/.env"
echo -e "2. Open port 80 and 443 in your firewall"
echo -e "3. Set up DNS records for $DOMAIN"

exit 0 