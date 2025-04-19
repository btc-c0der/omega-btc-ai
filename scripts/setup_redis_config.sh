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

# Setup Redis configuration environment variables
# This script helps switch between local and cloud Redis instances

# Check if a parameter was provided (local/cloud)
if [ "$1" == "cloud" ]; then
    echo "🚀 Setting up CLOUD Redis configuration..."
    export OMEGA_USE_CLOUD_REDIS=true
    
    # Prompt for Redis password if not provided
    if [ -z "$REDIS_PASSWORD" ]; then
        echo -n "Enter Redis password for btc-omega-redis: "
        read -s REDIS_PASSWORD
        echo ""
        export REDIS_PASSWORD
    fi
    
    # Check for certificate file
    CERT_FILE="SSL_redis-btc-omega-redis.pem"
    if [ ! -f "$CERT_FILE" ]; then
        echo "⚠️ Warning: SSL certificate file $CERT_FILE not found in current directory."
        echo "    You may need to download this file from Scaleway."
        echo -n "Path to certificate file (press Enter to use default name): "
        read CERT_PATH
        if [ ! -z "$CERT_PATH" ]; then
            export REDIS_CA_CERT="$CERT_PATH"
        fi
    fi
    
    # Set other cloud Redis parameters
    export REDIS_HOST=172.16.8.2
    export REDIS_PORT=6379
    export REDIS_USERNAME=btc-omega-redis
    
    echo "✅ Cloud Redis configuration set:"
    echo "  • Host: $REDIS_HOST"
    echo "  • Username: $REDIS_USERNAME"
    echo "  • SSL: Enabled"
    echo "  • Certificate: ${REDIS_CA_CERT:-$CERT_FILE}"
    
elif [ "$1" == "local" ] || [ -z "$1" ]; then
    echo "🏠 Setting up LOCAL Redis configuration..."
    export OMEGA_USE_CLOUD_REDIS=false
    
    # Set default local Redis parameters
    export REDIS_HOST=localhost
    export REDIS_PORT=6379
    export REDIS_DB=0
    
    # Unset cloud-specific variables
    unset REDIS_USERNAME
    unset REDIS_PASSWORD
    unset REDIS_CA_CERT
    
    echo "✅ Local Redis configuration set:"
    echo "  • Host: $REDIS_HOST"
    echo "  • Port: $REDIS_PORT"
    echo "  • SSL: Disabled"
    
else
    echo "❌ Invalid parameter: $1"
    echo "Usage: source $0 [local|cloud]"
    exit 1
fi

# Remind user to source this script
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "⚠️ This script should be sourced, not executed, to set environment variables."
    echo "    Please run: source $0 $1"
fi

# Instructions for testing Redis connection
echo ""
echo "📝 To test your Redis connection, run:"
echo "    python -c 'from omega_ai.utils.redis_manager import RedisManager, get_redis_config; RedisManager(**get_redis_config())'" 