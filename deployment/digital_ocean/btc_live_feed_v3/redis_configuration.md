# 🔮 Redis Configuration for BTC Live Feed v3

This guide provides detailed instructions for configuring Redis for the BTC Live Feed v3 deployment on Digital Ocean, focusing on the dual-Redis setup needed for automatic failover.

## Overview

BTC Live Feed v3 uses two Redis instances:

1. **Primary Redis**: A managed Redis database on Digital Ocean
2. **Failover Redis**: A local Redis instance running on the same Digital Ocean App

This dual-Redis architecture provides automatic failover capabilities, ensuring 99.99% uptime even during temporary outages of the primary Redis service.

## Digital Ocean Managed Redis Setup

### 1. Create a New Redis Database Cluster

1. Log in to your Digital Ocean account
2. Navigate to "Databases" and click "Create Database Cluster"
3. Select "Redis" as the database type
4. Choose the appropriate plan (at least Basic)
5. Select the same region as your App Platform deployment
6. Name your cluster (e.g., `omega-btc-ai-redis`)
7. Click "Create Database Cluster"

### 2. Configure User Access

When the database is created, you'll receive:

- Connection string
- Default username: `default`
- Password (save this securely)

### 3. Configure Trusted Sources

1. In the Redis database dashboard, go to "Settings" > "Trusted Sources"
2. Add your App Platform's IP addresses
   - If your app uses dynamic IPs, select "Allow All IPv4"
   - For production, limit access to only your app by using the VPC integration

### 4. SSL Configuration

Digital Ocean Redis requires SSL connections. Configure your app to use SSL:

1. Set `REDIS_USE_SSL=true` in your app environment variables
2. For certificate verification in production, you need to specify:

   ```
   REDIS_SSL_CERT_REQS=required
   REDIS_CERT=/workspace/SSL_redis-btc-omega-redis.pem
   ```

3. Make sure the certificate file `SSL_redis-btc-omega-redis.pem` is available in your workspace directory. This is typically deployed along with your application to Digital Ocean.

4. If you don't have the certificate file, you can copy it from an existing Digital Ocean deployment:

   ```bash
   # From your local machine
   doctl apps get <app-id>
   doctl ssh <component-name>
   
   # Once connected to the Digital Ocean app
   cd /workspace
   cat SSL_redis-btc-omega-redis.pem
   # Copy the contents to a local file
   ```

5. For testing/development without a certificate, you can use:

   ```
   REDIS_SSL_CERT_REQS=none
   ```

   But this is not recommended for production environments.

## Local Failover Redis Setup

The local Redis instance runs directly on the App Platform and serves as a failover when the primary Redis is unavailable.

### Deployment with App Platform

1. In the App Platform configuration, add the following packages to your app's build requirements:

   ```
   redis-server
   ```

2. Add a pre-run command to start the local Redis:

   ```
   redis-server --port 6379 --protected-mode no --daemonize yes
   ```

3. Configure environment variables:

   ```
   FAILOVER_REDIS_HOST=localhost
   FAILOVER_REDIS_PORT=6379
   ```

## Enhanced Redis Manager Configuration

The `EnhancedRedisManager` needs specific configuration to work with both Redis instances:

```python
# Example configuration
redis_manager = EnhancedRedisManager(
    use_failover=True,  # Enable failover
    sync_on_reconnect=True,  # Synchronize data when reconnecting to primary
    retry_interval=60,  # Retry connecting to primary every 60 seconds
    priority_keys=["last_btc_price", "last_btc_update_time"]  # Keys to sync first
)
```

## Environment Variables

Ensure these environment variables are configured in your Digital Ocean App Platform:

```
# Primary Redis
REDIS_HOST=${redis.HOSTNAME}
REDIS_PORT=${redis.PORT}
REDIS_USERNAME=${redis.USERNAME}
REDIS_PASSWORD=${redis.PASSWORD}
REDIS_USE_SSL=true

# Failover Redis
FAILOVER_REDIS_HOST=localhost
FAILOVER_REDIS_PORT=6379
```

## Data Synchronization Strategy

BTC Live Feed v3 uses the following strategy for Redis data synchronization:

1. **Priority Keys**: Critical data like current BTC price is synchronized first
2. **Batch Synchronization**: Non-priority keys are synchronized in batches
3. **Key Type Handling**: Different Redis data types (strings, lists, hashes) are handled appropriately
4. **Automatic Reconnection**: The system attempts to reconnect to the primary Redis at regular intervals

## Monitoring Redis Connections

Monitor Redis connections using:

1. **Health Check API**: Access `/redis/status` endpoint
2. **CLI Monitoring Tool**: Use `scripts/monitor_btc_feed_v3.py`
3. **Digital Ocean Metrics**: Check the Redis metrics in the Digital Ocean dashboard

## Performance Considerations

For optimal performance:

1. **Memory Usage**: Configure maxmemory policy in Redis settings

   ```
   maxmemory 100mb
   maxmemory-policy allkeys-lru
   ```

2. **Connection Pooling**: The Enhanced Redis Manager uses connection pooling for efficiency

3. **Periodic Cleaning**: Set up automatic cleaning of old data:

   ```
   # Configure automatic key expiration
   REDIS_DATA_EXPIRATION=86400  # 24 hours in seconds
   ```

## Troubleshooting

### Connection Issues

1. **Cannot connect to primary Redis**
   - Verify credentials in environment variables
   - Check that SSL is properly configured
   - Verify firewall rules in Digital Ocean

2. **Failover not working**
   - Check local Redis is running: `redis-cli ping`
   - Verify environment variables for failover Redis
   - Check logs for connection errors

### Data Synchronization Issues

1. **Missing data after failover recovery**
   - Check synchronization logs
   - Manually trigger sync: `curl -X POST https://<app-url>/redis/sync`

2. **Slow synchronization**
   - Increase batch size for larger deployments
   - Prioritize more critical keys

## Security Recommendations

1. **Password Strength**: Use strong unique passwords for Redis
2. **Network Isolation**: Use Digital Ocean VPC for private networking
3. **Access Control**: Limit trusted sources to only your application
4. **Encryption**: Keep SSL enabled for all Redis connections

## Backup Strategy

1. Configure automatic backups with Digital Ocean:
   - Navigate to your Redis database
   - Go to "Settings" > "Backups"
   - Configure daily backups with appropriate retention

2. For manual backups, you can use:

   ```bash
   doctl databases backup <redis-cluster-id>
   ```

## References

- [Digital Ocean Redis Documentation](https://docs.digitalocean.com/products/databases/redis/)
- [Redis Security Documentation](https://redis.io/topics/security)
- [Enhanced Redis Manager Documentation](../../BOOK/BTC_LIVE_FEED_V3.md)
