# BTC Live Feed v3 Documentation

## Overview

BTC Live Feed v3 is an enhanced version of the OMEGA BTC AI price feed service with automatic Redis failover capabilities. This service provides resilient monitoring of Bitcoin prices with 99.99% uptime guarantee through the implementation of automatic failover between remote and local Redis instances.

## Key Features

- **Automatic Redis Failover**: Seamlessly switches between remote (Digital Ocean) and local Redis instances to ensure continuous operation.
- **Data Synchronization**: Automatically synchronizes data between primary and failover Redis instances when connections are restored.
- **Enhanced Error Handling**: Recovers gracefully from connection issues and other runtime errors.
- **Comprehensive Health Monitoring**: Provides detailed health metrics and connection status through a dedicated API.
- **Performance Metrics**: Tracks and exposes detailed performance statistics for monitoring and diagnostics.
- **Configurable Failover Behavior**: Can be configured to use failover only for critical operations or for all Redis interactions.

## Architecture

BTC Live Feed v3 consists of several key components:

1. **WebSocket Client**: Connects to cryptocurrency exchanges to receive real-time Bitcoin price updates.
2. **Enhanced Redis Manager**: Handles connections to primary (remote) and failover (local) Redis instances with automatic failover capabilities.
3. **Health Check Server**: Provides API endpoints to monitor the status and performance of the feed.
4. **Monitoring Client**: CLI tool to visualize the feed's operation and performance.

## Enhanced Redis Manager

The Enhanced Redis Manager is the core component providing resilience and fault tolerance. It:

- Manages connections to both primary (remote) and failover (local) Redis instances
- Automatically detects connection failures and switches between instances
- Synchronizes data between instances when reconnecting to primary Redis
- Provides connection health statistics and monitoring information
- Supports prioritization of critical keys during synchronization operations

## Setup and Configuration

### Prerequisites

- Python 3.8+
- Redis server (for local failover)
- Required Python packages:
  - websockets
  - redis
  - fastapi
  - uvicorn
  - requests (for monitoring client)

### Environment Variables

The following environment variables are used to configure BTC Live Feed v3:

```
# Primary (Remote) Redis Configuration
REDIS_HOST=your.redis.host
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_USERNAME=your_username (optional)
REDIS_USE_SSL=true|false

# Failover (Local) Redis Configuration
FAILOVER_REDIS_HOST=localhost
FAILOVER_REDIS_PORT=6379
FAILOVER_REDIS_PASSWORD=your_password (optional)
FAILOVER_REDIS_USERNAME=your_username (optional)

# Health Check Server Configuration
HEALTH_CHECK_PORT=8080
HEALTH_CHECK_HOST=0.0.0.0
```

## Running the Service

### Starting the Feed

```bash
# From project root
python -m omega_ai.data_feed.btc_live_feed_v3
```

### Monitoring the Feed

```bash
# From project root
python scripts/monitor_btc_feed_v3.py --host localhost --port 8080 --refresh 5
```

## Health Check API

The Health Check API provides endpoints to monitor the status of the BTC Live Feed:

- **GET /health**: Returns the overall health status, including Redis and WebSocket connection status, last price, and uptime information.
- **GET /metrics**: Returns detailed performance metrics, including message processing time, operation success rate, and message counts.
- **GET /redis/status**: Returns specific Redis connection details, including failover status and reconnection statistics.

## Monitoring Dashboard

The monitoring client provides a CLI dashboard with the following information:

- Overall service status (healthy, degraded, unhealthy)
- Latest Bitcoin price and time since last update
- Redis connection status, including primary and failover availability
- WebSocket connection status
- Performance metrics, including message processing time and success rates
- Uptime and reconnection statistics

## Error Handling and Recovery

BTC Live Feed v3 implements the following error handling strategies:

1. **WebSocket Disconnections**: Automatic reconnection with exponential backoff
2. **Redis Connection Failures**: Automatic failover to local Redis with periodic reconnection attempts to primary
3. **Data Consistency**: Synchronization of data between Redis instances when connections are restored
4. **Health Check Integration**: Health endpoints expose current status for external monitoring systems

## Deployment Considerations

When deploying to Digital Ocean:

1. Ensure the app service has the necessary environment variables configured
2. For local failover in cloud environments, consider using a Redis instance in the same region
3. Adjust reconnection intervals based on expected network reliability
4. Monitor the health endpoints from external monitoring tools

## Development and Extensions

### Adding New Redis Operations

To add new Redis operations to the Enhanced Redis Manager:

1. Create a new method in the `EnhancedRedisManager` class
2. Include proper error handling and failover logic
3. Document the method's behavior with respect to failover

### Enhancing Monitoring Capabilities

The monitoring system can be extended by:

1. Adding new metrics to the feed's performance tracking
2. Creating new endpoints in the health check API
3. Enhancing the monitoring client to display additional information

## Troubleshooting

Common issues and their solutions:

1. **Cannot connect to primary Redis**: Verify credentials and network connectivity.
2. **WebSocket connection errors**: Check internet connectivity and firewall settings.
3. **Failover not working**: Ensure local Redis is running and properly configured.
4. **High latency in updates**: Check network conditions and Redis performance.

## Conclusion

BTC Live Feed v3 represents a significant enhancement in reliability and fault tolerance for the OMEGA BTC AI ecosystem. By implementing automatic failover between remote and local Redis instances, it ensures continuous operation even during temporary outages of the primary Redis service.

---

Copyright (c) 2025 OMEGA-BTC-AI - Licensed under the MIT License
JAH JAH BLESS THE DIVINE FLOW OF THE BLOCKCHAIN
