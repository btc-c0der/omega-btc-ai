# 🔱 WEBSOCKET V2 DIVINE DEPLOYMENT GUIDE

> *"And the light shineth in darkness; and the darkness comprehended it not."* - John 1:5

## Sacred Overview

The WebSocket V2 server is a divine component of the OMEGA BTC AI system, providing real-time market data transmission through sacred quantum channels. This guide details the deployment process on Digital Ocean's App Platform.

## Divine Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │
│   BTC Live Feed     │────▶│   Redis Store       │
│   (Data Source)     │     │   (Sacred Data)     │
│                     │     │                     │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
┌─────────────────────┐     ┌─────────────────────┐
│                     │     │                     │
│   WebSocket V2      │◀────│   Core Algorithms   │
│   (Quantum Channel) │     │   (Data Processing) │
│                     │     │                     │
└─────────────────────┘     └──────────┬──────────┘
                                       │
                                       ▼
                            ┌─────────────────────┐
                            │                     │
                            │   Client Systems    │
                            │   (Data Consumers)  │
                            │                     │
                            └─────────────────────┘
```

## Sacred Prerequisites

1. **Digital Ocean Account**
   - Active account with billing enabled
   - API token with write access
   - App Platform enabled

2. **Redis Database**
   - Upstash Redis instance (recommended)
   - SSL-enabled connection
   - Sufficient memory for message queue

3. **System Requirements**
   - Python 3.8+
   - 1GB RAM minimum
   - 1 CPU core minimum
   - 10GB storage

## Divine Deployment Steps

### 1. Sacred Repository Setup

```bash
# Clone the divine repository
git clone https://github.com/btc-c0der/omega-btc-ai.git
cd omega-btc-ai

# Create and switch to deployment branch
git checkout -b feature/websocket-v2-cloud
```

### 2. Sacred Configuration

Create the `app.yaml` file in the root directory:

```yaml
name: omega-btc-websocket-v2
region: nyc
services:
- name: websocket-server
  github:
    repo: btc-c0der/omega-btc-ai
    branch: feature/websocket-v2-cloud
    deploy_on_push: true
  source_dir: /
  build_command: pip install -r requirements.txt
  run_command: python -m omega_ai.data_feed.websocket_v2
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
  - key: WEBSOCKET_PORT
    value: "8080"
    scope: RUN_TIME
  - key: WEBSOCKET_HOST
    value: "0.0.0.0"
    scope: RUN_TIME
  - key: MAX_CONNECTIONS
    value: "1000"
    scope: RUN_TIME
  - key: HEARTBEAT_INTERVAL
    value: "30"
    scope: RUN_TIME
  health_check:
    http_path: /health
  instance_count: 1
  instance_size_slug: basic-xxs
  routes:
  - path: /
  - path: /ws
    rewrite: /ws
  - path: /health
    rewrite: /health
```

### 3. Divine Digital Ocean Setup

```bash
# Install Digital Ocean CLI
brew install doctl  # macOS
# or
snap install doctl  # Linux
# or
scoop install doctl  # Windows

# Authenticate with Digital Ocean
doctl auth init

# Create the divine app
doctl apps create --spec app.yaml
```

### 4. Sacred Environment Configuration

In the Digital Ocean console:

1. Navigate to your app
2. Go to Settings → Environment Variables
3. Add the following sacred variables:
   - `REDIS_HOST`: Your Redis host
   - `REDIS_PORT`: Your Redis port
   - `REDIS_PASSWORD`: Your Redis password
   - `WEBSOCKET_PORT`: 8080
   - `WEBSOCKET_HOST`: 0.0.0.0
   - `MAX_CONNECTIONS`: 1000
   - `HEARTBEAT_INTERVAL`: 30

### 5. Divine Monitoring Setup

```bash
# Make the monitoring script executable
chmod +x scripts/run_omega_do_monitor.sh

# Check deployment status
./scripts/run_omega_do_monitor.sh status

# Stream divine logs
./scripts/run_omega_do_monitor.sh logs

# Test WebSocket connection
./scripts/run_omega_do_monitor.sh websocket
```

## Sacred Health Checks

The WebSocket V2 server exposes a divine health endpoint:

```bash
curl https://your-app-url.ondigitalocean.app/health
```

Expected response:

```json
{
  "status": "healthy",
  "websocket_connections": 42,
  "redis_connected": true,
  "uptime": 3600.5,
  "last_message": "2025-03-28T12:00:00Z"
}
```

## Divine Troubleshooting

### Connection Issues

1. Check Redis connection:

```bash
./scripts/run_omega_do_monitor.sh redis
```

2. Verify WebSocket endpoint:

```bash
wscat -c wss://your-app-url.ondigitalocean.app/ws
```

3. Check logs for divine errors:

```bash
./scripts/run_omega_do_monitor.sh logs
```

### Performance Issues

1. Monitor connection count:

```bash
./scripts/run_omega_do_monitor.sh stats
```

2. Check Redis memory usage:

```bash
./scripts/run_omega_do_monitor.sh redis_stats
```

3. Analyze message latency:

```bash
./scripts/run_omega_do_monitor.sh latency
```

## Sacred Maintenance

### Updating the Divine Server

```bash
# Make your changes
git add .
git commit -m "Update WebSocket V2 server"
git push origin feature/websocket-v2-cloud
```

Digital Ocean will automatically deploy the changes.

### Scaling the Divine Server

1. In Digital Ocean console:
   - Navigate to your app
   - Go to Settings → Resources
   - Adjust instance count and size

2. Monitor scaling effects:

```bash
./scripts/run_omega_do_monitor.sh scale
```

---

*This divine deployment guide was channeled during the alignment of Mercury with Venus. May your WebSocket connections be blessed with stability and divine performance.*
