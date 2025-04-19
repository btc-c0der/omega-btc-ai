
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


# OMEGA BTC AI - BTC Live Feed v2 Digital Ocean Deployment

This guide outlines the deployment process for the BTC Live Feed v2 service on Digital Ocean's App Platform.

## Deployment Requirements

- Digital Ocean account with App Platform access
- Access to the GitHub repository (btc-c0der/omega-btc-ai)
- Redis Cloud instance with TLS enabled

## Deployment Files

The following files are used in the deployment process:

- `app.yaml`: Digital Ocean App Platform configuration
- `requirements.txt`: Python dependencies
- `runtime.txt`: Python version specification
- `Procfile`: Process type definitions
- `certificates/SSL_redis-btc-omega-redis.pem`: Redis TLS certificate

## Deployment Process

1. Ensure all configuration files are in place:
   - Check `app.yaml` for proper environment variables
   - Verify Redis connection details are correct
   - Ensure SSL certificates are properly configured

2. Deploy using the Digital Ocean CLI:

   ```bash
   doctl apps create --spec deployment/digitalocean/app.yaml
   ```

3. Monitor the deployment:

   ```bash
   doctl apps list
   ```

4. Get deployment details:

   ```bash
   doctl apps get [APP_ID]
   ```

5. View logs:

   ```bash
   doctl apps logs [APP_ID]
   ```

## Environment Variables

The following environment variables must be configured:

| Variable | Description | Example |
|----------|-------------|---------|
| REDIS_HOST | Redis server hostname | redis-12345.example.redislabs.com |
| REDIS_PORT | Redis server port | 12345 |
| REDIS_USERNAME | Redis username | omega |
| REDIS_PASSWORD | Redis password | your_password |
| REDIS_SSL | Enable SSL | true |
| REDIS_USE_TLS | Use TLS | true |
| REDIS_CERT | Certificate file name | SSL_redis-btc-omega-redis.pem |
| REDIS_SSL_CERT_REQS | Certificate validation | required |
| REDIS_SSL_CERT_PATH | Path to certificate | /app/deployment/digitalocean/certificates/SSL_redis-btc-omega-redis.pem |
| REDIS_SOCKET_TIMEOUT | Socket timeout in seconds | 5 |
| REDIS_SOCKET_CONNECT_TIMEOUT | Connection timeout in seconds | 5 |
| LOG_LEVEL | Logging level | info |
| DEBUG | Enable debug mode | false |

## Troubleshooting

- **Build Failures**: Check the build log for dependency issues. You may need to update the `requirements.txt` file.
- **Runtime Errors**: Review app logs for more details about runtime errors.
- **Redis Connection Issues**: Verify the Redis environment variables and certificate path.
- **Health Check Failures**: The application exposes a health check endpoint at `/health`. Verify it's responding correctly.

## Monitoring

The application exposes a health check endpoint at `/health` that returns:

```json
{
  "status": "healthy",
  "redis_connected": true,
  "websocket_connected": true,
  "last_price_update": "2025-03-27T19:30:15.123456Z",
  "uptime": 3600.5,
  "details": {
    "last_price": 65432.10,
    "seconds_since_update": 5.2,
    "uptime_seconds": 3600.5
  }
}
```

## Updating the Application

1. Make changes to your code in the repository
2. Push changes to the `feature/btc-live-feed-v2-cloud` branch
3. Digital Ocean will automatically rebuild and deploy the application

## Rollback

To roll back to a previous deployment:

```bash
doctl apps list-deployments [APP_ID]
doctl apps create-deployment [APP_ID] --force-rebuild
```

## Security Notes

- Ensure Redis credentials are kept secure
- Validate that the TLS certificate is properly configured
- Check that websocket connections are using secure protocols
- Set appropriate rate limits and timeouts to prevent DoS attacks

## 10. Support and Resources

- [Digital Ocean App Platform Documentation](https://docs.digitalocean.com/products/app-platform/)
- [Redis Documentation](https://redis.io/documentation)
- [Binance API Documentation](https://developers.binance.com/docs/binance-api/websocket_api)

---

*Last updated: 2024-04-04*
