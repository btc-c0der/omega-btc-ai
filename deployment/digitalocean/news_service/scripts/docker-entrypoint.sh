#!/bin/bash
set -e

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

echo "🔱 OMEGA BTC AI News Feed Service - Divine Startup 🔱"
echo "===================================================="
echo "Starting at: $(date)"
echo "Working directory: $(pwd)"
echo "Directory contents: $(ls -la)"

# Create necessary directories if they don't exist
mkdir -p /workspace/data/news
mkdir -p /workspace/logs
echo "📁 Created required directories"

# Check environment variables
echo "📊 Checking environment variables..."
REQUIRED_VARS=("NEWS_SERVICE_PORT")
missing_vars=0

for var in "${REQUIRED_VARS[@]}"; do
  if [[ -z "${!var}" ]]; then
    echo "❌ Missing required environment variable: $var"
    missing_vars=$((missing_vars+1))
  else
    echo "✅ Found environment variable: $var = ${!var}"
  fi
done

if [[ $missing_vars -gt 0 ]]; then
  echo "⚠️ Warning: $missing_vars required environment variables are missing."
fi

# Check if Redis is accessible
if [[ ! -z "$REDIS_HOST" ]]; then
  echo "📊 Checking Redis connection at $REDIS_HOST:$REDIS_PORT..."
  
  # Wait for Redis to be available
  MAX_RETRIES=30
  RETRY_INTERVAL=2
  
  for i in $(seq 1 $MAX_RETRIES); do
    if python -c "
import redis
import sys
try:
    redis_params = {
        'host': '$REDIS_HOST', 
        'port': $REDIS_PORT, 
        'db': 0,
        'socket_timeout': 5,
        'socket_connect_timeout': 5
    }
    
    if '$REDIS_USERNAME' and '$REDIS_USERNAME' != '':
        redis_params['username'] = '$REDIS_USERNAME'
    
    if '$REDIS_PASSWORD' and '$REDIS_PASSWORD' != '':
        redis_params['password'] = '$REDIS_PASSWORD'
    
    if '$REDIS_SSL' == 'true':
        redis_params['ssl'] = True
        redis_params['ssl_cert_reqs'] = None
    
    print(f'Connecting to Redis with params: {redis_params}')
    r = redis.Redis(**redis_params)
    ping_result = r.ping()
    print(f'✅ Redis connection successful: {ping_result}')
    r.set('news_service_health_check', 'OK')
    sys.exit(0)
except Exception as e:
    print(f'❌ Redis connection failed: {e}')
    sys.exit(1)
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
  if [[ -f "/workspace/ssl/redis-ca.crt" ]]; then
    echo "✅ Found Redis CA certificate"
    export REDIS_SSL_CA_CERTS="/workspace/ssl/redis-ca.crt"
  fi
  
  if [[ -f "/workspace/SSL_redis-btc-omega-redis.pem" ]]; then
    echo "✅ Found Redis PEM certificate"
    export REDIS_SSL_CERT_FILE="/workspace/SSL_redis-btc-omega-redis.pem"
  fi
  
  if [[ -f "/workspace/ssl/redis-client.crt" && -f "/workspace/ssl/redis-client.key" ]]; then
    echo "✅ Found Redis client certificate and key"
    export REDIS_SSL_CERTFILE="/workspace/ssl/redis-client.crt"
    export REDIS_SSL_KEYFILE="/workspace/ssl/redis-client.key"
  fi
fi

# Check for Python modules
echo "📚 Checking for required Python modules..."
python -c "
import sys
required_modules = ['redis', 'pandas', 'numpy', 'textblob', 'fastapi', 'uvicorn']
missing_modules = []

for module in required_modules:
    try:
        __import__(module)
        print(f'✅ Module {module} is available')
    except ImportError:
        missing_modules.append(module)
        print(f'❌ Module {module} is missing')

if missing_modules:
    print(f'⚠️ Warning: Missing {len(missing_modules)} required modules: {missing_modules}')
else:
    print('🎉 All required modules are available')
"

# Set PYTHONPATH for the application
export PYTHONPATH=$PYTHONPATH:/workspace:/workspace/src

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
echo "===================================================="
exec "$@" 