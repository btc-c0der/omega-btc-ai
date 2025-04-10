
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


# Docker Configuration

## Overview

The Docker configuration for Omega Bot Farm provides containerization for all system components, ensuring consistent deployment across environments. This directory contains Dockerfiles, docker-compose configurations, and related resources for building and running the system in containers.

## Container Structure

The Omega Bot Farm uses a multi-container architecture:

### Bot Base (bot-base/)

The foundational image that all trading bots inherit from:

- Python runtime environment
- Common dependencies
- Shared utilities
- Monitoring tooling

### Trading Bots (trading-bots/)

Container definitions for various trading bots:

- BitGet Position Analyzer
- Strategic Fibonacci Trader
- CCXT-based traders
- Other specialized trading bots

### Discord Bot (discord-bot/)

Container for the Discord interface:

- Waze Bot implementation
- User interaction services
- Notification systems
- Authentication handlers

## Image Hierarchy

```
┌─────────────┐
│   Bot Base  │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐
│ Trading Bots │     │ Discord Bot │
└─────────────┘     └─────────────┘
```

## Building Images

To build all images:

```bash
# From project root
cd src/omega_bot_farm/docker
docker-compose build
```

To build a specific image:

```bash
# Build just the base image
docker build -t omega-bot-base:latest ./bot-base

# Build a specific trading bot
docker build -t bitget-position-analyzer:latest ./trading-bots/bitget-analyzer
```

## Running Containers

### Using Docker Compose

```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d discord-bot

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Using Docker Directly

```bash
# Run Discord bot
docker run -d \
  --name waze-bot \
  -e DISCORD_TOKEN=your_token \
  -e REDIS_HOST=redis \
  --network omega-network \
  omega-discord-bot:latest

# Run BitGet analyzer
docker run -d \
  --name bitget-analyzer \
  -e BITGET_API_KEY=your_key \
  -e BITGET_SECRET_KEY=your_secret \
  -e BITGET_PASSPHRASE=your_passphrase \
  -e REDIS_HOST=redis \
  --network omega-network \
  bitget-position-analyzer:latest
```

## Configuration

Container configuration is managed through:

- Environment variables
- Mounted configuration files
- Docker secrets (for sensitive data)

### Environment Variables

Each container accepts specific environment variables:

- `REDIS_HOST`, `REDIS_PORT`: Redis connection details
- `LOG_LEVEL`: Logging verbosity
- Service-specific API credentials (e.g., `BITGET_API_KEY`)

### Volume Mounts

Containers use volume mounts for:

- Configuration files
- Persistent data storage
- Log output

## Networking

Containers communicate via a dedicated Docker network:

- Redis for shared state and messaging
- HTTP/HTTPS for API access
- Internal service discovery

## Development Workflow

For local development:

1. Build images with dev tags: `docker-compose build --build-arg ENV=dev`
2. Mount local code as volumes: `-v ./src:/app/src`
3. Enable hot reloading where supported
4. Use development-specific environment variables

## Production Deployment

For production:

1. Use specific version tags instead of latest
2. Configure proper logging and monitoring
3. Set up restart policies
4. Use Docker secrets for sensitive data
5. Implement health checks
