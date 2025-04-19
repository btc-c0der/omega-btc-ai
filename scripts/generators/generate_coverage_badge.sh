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


# 🌌 AIXBT Divine Monitor Coverage Badge Generator
# --------------------------------------------

# Color definitions
CYAN='\033[0;36m'
PURPLE='\033[0;35m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Log function
log() {
    echo -e "${CYAN}[$(date +'%Y-%m-%d %H:%M:%S')]${RESET} ${1}"
}

# Error handling
handle_error() {
    echo -e "${RED}Error:${RESET} ${1}"
    exit 1
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    handle_error "Python 3 is not installed"
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    handle_error "pip3 is not installed"
fi

# Check if coverage is installed
if ! command -v coverage &> /dev/null; then
    log "Installing coverage..."
    pip3 install coverage || handle_error "Failed to install coverage"
fi

# Check if anybadge is installed
if ! command -v anybadge &> /dev/null; then
    log "Installing anybadge..."
    pip3 install anybadge || handle_error "Failed to install anybadge"
fi

# Create and activate virtual environment
log "Creating virtual environment..."
virtualenv -p python3 venv || handle_error "Failed to create virtual environment"

log "Activating virtual environment..."
source venv/bin/activate || handle_error "Failed to activate virtual environment"

# Install dependencies
log "Installing dependencies..."
pip install -r requirements.txt || handle_error "Failed to install dependencies"

# Copy test environment file
log "Setting up test environment..."
cp .env.test .env || handle_error "Failed to copy test environment file"

# Run coverage
log "Running coverage..."
coverage run -m pytest omega_ai/tests/ -v || handle_error "Coverage run failed"

# Get coverage percentage
log "Getting coverage percentage..."
COVERAGE=$(coverage report | tail -n 1 | awk '{print $4}' | sed 's/%//')

# Generate badge
log "Generating coverage badge..."
anybadge --value="$COVERAGE" --file=coverage.svg --label="coverage" --color="#4CAF50" || handle_error "Failed to generate coverage badge"

# Deactivate virtual environment
log "Deactivating virtual environment..."
deactivate

# Clean up
log "Cleaning up..."
rm -rf venv
rm -f .env

log "${GREEN}Coverage badge generated successfully!${RESET}"
log "${YELLOW}Badge file:${RESET} coverage.svg"
log "${YELLOW}Coverage:${RESET} ${COVERAGE}%" 