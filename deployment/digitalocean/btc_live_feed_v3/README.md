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

## Environment Variables

Create a `.env` file in the project root with the following variables:

```bash
# Primary Redis Configuration
REDIS_HOST=your.redis.host
REDIS_PORT=6379
REDIS_PASSWORD=your_password
REDIS_USERNAME=your_username

# Failover Redis Configuration
FAILOVER_REDIS_HOST=localhost
FAILOVER_REDIS_PORT=6379
FAILOVER_REDIS_PASSWORD=your_password
FAILOVER_REDIS_USERNAME=your_username

# Health Check Configuration
HEALTH_CHECK_PORT=8080
HEALTH_CHECK_HOST=0.0.0.0
```

## Deployment Steps

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

4. Monitor the deployment:
   - Check the DigitalOcean dashboard
   - Use the monitoring dashboard: `python scripts/monitor_btc_feed_v3.py`
   - Access health check endpoint: `http://your-app-url:8080/health`

## Directory Structure

```
deployment/digitalocean/btc_live_feed_v3/
├── config/
│   └── app.yaml           # DigitalOcean app specification
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

## Maintenance

1. **Updating the Application**:

   ```bash
   doctl apps update $APP_ID --spec config/app.yaml
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
