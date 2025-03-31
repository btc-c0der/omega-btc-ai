#!/bin/bash
# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

set -euo pipefail

# Configuration
IMAGE_NAME="omega-btc-ai/immutable-news-service"
VERSION=$(date +"%Y%m%d-%H%M")
FULL_IMAGE_NAME="${IMAGE_NAME}:${VERSION}"
REGISTRY="registry.digitalocean.com"  # Change as needed

echo "🔱 Building immutable image: ${FULL_IMAGE_NAME}"

# Enable Docker Content Trust for secure image signing
export DOCKER_CONTENT_TRUST=1

# Create a temporary Dockerfile for the immutable image
cat > Dockerfile.immutable << EOF
FROM nginx:1.25.3-alpine
LABEL maintainer="OMEGA BTC AI <divine@omega-btc-ai.com>"
LABEL version="${VERSION}"
LABEL immutable="true"
LABEL build_date="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# Copy configuration and static content
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./web /usr/share/nginx/html

# Set ownership and permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 555 /usr/share/nginx/html && \
    chmod 444 /etc/nginx/nginx.conf && \
    chmod 444 /etc/nginx/conf.d/default.conf

# Create required directories with correct permissions
RUN mkdir -p /var/cache/nginx /var/log/nginx /var/run && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /var/run

# Set up health check
HEALTHCHECK --interval=30s --timeout=3s \
    CMD wget --quiet --tries=1 --spider http://localhost/portal/ || exit 1

# Use non-root user
USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOF

# Build the image
echo "🔱 Building image..."
docker build -t "${FULL_IMAGE_NAME}" -f Dockerfile.immutable .

# Tag the image for the registry
echo "🔱 Tagging image for registry..."
docker tag "${FULL_IMAGE_NAME}" "${REGISTRY}/${FULL_IMAGE_NAME}"

# Push the image to the registry
echo "🔱 Pushing signed image to registry..."
docker push "${REGISTRY}/${FULL_IMAGE_NAME}"

# Tag as latest
echo "🔱 Tagging as latest..."
docker tag "${FULL_IMAGE_NAME}" "${IMAGE_NAME}:latest"
docker tag "${FULL_IMAGE_NAME}" "${REGISTRY}/${IMAGE_NAME}:latest"
docker push "${REGISTRY}/${IMAGE_NAME}:latest"

# Update version file to track current immutable version
echo "${VERSION}" > CURRENT_IMMUTABLE_VERSION

# Clean up
rm Dockerfile.immutable

echo "🔱 Successfully built and pushed immutable image: ${FULL_IMAGE_NAME}"
echo "🔱 To use this immutable image, update your docker-compose.yml:"
echo "    image: ${REGISTRY}/${FULL_IMAGE_NAME}"
echo ""
echo "🔱 Image SHA256: $(docker inspect --format='{{index .RepoDigests 0}}' ${FULL_IMAGE_NAME})" 