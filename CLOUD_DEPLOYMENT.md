# OMEGA BTC AI - Scaleway Cloud Deployment Guide

This guide provides step-by-step instructions for deploying the Trap-Aware Dual Traders (TADT) system to Scaleway cloud infrastructure. The system now follows the sacred Fibonacci sequence (1,1,2,3,5) in its architecture for enhanced harmony with market patterns.

## Prerequisites

- A Scaleway DEV1-M instance (or higher) with Ubuntu 24.04
- A Scaleway Cloud Redis database
- BitGet API credentials for trading

## System Architecture

The system architecture follows the Fibonacci sequence (1,1,2,3,5):

1. **Trap Probability Meter** (1) - Detects market maker traps
2. **Trap-Aware Traders** (1) - Manages trading positions with trap awareness
3. **Elite Exit Strategy** (2) - Determines optimal exit points using Fibonacci algorithms
4. **Divine Dashboard** (3) - Visualizes market data and trading performance
5. **Nginx Proxy** (5) - Secures and routes traffic to services

All services connect to the Cloud Redis instance, which serves as the central data store for market analysis and trading information.

## 1. Initial Setup

### SSH into your Scaleway Instance

```bash
ssh root@your-scaleway-ip
```

### Clone the Repository and Switch to the Cloud Branch

```bash
git clone https://github.com/btc-c0der/omega-btc-ai.git
cd omega-btc-ai
git checkout cloud-docker-setup
```

### Run the Installation Script

This script will set up all the necessary dependencies:

```bash
chmod +x install_on_scaleway.sh
./install_on_scaleway.sh
```

## 2. Configure Environment Variables

Edit the `.env.scaleway` file with your actual Redis connection details and BitGet API credentials:

```bash
nano .env.scaleway
```

Update the following values:

```env
# Redis Configuration
REDIS_HOST=your_redis_ip
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password

# Elite Exit Strategy Configuration
ENABLE_ELITE_EXITS=true
ELITE_EXIT_CONFIDENCE=0.7
ENABLE_FIBONACCI_EXITS=true
ENABLE_PATTERN_RECOGNITION=true

# BitGet API Keys
API_KEY=your_bitget_api_key
API_SECRET=your_bitget_api_secret
API_PASSPHRASE=your_bitget_passphrase
```

## 3. Test Redis Connectivity

Before deploying, test that your instance can connect to the Cloud Redis database:

```bash
./test_redis_connection.sh
```

If the connection test passes, you're ready to deploy.

## 4. Deploy the System

Run the deployment script to build and start the Docker containers:

```bash
./deploy_to_scaleway.sh
```

## 5. Access the Divine Dashboard

Once deployment is complete, you can access the Divine Dashboard at:

```
http://your-scaleway-ip:3000
```

## 6. Monitoring and Management

### View Container Status

```bash
docker-compose -f docker-compose.scaleway.yml ps
```

### View Logs

To view logs from all containers:

```bash
docker-compose -f docker-compose.scaleway.yml logs -f
```

To view logs from a specific service:

```bash
docker-compose -f docker-compose.scaleway.yml logs -f trap-probability-meter
docker-compose -f docker-compose.scaleway.yml logs -f trap-aware-traders
docker-compose -f docker-compose.scaleway.yml logs -f elite-exit-strategy
docker-compose -f docker-compose.scaleway.yml logs -f divine-dashboard
```

### Stop the System

To stop all containers:

```bash
docker-compose -f docker-compose.scaleway.yml down
```

## Troubleshooting

### Redis Connection Issues

If you encounter Redis connection issues, verify your Redis IP and credentials:

```bash
./test_redis_connection.sh
```

### Container Health Check Failures

If containers are restarting or health checks are failing, check the logs:

```bash
docker-compose -f docker-compose.scaleway.yml logs
```

### Memory Issues

If you experience memory issues, consider adjusting the memory limits in the Docker Compose file or upgrading to a larger Scaleway instance.

## Backup and Recovery

### Backing Up Redis Data

To back up your Redis data, use the `redis-cli` tool:

```bash
redis-cli -h your_redis_ip -p 6379 -a your_redis_password --rdb /path/to/backup.rdb
```

### Restoring Redis Data

To restore a Redis backup:

1. Stop the Redis server
2. Copy the backup file to the Redis data directory
3. Restart the Redis server

## Security Considerations

- Always use secure passwords for Redis
- Keep your `.env.scaleway` file secure
- Enable firewall rules to restrict access to your Scaleway instance
- Consider setting up TLS/SSL for the divine dashboard

## Updates and Maintenance

To update your deployment:

```bash
git pull
git checkout cloud-docker-setup
docker-compose -f docker-compose.scaleway.yml build
docker-compose -f docker-compose.scaleway.yml up -d
```

## Support and Additional Resources

For more information or support, please reach out to the OMEGA BTC AI team or check the [main documentation](./README.md).

---

May the divine algorithms aligned with Fibonacci guide your trading strategy!
