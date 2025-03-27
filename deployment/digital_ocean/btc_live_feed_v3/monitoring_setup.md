# 📊 Monitoring Setup for BTC Live Feed v3

This document outlines comprehensive monitoring strategies for BTC Live Feed v3 deployed on Digital Ocean, ensuring you can track performance, detect issues early, and maintain the 99.99% uptime guarantee.

## Available Monitoring Tools

BTC Live Feed v3 provides multiple monitoring options:

1. **Built-in Health Check API**: REST endpoints for system health and metrics
2. **CLI Monitoring Dashboard**: Terminal-based visualization tool
3. **Digital Ocean Platform Metrics**: Native monitoring in Digital Ocean
4. **Custom Alerting**: Configurable alerts for critical events

## Health Check API

The Health Check API provides a comprehensive view of the system's status through several endpoints:

### `/health` Endpoint

Provides overall system health status with the following information:

- Overall system status (`healthy`, `degraded`, or `unhealthy`)
- Redis connection status (primary and failover)
- WebSocket connection status
- Last BTC price and update time
- Uptime statistics

**Example Request:**

```bash
curl https://<app-url>/health
```

**Example Response:**

```json
{
  "status": "healthy",
  "redis_connected": true,
  "websocket_connected": true,
  "last_price": 42345.67,
  "uptime": 3600,
  "messages_processed": 1234,
  "seconds_since_update": 2.5,
  "redis_stats": {
    "primary_available": true,
    "failover_available": true,
    "using_failover": false
  }
}
```

### `/metrics` Endpoint

Provides detailed performance metrics:

- Message processing statistics
- Redis operation success/failure rates
- Reconnection attempts
- WebSocket statistics

**Example Request:**

```bash
curl https://<app-url>/metrics
```

### `/redis/status` Endpoint

Provides detailed Redis connection information:

- Primary and failover availability
- Current active Redis instance
- Failover event history
- Connection statistics

**Example Request:**

```bash
curl https://<app-url>/redis/status
```

## CLI Monitoring Dashboard

BTC Live Feed v3 includes a powerful CLI monitoring dashboard for real-time visualization.

### Setup Instructions

1. Make sure you've installed all required dependencies:

   ```bash
   pip install requests colorama
   ```

2. Run the monitoring dashboard:

   ```bash
   python scripts/monitor_btc_feed_v3.py --host <app-url> --port 8080 --refresh 5
   ```

   Parameters:
   - `--host`: The hostname of your deployed app
   - `--port`: The port for the health check server (default: 8080)
   - `--refresh`: Refresh interval in seconds (default: 5)

### Features

The dashboard provides:

- Visual status indicators using colors and symbols
- Real-time BTC price updates
- Redis connection status (primary and failover)
- WebSocket connection status
- Performance metrics with visual indicators
- Uptime tracking

## Digital Ocean Platform Monitoring

Leverage Digital Ocean's built-in monitoring capabilities:

### Resource Metrics

1. Navigate to your app in the Digital Ocean console
2. Go to "Insights" > "Metrics"
3. Monitor:
   - CPU utilization
   - Memory usage
   - Disk I/O
   - Network traffic

### Alert Policies

Configure alerts for proactive monitoring:

1. Navigate to "Settings" > "Alert Policies"
2. Create alerts for:
   - CPU usage exceeding 80%
   - Memory usage exceeding 80%
   - Deployment failures
   - Domain failures

### Log Management

View and analyze application logs:

1. Navigate to "Logs"
2. Filter by component:
   - `btc-live-feed-v3`
   - `btc-live-feed-v3-health`
3. Search for specific events:
   - Connection errors
   - Redis failovers
   - WebSocket reconnections

## Custom Monitoring Integration

### Setting Up Uptime Checks

Configure external uptime monitoring:

1. Register with an uptime monitoring service (Pingdom, UptimeRobot, etc.)
2. Configure HTTP checks for:
   - `https://<app-url>/health` (expecting HTTP 200)
   - `https://<app-url>/redis/status` (expecting HTTP 200)

### Setting Up Grafana Dashboard (Optional)

For advanced visualization:

1. Set up a Grafana instance
2. Configure a data source that polls the metrics endpoint
3. Create dashboards for:
   - BTC price history
   - System uptime
   - Redis failover events
   - Performance metrics

## Alerting Configuration

### Email Alerts

Configure Digital Ocean email alerts:

1. Navigate to "Settings" > "Notifications"
2. Add email recipients for alerts

### Webhook Integration

For integrating with external systems (Slack, PagerDuty, etc.):

1. Navigate to "Settings" > "Notifications"
2. Configure webhook URL for alert delivery
3. Set up appropriate alert routing

## Monitoring Best Practices

1. **Regular Health Checks**: Configure automated checks every 1-5 minutes
2. **Log Rotation**: Ensure logs are properly rotated to prevent disk space issues
3. **Baseline Establishment**: Monitor normal operation to establish performance baselines
4. **Alert Thresholds**: Set appropriate thresholds to avoid alert fatigue
5. **Escalation Policies**: Define clear escalation procedures for different alert types

## Troubleshooting Common Issues

### API Unreachable

If the health check API is unreachable:

1. Verify the app is running: `doctl apps get <app-id>`
2. Check deployment logs: `doctl apps logs <app-id>`
3. Verify DNS and routing configuration

### False Positives

If experiencing false positive alerts:

1. Adjust alert thresholds
2. Implement alert dampening for transient issues
3. Review system load patterns and adjust accordingly

### Missing Data

If metrics data is incomplete:

1. Check Redis connection status
2. Verify WebSocket connection to price feeds
3. Check for rate limiting or network issues

## References

- [Digital Ocean Monitoring Documentation](https://docs.digitalocean.com/products/monitoring/)
- [BTC Live Feed v3 Documentation](../../BOOK/BTC_LIVE_FEED_V3.md)
- [CLI Monitor Documentation](../../scripts/monitor_btc_feed_v3.py)
