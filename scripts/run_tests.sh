#!/bin/bash

# 🌌 AIXBT Divine Monitor Test Runner
# ---------------------------------

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

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    log "Installing virtualenv..."
    pip3 install virtualenv || handle_error "Failed to install virtualenv"
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

# Run tests
log "Running tests..."
pytest omega_ai/tests/ -v --cov=omega_ai --cov-report=term-missing || handle_error "Tests failed"

# Deactivate virtual environment
log "Deactivating virtual environment..."
deactivate

# Clean up
log "Cleaning up..."
rm -rf venv
rm -f .env

log "${GREEN}All tests completed successfully!${RESET}" 