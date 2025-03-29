#!/bin/bash
set -e

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

echo "🔱 OMEGA BTC AI News Feed Service - Divine Startup 🔱"
echo "===================================================="
echo "Starting at: $(date)"

# Create necessary directories if they don't exist
mkdir -p /app/data/news
mkdir -p /app/logs

# Check if Redis is accessible
if [[ ! -z "$REDIS_HOST" ]]; then
  echo "📊 Checking Redis connection at $REDIS_HOST:$REDIS_PORT..."
  
  # Wait for Redis to be available
  MAX_RETRIES=30
  RETRY_INTERVAL=2
  
  for i in $(seq 1 $MAX_RETRIES); do
    if python -c "
import redis
try:
    r = redis.Redis(host='$REDIS_HOST', port=$REDIS_PORT, db=0)
    r.ping()
    print('✅ Redis connection successful')
    exit(0)
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
    exit(1)
"; then
      break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
      echo "❌ Failed to connect to Redis after $MAX_RETRIES attempts. Continuing without Redis..."
    else
      echo "⏳ Waiting for Redis to be available... (attempt $i/$MAX_RETRIES)"
      sleep $RETRY_INTERVAL
    fi
  done
else
  echo "⚠️ REDIS_HOST not set, continuing without Redis integration"
fi

# Check for SSL certificates if REDIS_SSL is enabled
if [[ "$REDIS_SSL" == "true" ]]; then
  echo "🔒 Redis SSL is enabled, checking for certificates..."
  
  # Check if we have SSL certificates
  if [[ -f "/app/ssl/redis-ca.crt" ]]; then
    echo "✅ Found Redis CA certificate"
    export REDIS_SSL_CA_CERTS="/app/ssl/redis-ca.crt"
  fi
  
  if [[ -f "/app/ssl/redis-client.crt" && -f "/app/ssl/redis-client.key" ]]; then
    echo "✅ Found Redis client certificate and key"
    export REDIS_SSL_CERTFILE="/app/ssl/redis-client.crt"
    export REDIS_SSL_KEYFILE="/app/ssl/redis-client.key"
  fi
fi

# Set PYTHONPATH for the application
export PYTHONPATH=$PYTHONPATH:/app:/app/src

# Print configuration
echo "===================================================="
echo "📋 Configuration:"
echo "  - Redis Host: $REDIS_HOST"
echo "  - Redis Port: $REDIS_PORT"
echo "  - Redis SSL: ${REDIS_SSL:-false}"
echo "  - News Service Port: $NEWS_SERVICE_PORT"
echo "  - Python Path: $PYTHONPATH"
echo "===================================================="

# Execute the command provided as arguments
echo "🚀 Executing command: $@"
exec "$@" 