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


# Script to set up environment variables for cloud database testing

echo "Setting up environment variables for Scaleway PostgreSQL testing"
echo "================================================================"

# Prompt for credentials
read -p "Host: " POSTGRES_CLOUD_HOST
read -p "Port [5432]: " POSTGRES_CLOUD_PORT
POSTGRES_CLOUD_PORT=${POSTGRES_CLOUD_PORT:-5432}
read -p "Database name [omega_db]: " POSTGRES_CLOUD_DB
POSTGRES_CLOUD_DB=${POSTGRES_CLOUD_DB:-omega_db}
read -p "Username: " POSTGRES_CLOUD_USER
read -s -p "Password: " POSTGRES_CLOUD_PASSWORD
echo ""

# Export variables
export POSTGRES_CLOUD_HOST="$POSTGRES_CLOUD_HOST"
export POSTGRES_CLOUD_PORT="$POSTGRES_CLOUD_PORT"
export POSTGRES_CLOUD_DB="$POSTGRES_CLOUD_DB"
export POSTGRES_CLOUD_USER="$POSTGRES_CLOUD_USER"
export POSTGRES_CLOUD_PASSWORD="$POSTGRES_CLOUD_PASSWORD"

echo "Environment variables set!"
echo ""
echo "To run the cloud database test, use:"
echo "python scripts/test_db_connection.py --cloud"
echo ""
echo "NOTE: This script must be sourced, not executed."
echo "You should run it using: source scripts/setup_cloud_db_test.sh" 