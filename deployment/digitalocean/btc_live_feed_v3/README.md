# BTC Live Feed v3 Deployment Guide

## Overview

This guide explains how to deploy BTC Live Feed v3 to DigitalOcean. The v3 version includes:

- Automatic Redis failover
- Health monitoring
- Enhanced error handling
- Data synchronization

## Prerequisites

1. DigitalOcean account with API access
2. `doctl` CLI tool installed
3. Redis instance (primary and failover)
4. Python 3.11 or higher
5. Required Python packages (installed via `pip install -e .`)

## Redis Configuration

BTC Live Feed v3 is configured to connect to DigitalOcean managed Redis using the following settings:

```
Host: omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com
Port: 25061
Username: default
Password: AVNS_OXMpU0P0ByYEz337Fgi
SSL: Enabled with cert_reqs set to None
```

### SSL Configuration Note

When connecting to DigitalOcean managed Redis with SSL, you need to set `REDIS_SSL_CERT_REQS=none` in your environment variables. This is because DigitalOcean uses its own certificate that may not be in your trusted root store.

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Primary Redis Configuration
REDIS_HOST=omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com
REDIS_PORT=25061
REDIS_USERNAME=default
REDIS_PASSWORD=AVNS_OXMpU0P0ByYEz337Fgi
REDIS_SSL=true
REDIS_USE_TLS=true
REDIS_SSL_CERT_REQS=none

# Failover Redis Configuration
FAILOVER_REDIS_HOST=omega-btc-ai-redis-do-user-20389918-0.d.db.ondigitalocean.com
FAILOVER_REDIS_PORT=25061
FAILOVER_REDIS_PASSWORD=AVNS_OXMpU0P0ByYEz337Fgi
FAILOVER_REDIS_USERNAME=default

# Health Check Configuration
HEALTH_CHECK_PORT=8080
HEALTH_CHECK_HOST=0.0.0.0
```

## Deployment Methods

### Method 1: Buildpack Deployment (Deprecated)

1. Install the package in development mode:

   ```bash
   pip install -e .
   ```

2. Authenticate with DigitalOcean:

   ```bash
   doctl auth init
   ```

3. Deploy the application:

   ```bash
   cd deployment/digitalocean/btc_live_feed_v3
   bash scripts/deploy.sh
   ```

### Method 2: Docker Deployment (Recommended)

1. Build the Docker image:

   ```bash
   cd deployment/digitalocean/btc_live_feed_v3
   docker build -t btc-live-feed-v3 .
   ```

2. Test locally with docker-compose:

   ```bash
   docker-compose up
   ```

3. Deploy to DigitalOcean App Platform:

   ```bash
   # Login to DigitalOcean Container Registry
   doctl registry login

   # Tag your image
   docker tag btc-live-feed-v3 registry.digitalocean.com/your-registry/btc-live-feed-v3:latest

   # Push to DigitalOcean Registry
   docker push registry.digitalocean.com/your-registry/btc-live-feed-v3:latest
   ```

4. Deploy from DigitalOcean dashboard:
   - Create a new App
   - Select "Deploy from Docker Registry"
   - Select your Docker image
   - Configure resources and settings

## Directory Structure

```
deployment/digitalocean/btc_live_feed_v3/
├── config/
│   └── app.yaml           # DigitalOcean app specification
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Local docker setup
├── scripts/
│   ├── deploy.sh         # Deployment script
│   └── setup_failover_redis.sh  # Redis failover setup
├── src/                  # Source code (symlinked to main package)
└── tests/               # Test files
```

## Health Monitoring

The application provides several monitoring endpoints:

- `/health`: Overall health status
- `/metrics`: Performance metrics
- `/redis/status`: Redis connection status

## Troubleshooting

1. **Redis Connection Issues**:
   - Check Redis credentials
   - Verify network connectivity
   - Check Redis logs

2. **Health Check Failures**:
   - Verify port 8080 is accessible
   - Check application logs
   - Verify environment variables

3. **Deployment Failures**:
   - Check DigitalOcean logs
   - Verify app.yaml configuration
   - Check environment variables

4. **Docker Deployment Issues**:
   - Check Docker build logs
   - Verify environment variables in Dockerfile
   - Check container logs with `docker logs <container_id>`

## Maintenance

1. **Updating the Application**:

   ```bash
   # For buildpack deployment
   doctl apps update $APP_ID --spec config/app.yaml
   
   # For Docker deployment
   docker build -t btc-live-feed-v3 .
   docker tag btc-live-feed-v3 registry.digitalocean.com/your-registry/btc-live-feed-v3:latest
   docker push registry.digitalocean.com/your-registry/btc-live-feed-v3:latest
   ```

2. **Scaling**:

   ```bash
   doctl apps update $APP_ID --instance-count 2
   ```

3. **Monitoring**:
   - Use DigitalOcean's built-in monitoring
   - Check application logs
   - Monitor Redis performance

## Support

For issues or questions:

1. Check the application logs
2. Review the health check endpoints
3. Contact the OMEGA BTC AI team
