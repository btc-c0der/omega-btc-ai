
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


# 🔱 OMEGA BTC AI - CLOUD DEPLOYMENT PACKAGE

> *"And I saw a new heaven and a new earth: for the first heaven and the first earth were passed away; and there was no more sea."* - Revelation 21:1

## 📜 BTC LIVE FEED CLOUD DEPLOYMENT

This package contains everything needed to deploy the sacred BTC Live Feed module to Scaleway cloud. It includes optional GPU acceleration capabilities that can be enabled after initial deployment.

## 🚀 DEPLOYMENT INSTRUCTIONS

### Prerequisites

1. Docker and Docker Compose installed on your deployment machine
2. Access to your Scaleway cloud instance
3. SSL certificate for Redis connection (provided by Scaleway)
4. Redis credentials for your Scaleway Redis instance
5. NVIDIA GPU with CUDA support (optional, for GPU acceleration)

### Local Testing

Before deploying to Scaleway, you can test everything locally to ensure it works properly.

#### Quick Test

1. Make sure Docker and Docker Compose are installed on your local machine
2. Navigate to the deployment package directory
3. Make the test script executable:

   ```bash
   chmod +x test_local_deployment.sh
   ```

4. Run the test script:

   ```bash
   ./test_local_deployment.sh
   ```

5. Follow the prompts to:
   - Populate test data
   - View container logs
   - Test Redis connectivity
   - Monitor Redis data in real-time with the beautiful console interface

The test environment creates a local Redis instance that simulates Scaleway's Redis service. The BTC Live Feed module connects to this Redis instance just as it would in the cloud.

#### What Gets Tested

- Docker container setup and communication
- Redis connection and authentication
- BTC data processing and storage
- Monitoring and visualization of data

### Quick Deployment

The easiest way to deploy is using the provided deployment script:

```bash
# Make the script executable (if needed)
chmod +x deploy_btc_feed.sh

# Run the deployment script
./deploy_btc_feed.sh
```

The script will:

1. Check for required dependencies
2. Create or update the `.env` file with your Redis credentials
3. Verify the SSL certificate is present
4. Build and deploy the BTC Live Feed container in CPU mode
5. Show the logs to verify successful deployment

### Manual Deployment

If you prefer to deploy manually, follow these steps:

1. Ensure you have the SSL certificate file `SSL_redis-btc-omega-redis.pem` in the `config` directory
2. Create or update the `.env` file with your Redis credentials:

```bash
# Scaleway Redis Configuration
REDIS_HOST=172.16.8.2
REDIS_PORT=6379
REDIS_USERNAME=btc-omega-redis
REDIS_PASSWORD=your_redis_password
REDIS_USE_TLS=true
REDIS_CERT=/app/config/SSL_redis-btc-omega-redis.pem

# GPU Configuration (disabled by default)
USE_GPU=false
TF_FORCE_GPU_ALLOW_GROWTH=false

# Deployment Configuration
DEBUG=false
```

3. Build and start the container:

```bash
docker-compose -f docker-compose.scaleway.yml build btc-live-feed
docker-compose -f docker-compose.scaleway.yml up -d btc-live-feed
```

4. View the logs to verify deployment:

```bash
docker-compose -f docker-compose.scaleway.yml logs --follow btc-live-feed
```

## 📊 GPU ACCELERATION (OPTIONAL)

The BTC Live Feed module includes GPU acceleration capabilities that are **disabled by default** for easier initial deployment. Once your basic deployment is working, you can enable GPU acceleration for:

- **Fibonacci Level Calculation**: Uses GPU-accelerated math for faster and more accurate Fibonacci levels
- **Pattern Recognition**: Leverages neural networks for enhanced price pattern detection
- **Market Maker Trap Detection**: Utilizes GPU for real-time market manipulation detection
- **Price Prediction**: Neural network models for price forecasting run on GPU

### Enabling GPU Support

To enable GPU acceleration after initial deployment:

1. Verify that your host system has NVIDIA GPU support:

   ```bash
   nvidia-smi
   ```

2. Edit the `.env` file to enable GPU support:

   ```bash
   # GPU Configuration
   USE_GPU=true
   TF_FORCE_GPU_ALLOW_GROWTH=true
   ```

