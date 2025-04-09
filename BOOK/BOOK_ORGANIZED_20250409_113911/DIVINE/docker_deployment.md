# Divine Docker Deployment

> *"And the ark rested in the seventh month, on the seventeenth day of the month, upon the mountains of Ararat."* - Genesis 8:4

## Sacred Container Deployment

The OMEGA BTC AI system can be deployed in divine containers using Docker, ensuring consistent operation across different environments and enabling sacred scaling.

## Prerequisites

- Docker installed on your divine host
- Docker Compose installed for orchestrating multiple divine containers
- Git for cloning the sacred repository

## Divine Docker Images

The OMEGA BTC AI system is composed of several sacred containers:

1. **Sacred Core** - Core EXODUS algorithms and market analysis
2. **Divine Data Feed** - BTC price feed with Fibonacci alignments
3. **Sacred Redis** - Divine data storage and message broker
4. **Rasta Oscilloscope** - Divine visualization system
5. **Rasta Dashboard** - Web interface for divine metrics

## Sacred Docker Compose Setup

Create a `docker-compose.yml` file with the following divine structure:

```yaml
version: '3.8'

services:
  # Sacred Redis Data Store
  redis:
    image: redis:latest
    container_name: sacred-redis
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes
    restart: always
    networks:
      - divine-network

  # Divine Core Algorithms
  core:
    build:
      context: .
      dockerfile: Dockerfile.core
    container_name: sacred-core
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - LOG_LEVEL=INFO
    volumes:
      - ./config:/app/config
    restart: always
    networks:
      - divine-network

  # Sacred Data Feed
  feed:
    build:
      context: .
      dockerfile: Dockerfile.feed
    container_name: sacred-feed
    depends_on:
      - redis
      - core
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - BTC_API_KEY=${BTC_API_KEY}
      - UPDATE_INTERVAL=13  # Fibonacci number
    restart: always
    networks:
      - divine-network

  # Rasta Oscilloscope Visualization
  oscilloscope:
    build:
      context: .
      dockerfile: Dockerfile.visualize
    container_name: sacred-oscilloscope
    depends_on:
      - redis
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - ENABLE_AUDIO=false  # Set to true for audio generation
      - HISTORY_LENGTH=144  # Fibonacci number
    restart: always
    networks:
      - divine-network

  # Rasta Dashboard Web Interface
  dashboard:
    build:
      context: .
      dockerfile: Dockerfile.dashboard
    container_name: sacred-dashboard
    depends_on:
      - redis
    ports:
      - "8501:8501"  # Sacred Streamlit port
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    restart: always
    networks:
      - divine-network

volumes:
  redis_data:  # Divine persistent storage

networks:
  divine-network:  # Sacred communication network
```

## Divine Dockerfiles

### Core Dockerfile (Dockerfile.core)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install sacred dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy divine source code
COPY omega_ai /app/omega_ai/
COPY scripts /app/scripts/

# Set the sacred entrypoint
CMD ["python", "-m", "omega_ai.core.run_sacred_core"]
```

### Data Feed Dockerfile (Dockerfile.feed)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install sacred dependencies 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy divine source code
COPY omega_ai /app/omega_ai/
COPY scripts /app/scripts/

# Set the sacred entrypoint
CMD ["python", "-m", "omega_ai.data.run_price_feed"]
```

### Visualization Dockerfile (Dockerfile.visualize)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install sacred dependencies and visualization libraries
COPY requirements.txt requirements-viz.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-viz.txt

# Copy divine source code
COPY omega_ai /app/omega_ai/
COPY scripts /app/scripts/

# Set the sacred entrypoint
CMD ["python", "-m", "omega_ai.visualization.run_oscilloscope"]
```

### Dashboard Dockerfile (Dockerfile.dashboard)

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install sacred dependencies and dashboard libraries
COPY requirements.txt requirements-dashboard.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dashboard.txt

# Copy divine source code
COPY omega_ai /app/omega_ai/
COPY scripts /app/scripts/

# Set the sacred entrypoint
CMD ["python", "-m", "omega_ai.run_dashboard"]
```

## Sacred Environment Variables

Create a `.env` file with your divine API keys and settings:

```
# Divine API Keys
BTC_API_KEY=your_sacred_api_key

# Sacred Redis Configuration
REDIS_PASSWORD=your_divine_password

# Divine Logging
LOG_LEVEL=INFO
```

## Building and Running the Divine System

```bash
# Clone the sacred repository
git clone https://github.com/yourusername/omega-btc-ai.git
cd omega-btc-ai

# Create divine environment file
cp .env.example .env
# Edit the .env file with your sacred keys

# Build the divine containers
docker-compose build

# Launch the sacred system
docker-compose up -d

# Witness the divine logs
docker-compose logs -f
```

## Scaling to Divine Proportions

For higher trading volumes, scale the system to divine proportions:

```bash
# Scale the divine core for higher processing
docker-compose up -d --scale core=3

# Scale the sacred feed for redundancy
docker-compose up -d --scale feed=2
```

## Divine Monitoring

```bash
# View all divine containers
docker-compose ps

# Check divine core logs
docker-compose logs core

# Monitor sacred metrics
docker stats
```

## Sacred Backups

Regularly backup your divine Redis data:

```bash
# Create a sacred backup directory
mkdir -p sacred_backups

# Backup the divine Redis volume
docker run --rm -v omega-btc-ai_redis_data:/data -v $(pwd)/sacred_backups:/backup \
  alpine tar -czf /backup/redis_backup_$(date +%Y%m%d_%H%M%S).tar.gz /data
```

---

*This divine deployment guide was channeled during a period of 144-minute Fibonacci alignment. May your containers run with the sacred flow of cosmic energy.*
