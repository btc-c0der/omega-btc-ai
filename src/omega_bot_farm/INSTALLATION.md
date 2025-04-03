# Omega Bot Farm - Installation Guide

## Overview

This guide provides step-by-step instructions for installing and configuring the Omega Bot Farm system. The installation can be performed in different environments:

1. Local development environment
2. Docker containers
3. Kubernetes cluster

## Prerequisites

### System Requirements

- Python 3.8 or higher
- Redis server
- Git
- Docker and Docker Compose (for containerized deployment)
- Kubernetes cluster (for cloud deployment)

### API Credentials

You will need API credentials for:

- BitGet exchange
- Discord bot token (for UI access)

## Installation Options

### Option 1: Local Development Setup

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/omega-btc-ai.git
cd omega-btc-ai
```

#### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies

```bash
pip install -r src/omega_bot_farm/requirements.txt
```

#### 4. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Discord Bot Configuration
DISCORD_TOKEN=your_discord_bot_token

# BitGet API Credentials
BITGET_API_KEY=your_bitget_api_key
BITGET_SECRET_KEY=your_bitget_secret_key
BITGET_PASSPHRASE=your_bitget_passphrase

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

# Logging Configuration
LOG_LEVEL=INFO
```

#### 5. Start Redis Server

If you don't have Redis running already:

```bash
# On macOS with Homebrew
brew install redis
brew services start redis

# On Ubuntu/Debian
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### 6. Run the Discord Bot

```bash
python -m src.omega_bot_farm.discord.waze_bot
```

#### 7. Run Trading Bots

To run a specific trading bot:

```bash
python -m src.omega_bot_farm.trading.b0ts.bitget_analyzer
```

### Option 2: Docker Deployment

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/omega-btc-ai.git
cd omega-btc-ai
```

#### 2. Create Environment Files

Create `.env` file with the same variables as in the local setup.

#### 3. Build and Start Containers

```bash
cd src/omega_bot_farm/docker
docker-compose build
docker-compose up -d
```

This will start:

- Redis container
- Discord bot container
- Trading bot containers

#### 4. Check Container Status

```bash
docker-compose ps
```

#### 5. View Logs

```bash
docker-compose logs -f
```

### Option 3: Kubernetes Deployment

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/omega-btc-ai.git
cd omega-btc-ai
```

#### 2. Create Kubernetes Secrets

```bash
# Create a namespace
kubectl create namespace omega-bot-farm

# Create secrets for API credentials
kubectl create secret generic bitget-api-credentials \
  --from-literal=api-key=your_bitget_api_key \
  --from-literal=secret-key=your_bitget_secret_key \
  --from-literal=passphrase=your_bitget_passphrase \
  -n omega-bot-farm

kubectl create secret generic discord-credentials \
  --from-literal=token=your_discord_token \
  -n omega-bot-farm
```

#### 3. Deploy Redis

```bash
kubectl apply -f src/omega_bot_farm/kubernetes/services/redis.yaml -n omega-bot-farm
```

#### 4. Deploy ConfigMaps

```bash
kubectl apply -f src/omega_bot_farm/kubernetes/configmaps/ -n omega-bot-farm
```

#### 5. Deploy Bots

```bash
kubectl apply -f src/omega_bot_farm/kubernetes/deployments/ -n omega-bot-farm
```

#### 6. Check Deployment Status

```bash
kubectl get pods -n omega-bot-farm
```

## Configuration

### Discord Bot Configuration

The Discord bot can be configured by editing `src/omega_bot_farm/config/waze_bot_config.yaml`:

```yaml
# Example configuration
discord:
  command_prefix: "!"
  description: "Waze Bot for BitGet position analysis"
  activity_status: "Analyzing positions"
  
channels:
  announcements: null  # Set to channel ID for announcements
  general: null        # Set to channel ID for general messages
  
commands:
  enabled_commands:
    - bitget-positions
    - bitget-analyze
    - bitget-changes
    - golden-wisdom
    - market-pulse
    
notifications:
  position_updates: true
  market_alerts: true
  report_frequency: 3600  # In seconds
```

### Trading Bot Configuration

Trading bots can be configured by:

1. Environment variables (recommended for credentials)
2. Config files in `src/omega_bot_farm/config/`
3. Command line arguments when running directly

## Post-Installation

### Verifying Installation

#### Discord Bot

1. Invite your bot to a Discord server
2. Type `!waze-help` in any channel
3. The bot should respond with available commands

#### Trading Bots

1. Check logs for successful connection to exchanges
2. Verify data being stored in Redis
3. Confirm position analysis is working

### Monitoring

For local deployment:

- Check application logs

For Docker deployment:

- Use `docker-compose logs`
- Consider setting up Portainer for container management

For Kubernetes deployment:

- Use Kubernetes Dashboard or command line tools
- Consider setting up Prometheus and Grafana for monitoring

## Troubleshooting

### Common Issues

#### Redis Connection Errors

If bots cannot connect to Redis:

- Verify Redis is running
- Check connection settings in environment variables
- Ensure network connectivity between services

#### API Authentication Failures

If exchange API calls are failing:

- Verify API credentials are correct
- Check if API has necessary permissions
- Ensure system time is synchronized (important for API signatures)

#### Discord Bot Not Responding

If the Discord bot is not responding:

- Check if the bot token is valid
- Verify the bot has proper permissions in Discord
- Check application logs for errors

## Updating

To update the system:

1. Pull the latest code:

   ```bash
   git pull origin main
   ```

2. Reinstall dependencies:

   ```bash
   pip install -r src/omega_bot_farm/requirements.txt
   ```

3. Restart services:
   - For local: Restart Python processes
   - For Docker: `docker-compose down && docker-compose up -d`
   - For Kubernetes: `kubectl rollout restart deployment -n omega-bot-farm`

## Support

For additional support:

- Check the documentation in `src/omega_bot_farm/docs/`
- Submit issues to the project repository
- Contact the development team
