# 🌊 DigitalOcean Deployment Guide for OMEGA BTC AI WebSocket Server

## Divine Prerequisites

- DigitalOcean account with API access
- `doctl` CLI tool installed
- Docker installed locally
- Access to Redis credentials

## Cosmic Configuration

### 1. Environment Setup

```bash
# Install doctl if not already installed
brew install doctl

# Authenticate with DigitalOcean
doctl auth init
```

### 2. Project Structure

```
omega-btc-ai/
├── Dockerfile
├── docker-compose.yml
├── .env
└── app.yaml
```

### 3. Dockerfile Configuration

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose WebSocket port
EXPOSE 8765

# Run the WebSocket server
CMD ["python", "-m", "omega_ai.mm_trap_detector.mm_websocket_server"]
```

### 4. Docker Compose Configuration

```yaml
version: '3.8'

services:
  websocket:
    build: .
    ports:
      - "8765:8765"
    environment:
      - REDIS_HOST=${REDIS_HOST}
      - REDIS_PORT=${REDIS_PORT}
      - REDIS_USERNAME=${REDIS_USERNAME}
      - REDIS_PASSWORD=${REDIS_PASSWORD}
      - REDIS_USE_TLS=${REDIS_USE_TLS}
      - REDIS_CERT=${REDIS_CERT}
    restart: always
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8765/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### 5. DigitalOcean App Platform Configuration

```yaml
name: omega-btc-ai-websocket
services:
- name: websocket
  github:
    branch: main
    deploy_on_push: true
    repo: your-username/omega-btc-ai
  health_check:
    http_path: /health
  http_port: 8765
  instance_count: 2
  instance_size_slug: basic-xxs
  run_command: python -m omega_ai.mm_trap_detector.mm_websocket_server
  envs:
  - key: REDIS_HOST
    value: ${REDIS_HOST}
  - key: REDIS_PORT
    value: ${REDIS_PORT}
  - key: REDIS_USERNAME
    value: ${REDIS_USERNAME}
  - key: REDIS_PASSWORD
    value: ${REDIS_PASSWORD}
  - key: REDIS_USE_TLS
    value: ${REDIS_USE_TLS}
  - key: REDIS_CERT
    value: ${REDIS_CERT}
databases:
- engine: REDIS
  name: omega-redis
  production: false
  version: "6"
```

## Divine Deployment Steps

1. **Initialize DigitalOcean Project**

```bash
# Create new project
doctl projects create --name omega-btc-ai

# Get project ID
PROJECT_ID=$(doctl projects list --format ID,Name | grep omega-btc-ai | awk '{print $1}')
```

2. **Create Redis Database**

```bash
# Create Redis database
doctl databases create omega-redis --engine REDIS --version 6

# Get database connection details
doctl databases connection omega-redis
```

3. **Deploy Application**

```bash
# Deploy to DigitalOcean App Platform
doctl apps create --spec app.yaml

# Get app ID
APP_ID=$(doctl apps list --format ID,Name | grep omega-btc-ai-websocket | awk '{print $1}')

# Deploy updates
doctl apps update $APP_ID --spec app.yaml
```

4. **Configure Domain**

```bash
# Add custom domain
doctl apps update $APP_ID --spec app.yaml --domain your-domain.com
```

## Divine Monitoring

### Health Checks

```bash
# Check app status
doctl apps get $APP_ID

# View logs
doctl apps logs $APP_ID
```

### Scaling

```bash
# Scale horizontally
doctl apps update $APP_ID --spec app.yaml --instance-count 3
```

## Divine Security

1. **SSL/TLS**

- Automatically handled by DigitalOcean
- Certificates managed through Let's Encrypt

2. **Firewall Rules**

```bash
# Create firewall
doctl compute firewall create --name omega-firewall

# Add rules
doctl compute firewall add-rules omega-firewall \
  --inbound-rules "protocol:tcp,ports:8765,address:0.0.0.0/0"
```

## Divine Maintenance

### Updates

```bash
# Pull latest changes
git pull origin main

# Deploy updates
doctl apps update $APP_ID --spec app.yaml
```

### Backup

```bash
# Backup Redis database
doctl databases backup omega-redis
```

## Divine Troubleshooting

1. **Connection Issues**

```bash
# Check WebSocket logs
doctl apps logs $APP_ID --type websocket

# Verify Redis connection
doctl databases connection omega-redis
```

2. **Performance Issues**

```bash
# Monitor resources
doctl monitoring alert policy create \
  --type v1/insights/droplet/cpu \
  --description "High CPU Usage" \
  --comparison greater_than \
  --value 80 \
  --window 5m
```

## Divine Cost Management

1. **Resource Optimization**

- Monitor usage through DigitalOcean dashboard
- Scale down during low-traffic periods
- Use appropriate instance sizes

2. **Budget Alerts**

```bash
# Set up billing alerts
doctl billing-history list
```

## Divine References

- [DigitalOcean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [DigitalOcean Redis Documentation](https://docs.digitalocean.com/products/databases/redis/)
- [DigitalOcean CLI Documentation](https://docs.digitalocean.com/reference/doctl/)