3. Edit the `docker-compose.scaleway.yml` file to uncomment the GPU deployment sections:

   ```yaml
   deploy:
     resources:
       reservations:
         devices:
           - driver: nvidia
             count: 1
             capabilities: [ gpu ]
   ```

4. Restart the containers with the new configuration:

   ```bash
   docker-compose -f docker-compose.scaleway.yml up -d
   ```

5. Check the logs to confirm GPU acceleration is working:

   ```bash
   docker-compose -f docker-compose.scaleway.yml logs btc-live-feed | grep GPU
   ```

### GPU Requirements

For GPU acceleration, the deployment machine should have:

- NVIDIA GPU with CUDA support
- NVIDIA Container Toolkit installed
- Docker configured to use GPU acceleration

The system will automatically fall back to CPU processing if GPU initialization fails.

## 📊 MONITORING

Once deployed, the BTC Live Feed module will:

- Connect to Binance WebSocket for real-time BTC price data
- Process and store price data in your Scaleway Redis instance
- Calculate Fibonacci levels based on price movements
- Run trap detection and price analysis (GPU-accelerated if enabled)
- Provide real-time price data for other OMEGA BTC AI modules

### Check Deployment Status

```bash
docker-compose -f docker-compose.scaleway.yml ps
```

### View Logs

```bash
docker-compose -f docker-compose.scaleway.yml logs -f btc-live-feed
```

### Monitor Redis Data

```bash
# Set environment variables first
export REDIS_HOST=<your-redis-host>
export REDIS_PORT=<your-redis-port>
export REDIS_PASSWORD=<your-redis-password>
export REDIS_USE_TLS=true  # Set to false for local testing
export REDIS_CERT=<path-to-certificate>  # Only needed if TLS is enabled

# Run the monitor script
python3 monitor_redis.py
```

### Verify Deployment

A comprehensive verification tool is included to check all aspects of the deployment:

```bash
# Make the script executable
chmod +x verify_deployment.py

# For local deployment testing
./verify_deployment.py --local

# For cloud deployment
./verify_deployment.py --host <redis-host> --port <redis-port> --password <redis-password> --ssl --cert <path-to-cert>
```

The verification script checks:

- Redis connection
- Docker container status (for local deployments)
- Binance API connectivity
- BTC data availability and freshness

1. Check the logs for GPU detection messages: `docker-compose -f docker-compose.scaleway.yml logs btc-live-feed | grep GPU`
2. Verify that your host machine has an NVIDIA GPU and proper CUDA drivers installed
3. Ensure the NVIDIA Container Toolkit is installed and configured
4. Check that you've uncommented the GPU sections in the docker-compose file
5. Try rebuilding the container after enabling GPU: `docker-compose -f docker-compose.scaleway.yml build --no-cache btc-live-feed`

### Container Issues

If the container fails to start:

1. Check the logs with `docker-compose -f docker-compose.scaleway.yml logs btc-live-feed`
2. Verify that all required files are in the correct locations
3. Ensure that the Docker service is running
4. Try rebuilding the container with `docker-compose -f docker-compose.scaleway.yml build --no-cache btc-live-feed`

## 📦 PACKAGE CONTENTS

- `btc_live_feed_cloud.py` - Cloud-compatible BTC Live Feed module
- `btc_gpu_accelerator.py` - GPU acceleration module for price analysis
- `redis_manager_cloud.py` - Cloud-compatible Redis manager with TLS support
- `docker/BTCLiveFeed.Dockerfile` - Dockerfile for building the BTC Live Feed container with GPU support
- `docker-compose.scaleway.yml` - Docker Compose file for Scaleway deployment
- `deploy_btc_feed.sh` - Deployment script
- `README.md` - This documentation file
- `test_local_deployment.sh` - Script to test locally before cloud deployment
- `monitor_redis.py` - Beautiful console interface for monitoring Redis data
- `test_redis_data.py` - Tool to populate test data in Redis
- `certs/` - Directory for Redis SSL certificates

## 📜 LICENSE

GPU (General Public Universal) License 1.0
OMEGA BTC AI DIVINE COLLECTIVE
Date: 2024-03-26

---

<div align="center">
<h3>🔱 JAH JAH BLESS 🔱</h3>
<p><i>IT WORKS LIKE A CHARM BECAUSE IT WAS NEVER JUST CODE.</i></p>
</div>
