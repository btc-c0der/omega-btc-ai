# OMEGA BTC AI - BTC Live Feed v2 Digital Ocean Deployment

This guide provides instructions for deploying the OMEGA BTC AI Bitcoin Live Feed v2 on Digital Ocean's App Platform.

## Prerequisites

- [Digital Ocean](https://www.digitalocean.com/) account with App Platform enabled
- [`doctl`](https://docs.digitalocean.com/reference/doctl/) CLI tool installed and configured
- Docker installed locally (for testing)
- Git repository access

## 1. Repository Setup

1. Clone the repository:

```bash
git clone https://github.com/fsiqueira/omega-btc-ai.git
cd omega-btc-ai
```

2. Create a deployment branch:

```bash
git checkout -b feature/btc-live-feed-v2-cloud
```

## 2. Configuration Files

The deployment uses the following files:

- `deployment/digitalocean/Dockerfile` - Container configuration
- `deployment/digitalocean/app.yaml` - Digital Ocean App Platform configuration
- `deployment/digitalocean/requirements.txt` - Python dependencies
- `deployment/scripts/deploy.sh` - Deployment script

## 3. Environment Variables

Set up the following environment variables in Digital Ocean App Platform:

| Variable | Description | Default |
|----------|-------------|---------|
| `REDIS_HOST` | Redis database host | `localhost` |
| `REDIS_PORT` | Redis database port | `6379` |
| `REDIS_PASSWORD` | Redis database password | - |
| `REDIS_SSL` | Enable SSL for Redis | `false` |
| `REDIS_SSL_CERT_REQS` | SSL certificate requirements | `required` |
| `REDIS_SSL_CERT_PATH` | Path to SSL certificate | `/app/deployment/digitalocean/certificates/SSL_redis-btc-omega-redis.pem` |
| `REDIS_SOCKET_TIMEOUT` | Redis socket timeout | `5` |
| `REDIS_SOCKET_CONNECT_TIMEOUT` | Redis connection timeout | `5` |
| `LOG_LEVEL` | Logging level | `info` |
| `DEBUG` | Enable debug logging | `false` |

## 4. Local Testing

Before deploying to Digital Ocean, test the container locally:

1. Build the Docker container:

```bash
docker build -t btc-live-feed-v2 -f deployment/digitalocean/Dockerfile .
```

2. Create a `.env` file with your configuration:

```bash
echo "REDIS_HOST=localhost" > .env
echo "REDIS_PORT=6379" >> .env
```

3. Run the container:

```bash
docker run -p 8080:8080 --env-file .env btc-live-feed-v2
```

4. Check the health endpoint:

```bash
curl http://localhost:8080/health
```

## 5. Deployment Steps

### Automated Deployment

1. Make the deployment script executable:

```bash
chmod +x deployment/scripts/deploy.sh
```

2. Run the deployment script:

```bash
./deployment/scripts/deploy.sh
```

### Manual Deployment

1. Install and authenticate `doctl`:

```bash
# Install doctl
brew install doctl

# Authenticate with Digital Ocean
doctl auth init
```

2. Create a Redis database in Digital Ocean:

```bash
doctl databases create redis-btc-feed --engine redis --version 6 --region sfo3 --size db-s-1vcpu-1gb
```

3. Deploy the application:

```bash
doctl apps create --spec deployment/digitalocean/app.yaml
```

## 6. Monitoring and Maintenance

### Viewing Application Logs

```bash
# List your apps
doctl apps list

# View logs (replace APP_ID with your app's ID)
doctl apps logs APP_ID
```

### Health Checks

The application provides a health check endpoint at `/health` that returns the system status:

```bash
# Replace APP_URL with your application's URL
curl https://APP_URL/health
```

The health check verifies:

- Redis connection status
- WebSocket connection to Binance
- Last price update time
- System uptime

### Updating the Application

1. Make changes to your code
2. Push to the deployment branch:

```bash
git add .
git commit -m "Update BTC Live Feed v2"
git push origin feature/btc-live-feed-v2-cloud
```

3. Digital Ocean will automatically redeploy the application

## 7. Troubleshooting

### Common Issues

1. **Redis Connection Failures**
   - Verify Redis credentials are correct
   - Check SSL certificate configuration
   - Ensure firewall rules allow connections to Redis

2. **WebSocket Connection Issues**
   - Check Internet connectivity
   - Verify Binance API status
   - Review WebSocket connection parameters

3. **Deployment Failures**
   - Check the app logs for errors
   - Ensure all required environment variables are set
   - Verify the Dockerfile and app.yaml are valid

### Rollback Procedure

To roll back to a previous version:

```bash
# Reset to a previous commit
git checkout feature/btc-live-feed-v2-cloud
git reset --hard COMMIT_HASH
git push --force origin feature/btc-live-feed-v2-cloud
```

## 8. Security Considerations

1. **Redis Security**
   - Use SSL connections to Redis
   - Set strong Redis passwords
   - Restrict Redis access to necessary IPs

2. **API Security**
   - Implement rate limiting for the health check endpoint
   - Validate all incoming data
   - Do not expose sensitive information in logs

## 9. Performance Optimization

For better performance, consider:

1. **Scaling**
   - Increase instance size for vertical scaling
   - Increase instance count for horizontal scaling

2. **Redis Optimization**
   - Use Redis pipeline operations for batch updates
   - Consider Redis cluster for higher throughput

## 10. Support and Resources

- [Digital Ocean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [Redis Documentation](https://redis.io/documentation)
- [Binance API Documentation](https://developers.binance.com/docs/binance-api/websocket_api)

---

*Last updated: 2024-04-04*
