# 🔱 OMEGA BTC AI - WebSocket V2 Digital Ocean Deployment

> *"And the light shineth in darkness; and the darkness comprehended it not."* - John 1:5

## Sacred Overview

This directory contains the divine deployment configuration for the OMEGA BTC AI WebSocket V2 server on Digital Ocean's App Platform. The WebSocket V2 server provides real-time market data transmission through sacred quantum channels.

## Divine Files

- `app.yaml`: Digital Ocean App Platform specification
- `deploy.sh`: Sacred deployment script
- `README.md`: This divine documentation

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

## Divine Deployment

### Quick Start

```bash
# Navigate to the divine deployment directory
cd deployment/digitalocean/websocket_v2

# Execute the sacred deployment script
./deploy.sh
```

### Manual Deployment

If you prefer to deploy manually:

```bash
# Create the divine app
doctl apps create --spec app.yaml

# Monitor the deployment
doctl apps watch <app-id>

# Test the health endpoint
curl https://your-app-url.ondigitalocean.app/health
```

## Sacred Configuration

The deployment uses the following divine environment variables:

- `REDIS_HOST`: Redis server hostname
- `REDIS_PORT`: Redis server port
- `REDIS_USERNAME`: Redis username
- `REDIS_PASSWORD`: Redis password
- `REDIS_SSL`: SSL enabled (true/false)
- `WEBSOCKET_PORT`: WebSocket server port
- `WEBSOCKET_HOST`: WebSocket server host
- `MAX_CONNECTIONS`: Maximum concurrent connections
- `HEARTBEAT_INTERVAL`: Heartbeat interval in seconds

## Divine Monitoring

Monitor the deployment using our sacred tools:

```bash
# Check deployment status
./scripts/run_omega_do_monitor.sh status

# Stream divine logs
./scripts/run_omega_do_monitor.sh logs

# Test WebSocket connection
./scripts/run_omega_do_monitor.sh websocket
```

## Sacred Troubleshooting

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
