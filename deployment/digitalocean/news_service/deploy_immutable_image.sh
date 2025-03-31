#!/bin/bash
# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

set -euo pipefail

# Configuration
REGISTRY="registry.digitalocean.com"
IMAGE_NAME="omega-btc-ai/immutable-news-service"

# If provided, use specific version, otherwise use latest
if [ $# -eq 1 ]; then
  VERSION="$1"
else
  # Get the current version from version file
  VERSION=$(cat CURRENT_IMMUTABLE_VERSION)
fi

FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${VERSION}"

echo "🔱 Deploying immutable image: ${FULL_IMAGE_NAME}"

# Enable Docker Content Trust for image verification
export DOCKER_CONTENT_TRUST=1

# Pull the image with verification
echo "🔱 Pulling and verifying signed image..."
docker pull "${FULL_IMAGE_NAME}"

# Create deployment-specific docker-compose file
cat > docker-compose.deploy.yml << EOF
version: '3'

services:
  news-service:
    build: .
    ports:
      - "8080:8080"
    restart: always
    volumes:
      - ./articles:/app/articles
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:8080/health" ]
      interval: 30s
      timeout: 10s
      retries: 3

  nginx:
    image: ${FULL_IMAGE_NAME}
    ports:
      - "10082:80"
    volumes:
      # Only mount writable volumes needed for operation
      - nginx_temp:/var/cache/nginx
      - nginx_logs:/var/log/nginx
      - nginx_run:/var/run
    depends_on:
      - news-service
    restart: always
    read_only: true
    security_opt:
      - no-new-privileges:true
    healthcheck:
      test: [ "CMD", "curl", "-f", "http://localhost:80/portal/" ]
      interval: 30s
      timeout: 10s
      retries: 3
    deploy:
      update_config:
        order: start-first
        failure_action: rollback
      rollback_config:
        parallelism: 0
        order: stop-first

volumes:
  nginx_temp:
  nginx_logs:
  nginx_run:
EOF

# Backup current deployment if it exists
if [ -f "docker-compose.override.yml" ]; then
  echo "🔱 Backing up current deployment configuration..."
  cp docker-compose.override.yml docker-compose.override.backup.$(date +"%Y%m%d-%H%M")
fi

# Move deployment file into place
mv docker-compose.deploy.yml docker-compose.override.yml

# Deploy the immutable container
echo "🔱 Deploying immutable container..."
docker-compose down nginx
docker-compose up -d nginx

# Verify deployment
echo "🔱 Verifying deployment..."
sleep 5
HEALTH_CHECK=$(docker-compose ps nginx | grep "Up" | wc -l)

if [ "$HEALTH_CHECK" -eq 1 ]; then
  echo "🔱 Deployment successful! Immutable container is running."
  echo "🔱 Deployed version: ${VERSION}"
  
  # Record deployment in log
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Deployed ${FULL_IMAGE_NAME}" >> deployment_history.log
else
  echo "⚠️ Deployment failed! Rolling back..."
  if [ -f "docker-compose.override.backup.$(date +"%Y%m%d-%H%M")" ]; then
    mv "docker-compose.override.backup.$(date +"%Y%m%d-%H%M")" docker-compose.override.yml
    docker-compose down nginx
    docker-compose up -d nginx
    echo "🔱 Rollback completed."
  else
    echo "⚠️ No backup file found for automatic rollback. Manual intervention required."
  fi
  exit 1
fi 