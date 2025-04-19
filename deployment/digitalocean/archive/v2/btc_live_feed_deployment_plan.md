
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


# OMEGA BTC AI - BTC Live Feed v2 Digital Ocean Deployment Plan

## 1. Deployment Architecture Overview

```
                   ┌─────────────────┐
                   │  Digital Ocean  │
                   │  App Platform   │
                   └────────┬────────┘
                            │
                            ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Docker    │◄────►│   BTC Live  │◄────►│   Redis DB   │
│   Container │      │   Feed v2   │      │   (Managed)  │
└─────────────┘      └─────────────┘      └─────────────┘
                            │
                            ▼
                    ┌─────────────────┐
                    │   Binance API   │
                    │   WebSockets    │
                    └─────────────────┘
```

## 2. Prerequisites

- Digital Ocean account with App Platform enabled
- `doctl` CLI tool installed and configured
- Docker installed locally for testing
- Access to OMEGA BTC AI repository
- SSL certificates for secure Redis connections

## 3. Repository Structure

Ensure the following files are prepared:

```
deployment/
  ├── digitalocean/
  │   ├── Dockerfile           # Container configuration
  │   ├── app.yaml             # App Platform configuration
  │   ├── requirements.txt     # Python dependencies
  │   └── certificates/        # SSL certificates for Redis
  └── scripts/
      ├── deploy.sh            # Deployment script
      └── healthcheck.sh       # Health check script
```

## 4. Docker Configuration

### Dockerfile

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Expose port for health check
EXPOSE 8080

# Run the application
CMD ["python", "-m", "omega_ai.data_feed.btc_live_feed_v2"]
```

## 5. Environment Variables

Configure the following environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| REDIS_HOST | Redis database host | redis-host |
| REDIS_PORT | Redis database port | 6379 |
| REDIS_PASSWORD | Redis database password | securepassword |
| REDIS_SSL | Enable SSL for Redis | true |
| REDIS_SSL_CERT_REQS | SSL certificate requirements | required |
| REDIS_SSL_CERT_PATH | Path to SSL certificate | /app/deployment/digitalocean/certificates/SSL_redis-btc-omega-redis.pem |
| REDIS_SOCKET_TIMEOUT | Redis socket timeout | 5 |
| REDIS_SOCKET_CONNECT_TIMEOUT | Redis connection timeout | 5 |
| DEBUG | Enable debug logging | false |
| LOG_LEVEL | Logging level | info |

## 6. Health Checks

Implement a health check endpoint at `/health` that verifies:

1. Connection to Binance WebSocket is active
2. Redis connection is functional
3. Price data is being received and stored

## 7. Digital Ocean App Platform Configuration

### app.yaml

```yaml
name: omega-btc-live-feed-v2
services:
- name: btc-live-feed
  github:
    branch: feature/btc-live-feed-v2-cloud
    deploy_on_push: true
    repo: fsiqueira/omega-btc-ai
  build_command: pip install -r requirements.txt
  run_command: python -m omega_ai.data_feed.btc_live_feed_v2
  envs:
  - key: REDIS_HOST
    value: ${redis.REDIS_HOST}
  - key: REDIS_PORT
    value: ${redis.REDIS_PORT}
  - key: REDIS_PASSWORD
    value: ${redis.REDIS_PASSWORD}
  - key: REDIS_SSL
    value: "true"
  - key: REDIS_SSL_CERT_REQS
    value: "required"
  - key: REDIS_SSL_CERT_PATH
    value: "/app/deployment/digitalocean/certificates/SSL_redis-btc-omega-redis.pem"
  - key: REDIS_SOCKET_TIMEOUT
    value: "5"
  - key: REDIS_SOCKET_CONNECT_TIMEOUT
    value: "5"
  instance_count: 1
  instance_size_slug: basic-xxs
  health_check:
    http_path: /health
    initial_delay_seconds: 10
    period_seconds: 60

databases:
- engine: REDIS
  name: redis
  production: false
  version: "6"
```

## 8. Deployment Steps

### 8.1 Preparing for Deployment

1. Create a deployment branch:

```bash
git checkout -b feature/btc-live-feed-v2-cloud
```

2. Build and test Docker container locally:

```bash
docker build -t btc-live-feed-v2 -f deployment/digitalocean/Dockerfile .
docker run -p 8080:8080 --env-file deployment/digitalocean/.env btc-live-feed-v2
```

3. Create necessary Redis database on Digital Ocean:

```bash
doctl databases create redis-btc-feed --engine redis --version 6 --region sfo3 --size db-s-1vcpu-1gb
```

### 8.2 Automated Deployment Script

Create `deployment/scripts/deploy.sh`:

```bash
#!/bin/bash

