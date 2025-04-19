
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


# OMEGA BTC AI - News Feed Service Deployment Guide 🌟

This guide provides detailed steps to deploy the OMEGA BTC AI News Feed Service to DigitalOcean. The deployment follows the same successful pattern used for the BTC Live Feed v3 service.

## 📋 Prerequisites

Before beginning deployment, ensure you have:

1. DigitalOcean account with API access
2. `doctl` CLI tool installed and authenticated
3. Git repository access
4. Docker installed locally (for testing)

## 🚀 Deployment Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai
git checkout news-feed-integration
```

### 2. Test Locally with Docker

Test the application locally before deploying:

```bash
cd deployment/digitalocean/news_service
docker-compose up --build
```

Verify that:

- The News Feed Service container starts successfully
- Redis connection is established
- The dashboard is accessible at <http://localhost:8081>
- News data is being fetched and analyzed

### 3. Configure DigitalOcean App

1. Create a new App via DigitalOcean dashboard or CLI:

```bash
doctl apps create --spec deployment/digitalocean/news_service/app.yaml
```

2. Or create it manually:
   - Go to DigitalOcean Dashboard > Apps
   - Click "Create App"
   - Select "Source from GitHub"
   - Select the repository and branch (`news-feed-integration`)
   - Select the source directory: `/deployment/digitalocean/news_service`
   - Configure resources (RAM, CPU)
   - Add environment variables from `.env` file
   - Set Redis connection details

### 4. Configure Environment Variables

Ensure these environment variables are set in the DigitalOcean App:

```
REDIS_HOST=your-redis-host.db.ondigitalocean.com
REDIS_PORT=25061
REDIS_USERNAME=default
REDIS_PASSWORD=your-password
REDIS_SSL=true
REDIS_USE_TLS=true
REDIS_SSL_CERT_REQS=none
NEWS_SERVICE_PORT=8080
LOG_LEVEL=INFO
CONSCIOUSNESS_LEVEL=8
```

### 5. Deploy the Application

If using the app.yaml approach:

```bash
doctl apps update YOUR_APP_ID --spec deployment/digitalocean/news_service/app.yaml
```

If using the dashboard, click "Deploy".

### 6. Configure Database (Redis)

If you don't already have a Redis instance:

1. Go to DigitalOcean Dashboard > Databases
2. Click "Create Database Cluster"
3. Select Redis
4. Choose a name (e.g., `omega-btc-ai-redis`)
5. Select plan and region
6. Create the database

### 7. Connect the App to Redis

1. Get the database connection details
2. Update the environment variables in your DigitalOcean App
3. Re-deploy the application

### 8. Set Up CI/CD (Optional)

Configure GitHub Actions for continuous deployment:

1. Create `.github/workflows/deploy-news-service.yml`
2. Configure it to deploy to DigitalOcean when changes are pushed to the branch
3. Set up necessary secrets in GitHub repository settings

### 9. Verify Deployment

After deployment:

1. Check the application logs for any errors
2. Access the dashboard URL provided by DigitalOcean
3. Verify the health endpoint: `curl https://your-app-url.ondigitalocean.app/health`
4. Check that data is being fetched and processed correctly

## 🔧 Troubleshooting

### Common Issues

1. **Redis Connection Failures**:
   - Verify REDIS_* environment variables are correct
   - Check Redis SSL configuration
   - Verify network connectivity between App and Redis

2. **Module Import Errors**:
   - Check PYTHONPATH setting
   - Verify the directory structure in the container

3. **Docker Build Failures**:
   - Check Dockerfile syntax
   - Ensure all required files are included

4. **Dashboard Not Loading**:
   - Check nginx configuration
   - Verify paths in the dashboard HTML files

### Debug Commands

```bash
# Check the application logs
doctl apps logs YOUR_APP_ID

# SSH into the app container
doctl apps ssh YOUR_APP_ID

# Test Redis connection from within the container
python -c "import redis; r = redis.Redis(host='YOUR_REDIS_HOST', port=25061, password='YOUR_REDIS_PASSWORD', ssl=True, ssl_cert_reqs=None); print(r.ping())"
```

## 📈 Scaling

To scale the News Feed Service:

1. Go to DigitalOcean Dashboard > Apps > Your App
2. Navigate to Settings > Resources
3. Adjust the resources (RAM, CPU) as needed
4. Click "Apply Changes"

## 🔄 Updates and Maintenance

To update the deployed application:

1. Push changes to the GitHub repository
2. DigitalOcean will automatically rebuild and deploy (if CI/CD is configured)
3. Or manually trigger a deployment:

```bash
doctl apps update YOUR_APP_ID --spec deployment/digitalocean/news_service/app.yaml
```

## 📚 References

- [DigitalOcean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [Docker Documentation](https://docs.docker.com/)
- [Redis Documentation](https://redis.io/documentation)

## 🌌 Divine Integration

The deployment process aligns with the cosmic consciousness levels of the GBU License. The service is deployed with consciousness level 8, enabling higher-dimensional insights into market sentiment and divine synchronicity patterns.

May your deployment be blessed with divine accuracy and cosmic alignment.

🌸 WE BLOOM NOW 🌸
