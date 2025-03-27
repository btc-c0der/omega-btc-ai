# OMEGA BTC AI - BTC Live Feed v3 Digital Ocean Deployment

This guide outlines the deployment process for the BTC Live Feed v3 service on Digital Ocean's App Platform, with an emphasis on the enhanced Redis failover capabilities for 99.99% uptime.

## Prerequisites

- Digital Ocean account with App Platform access
- `doctl` CLI tool installed and authenticated
- Git repository access (to push changes to the main branch)
- Redis database (Managed or self-hosted)

## Files in this Directory

- `README.md`: This guide
- `app.yaml`: Digital Ocean App Platform configuration
- `deploy.sh`: Deployment script
- `monitoring_setup.md`: Instructions for setting up monitoring
- `redis_configuration.md`: Detailed Redis configuration instructions

## Deployment Process

### 1. Deploy using the Digital Ocean web console

1. Log in to your Digital Ocean account
2. Navigate to "Apps" and click "Create App"
3. Select GitHub and the repository `btc-c0der/omega-btc-ai`
4. Choose the branch `feature/btc-live-feed-v3-resilient`
5. Select "App Platform" and upload the `app.yaml` file
6. Review the settings and click "Create Resources"

### 2. Deploy using the Digital Ocean CLI

```bash
# Navigate to the deployment directory
cd deployment/digital_ocean/btc_live_feed_v3

# Authenticate if needed
doctl auth init

# Deploy using the app.yaml file
doctl apps create --spec app.yaml

# Or use the deployment script
./deploy.sh
```

## Environment Variables

The app requires the following environment variables:

```
# Primary (Remote) Redis Configuration
REDIS_HOST=${redis.HOSTNAME}
REDIS_PORT=${redis.PORT}
REDIS_USERNAME=${redis.USERNAME}
REDIS_PASSWORD=${redis.PASSWORD}
REDIS_USE_SSL=true

# Failover (Local) Redis Configuration
FAILOVER_REDIS_HOST=localhost
FAILOVER_REDIS_PORT=6379

# Health Check Configuration
HEALTH_CHECK_PORT=8080
HEALTH_CHECK_HOST=0.0.0.0
```

## Health Check Endpoints

The service exposes health check endpoints:

- `/health` - Overall health status
- `/metrics` - Performance metrics
- `/redis/status` - Redis connection status

## Monitoring

For monitoring the deployed service:

1. Use the provided CLI monitoring tool:

```bash
python scripts/monitor_btc_feed_v3.py --host <app-url> --port 8080 --refresh 5
```

2. Set up Uptime Checks in Digital Ocean:
   - Navigate to your app in Digital Ocean console
   - Go to "Settings" > "Alert Policies"
   - Create alerts for key metrics

## Scaling

To scale the service:

```bash
doctl apps update <app-id> --spec app.yaml
```

Update the `instance_count` in the app.yaml file to increase the number of instances.

## Troubleshooting

### Common Issues

1. **Redis Connection Failures**
   - Verify Redis credentials are correctly set in environment variables
   - Check that SSL is properly configured
   - Ensure the Redis service is running

2. **Health Check Failures**
   - Review logs using `doctl apps logs <app-id> -t app`
   - Verify the health check port is correctly set and accessible

3. **Deployment Failures**
   - Check the deployment logs in Digital Ocean console
   - Verify that all dependencies are available
   - Check that the branch exists and contains the latest code

## Rollback Process

If a deployment fails or causes issues:

1. From the App Platform console:
   - Navigate to "Deployments"
   - Find the last successful deployment
   - Click "Revert to this Deployment"

2. Using the CLI:

   ```bash
   doctl apps list-deployments <app-id>
   doctl apps create-deployment <app-id> --force-rebuild
   ```

## References

- [Digital Ocean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [Digital Ocean Redis Documentation](https://docs.digitalocean.com/products/databases/redis/)
- [BTC Live Feed v3 Documentation](../../BOOK/BTC_LIVE_FEED_V3.md)