# OMEGA BTC AI - Digital Ocean Deployment Script
# ==============================================

# Set error handling
set -e

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RESET='\033[0m'

echo -e "${YELLOW}=== OMEGA BTC AI - Digital Ocean Deployment ===${RESET}"

# Check if doctl is installed
if ! command -v doctl &> /dev/null; then
    echo -e "${RED}Error: doctl not found. Please install the Digital Ocean CLI.${RESET}"
    exit 1
fi

# Check authentication
echo -e "${YELLOW}Checking Digital Ocean authentication...${RESET}"
if ! doctl account get &> /dev/null; then
    echo -e "${RED}Error: Not authenticated with Digital Ocean.${RESET}"
    echo "Run 'doctl auth init' to authenticate."
    exit 1
fi

# Deploy the application
echo -e "${YELLOW}Deploying to Digital Ocean App Platform...${RESET}"
doctl apps create --spec deployment/digitalocean/app.yaml

echo -e "${GREEN}Deployment initiated! Monitor status with 'doctl apps list'${RESET}"
```

Make the script executable:

```bash
chmod +x deployment/scripts/deploy.sh
```

### 8.3 Executing Deployment

1. Push changes to GitHub:

```bash
git add .
git commit -m "Prepare BTC Live Feed v2 for Digital Ocean deployment"
git push origin feature/btc-live-feed-v2-cloud
```

2. Run deployment script:

```bash
./deployment/scripts/deploy.sh
```

3. Monitor deployment:

```bash
doctl apps list
doctl apps get <app-id>
```

## 9. Monitoring & Maintenance

### 9.1 Monitoring

1. Application logs:

```bash
doctl apps logs <app-id>
```

2. Set up alerts for:
   - High resource utilization
   - Connection failures to Binance WebSocket
   - Redis connection issues
   - Stale price data (no updates for >5 minutes)

### 9.2 Maintenance Tasks

Create a maintenance schedule:

1. **Daily**: Check application logs for errors
2. **Weekly**: Check for dependency updates
3. **Monthly**: Review and optimize resource usage

### 9.3 Backup Strategy

1. Configure Redis database backups with Digital Ocean
2. Implement periodic exports of critical price data

## 10. Rollback Procedures

In case of deployment failures:

1. Roll back to previous version:

```bash
git checkout <previous-commit>
git push origin feature/btc-live-feed-v2-cloud --force
```

2. Manual rollback on Digital Ocean:

```bash
doctl apps update <app-id> --spec deployment/digitalocean/app.yaml
```

## 11. Security Considerations

1. Secure Redis connection with SSL
2. Implement proper validation of WebSocket messages
3. Set connection timeouts to prevent resource exhaustion
4. Validate price data to prevent malicious inputs
5. Ensure Docker container runs with minimal privileges

## 12. Performance Optimization

1. Configure appropriate instance size based on usage patterns
2. Implement rate limiting for Redis connections
3. Optimize Python dependencies to reduce container size
4. Implement caching strategies for frequently accessed data

## 13. Scaling Strategy

1. Increase instance size for vertical scaling:

```yaml
instance_size_slug: basic-s # Upgrade from basic-xxs
```

2. Enable horizontal scaling for high availability:

```yaml
instance_count: 2 # Increase from 1
```

## 14. Testing Strategy

1. Unit tests for each component
2. Integration tests for Redis connections
3. End-to-end tests with mock WebSocket data
4. Load testing to ensure stability under high traffic

## 15. Documentation

Maintain documentation for:

- Deployment procedures
- Monitoring guidelines
- Troubleshooting common issues
- Configuration parameters

## 16. Cost Estimation

| Resource | Size | Monthly Cost |
|----------|------|--------------|
| App Platform (basic-xxs) | 1 instance | ~$5 |
| Redis Database (1GB) | 1 instance | ~$15 |
| **Total Estimated Cost** | | **~$20/month** |

## 17. Next Steps

1. Implement CI/CD pipeline for automated testing and deployment
2. Set up comprehensive monitoring with Prometheus and Grafana
3. Develop a disaster recovery plan
4. Optimize Docker container for faster startup times
