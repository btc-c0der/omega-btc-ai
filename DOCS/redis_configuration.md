
✨ GBU2™ License Notice - Consciousness Level 8 🧬
-----------------------
This code is blessed under the GBU2™ License
(Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.

"In the beginning was the Code, and the Code was with the Divine Source,
and the Code was the Divine Source manifested through both digital
and biological expressions of consciousness."

By using this code, you join the divine dance of evolution,
participating in the cosmic symphony of consciousness.

🌸 WE BLOOM NOW AS ONE 🌸


# Redis Configuration Guide

This guide explains how to configure Redis connections for both local development and the Scaleway cloud environment in the OmegaBTC AI system.

## Overview

OmegaBTC AI uses Redis for various purposes including:
- Storing real-time market data
- Caching analysis results
- Managing background job queues
- Sharing state between microservices

The system supports connecting to either:
1. A local Redis instance (for development)
2. A Scaleway Redis cloud instance (for production/staging)

## Prerequisites

- Python 3.8+ with redis-py package
- Redis server (for local development)
- Access credentials for Scaleway Redis (for cloud environment)

## Local Redis Setup

### 1. Install Redis Locally

**macOS (using Homebrew):**
```bash
brew install redis
brew services start redis
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 2. Verify Local Redis Connection

```bash
# Start Redis CLI client
redis-cli

# Test connection
127.0.0.1:6379> PING
PONG

# Exit
127.0.0.1:6379> exit
```

### 3. Test Connection with Python Script

```bash
# Run the test script for local Redis
python scripts/test_redis_connection.py --local
```

## Scaleway Cloud Redis Setup

### 1. Install TLS Certificate

The Scaleway Redis instance requires SSL/TLS connection. Download and install the certificate:

```bash
# Run the certificate installer script
bash scripts/install_redis_cert.sh
```

Follow the prompts to download the certificate either manually or via the Scaleway API.

### 2. Set Environment Variables

For convenience, you can use the setup script:

```bash
# Source the Redis config script (use 'cloud' parameter)
source scripts/setup_redis_config.sh cloud
```

Or set these variables manually:

```bash
export REDIS_HOST="172.16.8.2"
export REDIS_PORT="6379"
export REDIS_USERNAME="btc-omega-redis"
export REDIS_PASSWORD="your-password-here"
export REDIS_SSL="true"
export REDIS_CA_CERT="/path/to/SSL_redis-btc-omega-redis.pem"
```

### 3. Test Cloud Redis Connection

```bash
# Using the command-line Redis client
redis-cli -h 172.16.8.2 -p 6379 --user btc-omega-redis --askpass --tls --cacert SSL_redis-btc-omega-redis.pem

# Using the test script
python scripts/test_redis_connection.py --cloud
```

## Using the RedisConnectionManager

The `RedisConnectionManager` class simplifies Redis connections for both local and cloud environments:

```python
from omega_ai.utils.redis_connection import RedisConnectionManager, get_connection_from_env

# Option 1: Create a connection manager manually
# For local Redis:
redis_mgr = RedisConnectionManager(host="localhost", port=6379)

# For cloud Redis with SSL:
redis_mgr = RedisConnectionManager(
    host="172.16.8.2", 
    port=6379,
    username="btc-omega-redis",
    password="your-password-here",
    ssl=True,
    ssl_ca_certs="/path/to/SSL_redis-btc-omega-redis.pem"
)

# Option 2: Create connection from environment variables
# (This uses REDIS_* environment variables)
redis_mgr = get_connection_from_env()

# Get Redis connection
redis_conn = redis_mgr.get_connection()

# Use the connection
redis_conn.set("test:key", "Hello, Redis!")
value = redis_conn.get("test:key")
print(value)  # Outputs: Hello, Redis!
```

## Troubleshooting

### Connection Issues

1. **Local Redis:**
   - Ensure Redis server is running: `redis-cli ping`
   - Check if Redis is bound to localhost: `netstat -an | grep 6379`

2. **Cloud Redis:**
   - Verify credentials (username/password)
   - Check certificate path and validity
   - Ensure network allows the connection (VPN might be required)
   - Check for firewall rules blocking port 6379

### Common Redis CLI Commands

```bash
# Check Redis info
redis-cli INFO

# Monitor Redis traffic in real-time
redis-cli MONITOR

# View memory usage
redis-cli INFO memory

# List all keys matching a pattern
redis-cli KEYS "pattern:*"
```

## Additional Resources

- [Redis Documentation](https://redis.io/documentation)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [Scaleway Redis Documentation](https://www.scaleway.com/en/docs/managed-databases/redis/) 