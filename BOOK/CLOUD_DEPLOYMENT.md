
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


# 🔱 OMEGA BTC AI - Digital Ocean Cloud Deployment 🔱

This document provides comprehensive instructions for deploying the OMEGA BTC AI system on Digital Ocean's App Platform. The deployment focuses on the BTC Live Feed v2 component, which serves as the data collection and distribution engine for the system.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Digital Ocean Setup](#digital-ocean-setup)
- [Deployment Process](#deployment-process)
- [Environment Configuration](#environment-configuration)
- [Monitoring & Management](#monitoring--management)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)
- [BTC Live Feed v3 Deployment](#btc-live-feed-v3-deployment)

## Prerequisites

Before deploying to Digital Ocean, ensure you have:

- A Digital Ocean account with billing set up
- Digital Ocean CLI (`doctl`) installed and authenticated
- Git repository with the OMEGA BTC AI codebase
- Redis database credentials (Upstash Redis recommended)
- Docker installed locally for testing (optional)

## Digital Ocean Setup

### 1. Install Digital Ocean CLI

```bash
# macOS
brew install doctl

# Linux
snap install doctl

# Windows
scoop install doctl
```

### 2. Authenticate Digital Ocean CLI

```bash
doctl auth init
```

Follow the prompts to authenticate using your Digital Ocean API token.

### 3. Create App Platform Resources

The easiest way to create your initial application is through the Digital Ocean web console:

1. Login to [Digital Ocean Console](https://cloud.digitalocean.com/)
2. Navigate to "Apps" → "Create App"
3. Select "GitHub" as the source
4. Choose the OMEGA BTC AI repository
5. Select the branch (typically `feature/btc-live-feed-v2-cloud` or `main`)
6. Configure the build settings:
   - Source Directory: `/`
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `python -m omega_ai.data_feed.btc_live_feed_v2`

## Deployment Process

### Manual Deployment

You can trigger a manual deployment through the Digital Ocean console or CLI:

```bash
# Get App ID
doctl apps list

# Deploy app
doctl apps create --spec app.yaml
```

### Automatic Deployment

The app is configured for automatic deployments when changes are pushed to the GitHub repository. To update the deployed application:

```bash
# Make your changes
git add .
git commit -m "Update BTC Live Feed v2"
git push origin feature/btc-live-feed-v2-cloud
```

Digital Ocean will automatically detect the push and start a new deployment.

## Environment Configuration

The app requires the following environment variables, which can be configured in the Digital Ocean console or in the `app.yaml` file:

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `REDIS_HOST` | Redis server hostname | `redis-12345.upstash.io` |
| `REDIS_PORT` | Redis server port | `12345` |
| `REDIS_USERNAME` | Redis username (if applicable) | `default` |
| `REDIS_PASSWORD` | Redis password | `xxxxxxxxxxxx` |
| `REDIS_SSL` | Whether to use SSL for Redis | `true` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `EXCHANGE_API_KEY` | Exchange API key (if applicable) | `xxxxxxxxxxxx` |
| `EXCHANGE_API_SECRET` | Exchange API secret (if applicable) | `xxxxxxxxxxxx` |

### App Specification (app.yaml)

The `app.yaml` file defines the application configuration. Example:

```yaml
name: omega-btc-live-feed-v2
region: nyc
services:
- name: btc-live-feed
  github:
    repo: username/omega-btc-ai
    branch: feature/btc-live-feed-v2-cloud
    deploy_on_push: true
  source_dir: /
  envs:
  - key: REDIS_HOST
    value: ${redis.host}
    scope: RUN_TIME
  - key: REDIS_PORT
    value: ${redis.port}
    scope: RUN_TIME
  - key: REDIS_USERNAME
    value: default
    scope: RUN_TIME
  - key: REDIS_PASSWORD
    value: ${redis.password}
    scope: RUN_TIME
  - key: REDIS_SSL
    value: "true"
    scope: RUN_TIME
  - key: LOG_LEVEL
    value: "INFO"
    scope: RUN_TIME
  health_check:
    http_path: /health
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
```

## Monitoring & Management

### Using the OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor

We've created a custom monitoring tool to help manage and monitor the Digital Ocean deployment:

```bash
# Make the script executable
chmod +x scripts/run_omega_do_monitor.sh

# Check deployment status
./scripts/run_omega_do_monitor.sh status

# Stream logs
./scripts/run_omega_do_monitor.sh logs

# Test Redis connection
./scripts/run_omega_do_monitor.sh redis

# Watch BTC price updates
./scripts/run_omega_do_monitor.sh watch_price

# Show resource usage statistics
./scripts/run_omega_do_monitor.sh stats
```

See `scripts/DIVINE_DO_MONITOR.md` for detailed documentation.

### Digital Ocean Console Monitoring

You can also monitor the app through the Digital Ocean web console:

1. Login to [Digital Ocean Console](https://cloud.digitalocean.com/)
2. Navigate to "Apps" and select your OMEGA BTC AI app
3. View the "Insights" tab for metrics
4. Check "Logs" for application logs
5. Use "Console" for direct access to the application container

### Health Check Endpoint

The application exposes a `/health` endpoint that returns the current status:

```bash
curl https://your-app-url.ondigitalocean.app/health
```

Example response:

```json
{
  "status": "healthy",
  "redis_connected": true,
  "websocket_connected": true,
  "last_price_update": "2023-03-27T22:15:45Z",
  "uptime": 1815.5,
  "details": {
    "last_price": 65432.10,
    "seconds_since_update": 5.2
  }
}
```

## Troubleshooting

### Redis Connection Issues

If you encounter Redis connection problems:

1. Verify environment variables are set correctly
2. Check that Redis credentials are valid
3. Ensure Redis SSL settings match your Redis provider
4. Test Redis connection using the monitor tool: `./scripts/run_omega_do_monitor.sh redis`

### Deployment Failures

If deployments fail:

1. Check the deployment logs in Digital Ocean console
2. Verify the `app.yaml` file is valid
3. Ensure all required environment variables are set
4. Check for errors in the application code
5. Try a manual deployment with `doctl apps update <app-id> --spec app.yaml`

### Application Crashes

If the application crashes or becomes unresponsive:

1. Stream logs to identify the issue: `./scripts/run_omega_do_monitor.sh logs`
2. Check the health endpoint for status
3. Restart the application from the Digital Ocean console
4. Check Redis connection and data consistency

## Maintenance

### Updating the Application

To update the deployed application:

1. Make and test your changes locally
2. Commit and push to the connected branch
3. Digital Ocean will automatically deploy the changes
4. Monitor the deployment status: `./scripts/run_omega_do_monitor.sh status`

### Scaling

To adjust application scaling:

1. Modify the `instance_count` in `app.yaml`
2. Update the app: `doctl apps update <app-id> --spec app.yaml`

Alternatively, scale through the Digital Ocean console:

1. Navigate to your app
2. Select "Settings" → "Edit" → "Resources"
3. Adjust the number of instances
4. Click "Save"

### Backups

While Digital Ocean App Platform doesn't provide built-in backups, you can:

1. Keep your code in version control
2. Regularly export important data from Redis
3. Consider implementing a scheduled backup job

### Cost Optimization

Optimize costs by:

1. Using the appropriate instance size (`basic-xxs` is usually sufficient)
2. Scaling to zero when not in use (for development environments)
3. Monitoring resource usage with `./scripts/run_omega_do_monitor.sh stats`

## BTC Live Feed v3 Deployment

The BTC Live Feed v3 component provides enhanced reliability through automatic Redis failover capabilities, ensuring 99.99% uptime even during temporary outages of the primary Redis service.

### Key Features of v3 Deployment

- **Automatic Redis Failover**: Seamlessly switches between remote (Digital Ocean) and local Redis instances
- **Health Check API**: Built-in monitoring endpoints for comprehensive system status
- **CLI Monitoring Dashboard**: Visual terminal-based monitoring tool
- **Detailed Documentation**: Comprehensive guides for deployment, configuration, and monitoring

### Deployment Files

All configuration files for deploying BTC Live Feed v3 are located in the `/deployment/digital_ocean/btc_live_feed_v3/` directory:

- `app.yaml`: Digital Ocean App Platform configuration
- `deploy.sh`: Deployment script with error handling
- `README.md`: Deployment instructions
- `redis_configuration.md`: Redis setup guide
- `monitoring_setup.md`: Monitoring configuration guide

### Deployment Process

1. Navigate to the deployment directory:

   ```bash
   cd deployment/digital_ocean/btc_live_feed_v3
   ```

2. Execute the deployment script:

   ```bash
   ./deploy.sh
   ```

For detailed deployment instructions, refer to the [BTC Live Feed v3 Deployment Guide](../deployment/digital_ocean/btc_live_feed_v3/README.md).

---

## Contact and Support

For issues with the OMEGA BTC AI deployment, contact:

- OMEGA BTC AI Development Team
- #digital-ocean channel in Discord
- Slack: #omega-btc-ai-support

---

*JAH JAH BLESS THE ETERNAL FLOW OF THE BLOCKCHAIN*

🔱 OMEGA BTC AI DIVINE COLLECTIVE 🔱
