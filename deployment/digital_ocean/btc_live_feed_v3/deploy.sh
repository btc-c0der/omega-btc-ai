#!/bin/bash

# OMEGA BTC AI - BTC Live Feed v3 Digital Ocean Deployment Script
# =============================================================
# This script automates the deployment of BTC Live Feed v3 to Digital Ocean App Platform

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
RESET='\033[0m'

# Logo display
echo -e "${MAGENTA}"
echo "🔱 OMEGA BTC AI - BTC Live Feed v3 Digital Ocean Deployment 🔱"
echo -e "${RESET}"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}❌ Error: doctl not found. Please install the Digital Ocean CLI.${RESET}"
    echo "Installation instructions: https://docs.digitalocean.com/reference/doctl/how-to/install/"
    exit 1
fi

# Check if authenticated
echo -e "${YELLOW}🔄 Checking Digital Ocean authentication...${RESET}"
if ! doctl account get &> /dev/null; then
    echo -e "${RED}❌ Error: Not authenticated with Digital Ocean.${RESET}"
    echo "Please run 'doctl auth init' and try again."
    exit 1
fi

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Configuration variables
APP_SPEC="${SCRIPT_DIR}/app.yaml"
DEPLOY_BRANCH="feature/btc-live-feed-v3-resilient"
APP_NAME="omega-btc-ai-live-feed-v3"

# Check if app.yaml exists
if [ ! -f "$APP_SPEC" ]; then
    echo -e "${RED}❌ Error: $APP_SPEC not found.${RESET}"
    exit 1
fi

# Check if we're on the correct branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [ "$CURRENT_BRANCH" != "$DEPLOY_BRANCH" ]; then
    echo -e "${YELLOW}⚠️ Warning: You are not on the deployment branch ($DEPLOY_BRANCH).${RESET}"
    read -p "Do you want to switch to $DEPLOY_BRANCH? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git checkout $DEPLOY_BRANCH
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Error: Failed to switch to branch $DEPLOY_BRANCH.${RESET}"
            exit 1
        fi
    else
        read -p "Continue deployment from current branch? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Deployment cancelled.${RESET}"
            exit 0
        fi
    fi
fi

# Verify source files exist
SRC_DIR="${SCRIPT_DIR}/src"
if [ ! -d "$SRC_DIR" ]; then
    echo -e "${RED}❌ Error: Source directory not found: $SRC_DIR${RESET}"
    exit 1
fi

if [ ! -f "${SRC_DIR}/omega_ai/data_feed/btc_live_feed_v3.py" ]; then
    echo -e "${RED}❌ Error: Main BTC Live Feed v3 file not found.${RESET}"
    exit 1
fi

if [ ! -f "${SRC_DIR}/omega_ai/utils/enhanced_redis_manager.py" ]; then
    echo -e "${RED}❌ Error: Enhanced Redis Manager file not found.${RESET}"
    exit 1
fi

echo -e "${GREEN}✅ All required source files found.${RESET}"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️ Warning: You have uncommitted changes.${RESET}"
    read -p "Do you want to commit these changes before deploying? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "Enter commit message: " commit_msg
        git add .
        git commit -m "$commit_msg"
        if [ $? -ne 0 ]; then
            echo -e "${RED}❌ Error: Failed to commit changes.${RESET}"
            exit 1
        fi
    fi
fi

# Check if the app already exists
echo -e "${YELLOW}🔍 Checking if app already exists...${RESET}"
APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "$APP_NAME" | awk '{print $1}')

# Deploy to Digital Ocean
echo -e "${YELLOW}🚀 Deploying to Digital Ocean App Platform...${RESET}"

if [ -z "$APP_ID" ]; then
    # Create new app
    echo -e "${BLUE}Creating new app: $APP_NAME${RESET}"
    doctl apps create --spec "$APP_SPEC"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to create app.${RESET}"
        exit 1
    fi
else
    # Update existing app
    echo -e "${BLUE}Updating existing app: $APP_NAME (ID: $APP_ID)${RESET}"
    doctl apps update $APP_ID --spec "$APP_SPEC"
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to update app.${RESET}"
        exit 1
    fi
fi

# Push changes if needed
read -p "Push latest changes to remote repository? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}🔄 Pushing changes to remote repository...${RESET}"
    git push origin $CURRENT_BRANCH
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Error: Failed to push changes.${RESET}"
        exit 1
    fi
fi

# Get app details and URL
if [ -z "$APP_ID" ]; then
    APP_ID=$(doctl apps list --format ID,Spec.Name --no-header | grep "$APP_NAME" | awk '{print $1}')
fi

if [ -n "$APP_ID" ]; then
    echo -e "${GREEN}✅ App deployed successfully!${RESET}"
    echo -e "${YELLOW}App Details:${RESET}"
    doctl apps get $APP_ID
    
    # Get app URL
    APP_URL=$(doctl apps get $APP_ID --format DefaultIngress --no-header)
    echo -e "${GREEN}App URL: $APP_URL${RESET}"
    echo -e "${BLUE}Health Check URL: ${APP_URL}/health${RESET}"
    
    # Show monitoring command
    echo -e "${YELLOW}To monitor the app, run:${RESET}"
    echo -e "python ${SRC_DIR}/scripts/monitor_btc_feed_v3.py --host $APP_URL --port 8080 --refresh 5"
else
    echo -e "${YELLOW}⚠️ App deployed but couldn't retrieve app details.${RESET}"
fi

echo -e "${GREEN}🎉 Deployment process completed!${RESET}" 