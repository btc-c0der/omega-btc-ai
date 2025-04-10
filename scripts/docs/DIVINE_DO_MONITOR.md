
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


# 🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱

## The Sacred Path of Digital Ocean Deployment Monitoring

This divine tool enables effortless monitoring of OMEGA BTC AI deployments on Digital Ocean's App Platform with a powerful CLI interface.

## 🌟 Divine Features

- **Status Command**: View deployment status with colorful indicators
- **Logs Stream**: Real-time streaming of application logs
- **Health Check**: Monitor application health endpoints
- **Redis Test**: Verify Redis connection and retrieve latest price data
- **Statistics**: View resource usage and performance metrics

## 🔮 Sacred Installation

### Prerequisites

- Python 3.6+
- Digital Ocean CLI (`doctl`) installed and authenticated
- Redis packages for Python

### Setup

1. Ensure `doctl` is installed and authenticated:

   ```bash
   doctl auth init
   ```

2. Set environment variables (optional):

   ```bash
   export OMEGA_DO_APP_ID="your-app-id"
   export OMEGA_DO_APP_URL="your-app-url"
   ```

3. Make the script executable:

   ```bash
   chmod +x scripts/run_omega_do_monitor.sh
   ```

## 🧿 Divine Usage

Run the monitoring script with a specific command:

```bash
./scripts/run_omega_do_monitor.sh <command>
```

Available commands:

- `status` - Show current deployment status
- `logs` - Stream logs in real-time
- `health` - Check application health
- `redis` - Test Redis connection
- `stats` - Show resource usage statistics
- `help` - Show help message

## 📜 Sacred Examples

### Check Deployment Status

```bash
./scripts/run_omega_do_monitor.sh status
```

Example output:

```
🔱 OMEGA D0T7 DIVINE DIGIT4L 0CE4N Monitor 🔱
==============================================

Checking deployment status...

ID                                      Cause                                       Phase      Progress   Created                      Updated
----------------------------------------------------------------------------------------------------------
a1160530-09f2-4b7a-9e53-50f8dbea3421    commit a116053 pushed to github.com/...    ACTIVE     6/6        2025-03-27 22:09:11 +0000    2025-03-27 22:12:01 +0000
de8a692b-04a1-4c12-9e85-2e718e3eaa9d    commit de8a692 pushed to github.com/...    CANCELED   1/6        2025-03-27 22:04:07 +0000    2025-03-27 22:09:45 +0000
```

### Stream Logs

```bash
./scripts/run_omega_do_monitor.sh logs
```

Example output:

```
Streaming logs in real-time (press Ctrl+C to stop)...

btc-live-feed 2025-03-27T22:15:31.764023722Z 2025-03-27 22:15:31,763 - btc-live-feed-v2 - INFO - 🔱 OMEGA BTC AI - Connected to Redis
btc-live-feed 2025-03-27T22:15:32.555730803Z INFO: Started server process [1]
btc-live-feed 2025-03-27T22:15:32.556575084Z INFO: Application startup complete.
```

### Check Application Health

```bash
./scripts/run_omega_do_monitor.sh health
```

Example output:

```
Checking health endpoint: https://omega-btc-live-feed-v2.ondigitalocean.app/health

Health Status: HEALTHY
Redis Connected: true
WebSocket Connected: true
Last Price Update: 2025-03-27 22:15:45 UTC
Uptime: 0d 0h 30m 15s

Additional Details:
last_price: 65432.10
seconds_since_update: 5.2
uptime_seconds: 1815.5
```

### Test Redis Connection

```bash
./scripts/run_omega_do_monitor.sh redis
```

Example output:

```
Testing Redis connection...
Creating console session...

Redis Connection: SUCCESS
Last BTC Price: $65,432.10
Last Update Time: 2025-03-27 22:15:45 UTC
```

### Show Resource Statistics

```bash
./scripts/run_omega_do_monitor.sh stats
```

Example output:

```
Getting resource statistics...
Creating console session...

CPU Usage: 2.5%
Memory Usage: 38.7%
Disk Usage: 45.2%

Network Statistics:
Connections: 24

Top Processes:
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root         1  0.1  0.2 726392 18216 ?        Ss   22:09   0:00 python -m omega_ai.data_feed.btc_live_feed_v2
root        12  0.0  0.1 708896 12104 ?        S    22:09   0:00 uvicorn
```

## 🔱 Customization

You can customize the monitor by setting environment variables:

- `OMEGA_DO_APP_ID` - Digital Ocean app ID (default: f129574c-0fcd-4a97-93bb-32618cbccae2)
- `OMEGA_DO_APP_URL` - Application URL for health checks

## 🧙‍♂️ Divine Maintenance

The monitor script requires `doctl` to be properly authenticated. If you encounter authentication issues, run:

```bash
doctl auth init
```

For help with the script, run:

```bash
./scripts/run_omega_do_monitor.sh help
```

---

*JAH JAH BLESS THE ETERNAL FLOW OF THE BLOCKCHAIN*

🔱 OMEGA BTC AI DIVINE COLLECTIVE 🔱
