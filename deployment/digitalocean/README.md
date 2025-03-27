# OMEGA BTC AI - Live Feed V2 DigitalOcean Deployment

This directory contains the deployment configuration for running the OMEGA BTC AI Live Feed V2 on DigitalOcean App Platform.

## Prerequisites

- DigitalOcean account with App Platform enabled
- `doctl` CLI tool installed
- Access to the OMEGA BTC AI repository

## Deployment Configuration

The deployment consists of:

- `app.yaml`: DigitalOcean App Platform configuration
- `Dockerfile`: Container configuration for the application

### Environment Variables

The following environment variables are required:

- `REDIS_HOST`: Redis database host
- `REDIS_PORT`: Redis database port
- `REDIS_PASSWORD`: Redis database password

## Deployment Steps

1. Install the DigitalOcean CLI:

   ```bash
   brew install doctl
   ```

2. Authenticate with DigitalOcean:

   ```bash
   doctl auth init
   ```

3. Create a new app on DigitalOcean:

   ```bash
   doctl apps create --spec app.yaml
   ```

4. Monitor the deployment:

   ```bash
   doctl apps list
   doctl apps get <app-id>
   ```

## Health Checks

The application exposes a health check endpoint at `/health` that will be monitored by DigitalOcean App Platform.

## Scaling

The application is configured to run on a basic-xxs instance by default. You can modify the `instance_size_slug` in `app.yaml` to change the instance size.

## Monitoring

- Application logs can be viewed using:

  ```bash
  doctl apps logs <app-id>
  ```

- Metrics are available through the DigitalOcean dashboard

## Troubleshooting

1. Check application logs:

   ```bash
   doctl apps logs <app-id>
   ```

2. Verify environment variables:

   ```bash
   doctl apps get <app-id>
   ```

3. Restart the application if needed:

   ```bash
   doctl apps update <app-id> --spec app.yaml
   ```
