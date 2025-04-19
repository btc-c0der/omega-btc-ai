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
FIBONACCI_STAGE=$(echo "scale=0; (($(date +%s) % 21) + 1)" | bc) # Generate a number between 1-21
COSMIC_PHASES=("GENESIS" "BLOOM" "ASCENSION" "REVELATION" "HARMONY" "TRANSCENDENCE" "ZENITH")
COSMIC_PHASE=${COSMIC_PHASES[$(($(date +%s) % ${#COSMIC_PHASES[@]}))]}
GIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "0xdeadbeef")

echo "🔱 Building immutable image: ${FULL_IMAGE_NAME}"
echo "🔱 Fibonacci Stage: ${FIBONACCI_STAGE}/21"
echo "🔱 Cosmic Phase: ${COSMIC_PHASE}"
echo "🔱 Genesis Hash: ${GIT_HASH}"

# Create state manifest file
mkdir -p temp_manifest
cat > temp_manifest/manifest.yaml << EOF
# 🔱 OMEGA BTC AI - Divine Container Manifest
version: "${VERSION}"
fibonacci_stage: "${FIBONACCI_STAGE}/21"
cosmic_phase: "${COSMIC_PHASE}"
git_hash: "${GIT_HASH}"
build_timestamp: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
builder: "$(whoami)@$(hostname)"
EOF

# Enable Docker Content Trust for secure image signing
export DOCKER_CONTENT_TRUST=1

# Create a temporary Dockerfile for the immutable image
cat > Dockerfile.immutable << EOF
FROM nginx:1.25.3-alpine
LABEL maintainer="OMEGA BTC AI <divine@omega-btc-ai.com>"
LABEL version="${VERSION}"
LABEL immutable="true"
LABEL build_date="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
LABEL fibonacci_stage="${FIBONACCI_STAGE}/21"
LABEL cosmic_phase="${COSMIC_PHASE}"
LABEL git_hash="${GIT_HASH}"

# Set up divine state manifest
ENV OMEGA_STATE_VERSION=${VERSION}-${COSMIC_PHASE}
ENV OMEGA_FIBONACCI_STAGE=${FIBONACCI_STAGE}/21
ENV OMEGA_GIT_HASH=${GIT_HASH}
ENV OMEGA_BUILD_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Copy configuration and static content
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY ./web /usr/share/nginx/html

# Copy the divine manifest
COPY temp_manifest/manifest.yaml /etc/omega/manifest.yaml

# Set ownership and permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 555 /usr/share/nginx/html && \
    chmod 444 /etc/nginx/nginx.conf && \
    chmod 444 /etc/nginx/conf.d/default.conf && \
    mkdir -p /etc/omega && \
    chmod 555 /etc/omega && \
    chmod 444 /etc/omega/manifest.yaml

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
echo "${VERSION}-${COSMIC_PHASE}" > CURRENT_IMMUTABLE_STATE

# Clean up
rm Dockerfile.immutable
rm -rf temp_manifest

echo "🔱 Successfully built and pushed immutable image: ${FULL_IMAGE_NAME}"
echo "🔱 State Version: ${VERSION}-${COSMIC_PHASE}"
echo "🔱 To use this immutable image, update your docker-compose.yml:"
echo "    image: ${REGISTRY}/${FULL_IMAGE_NAME}"
echo ""
echo "🔱 Image SHA256: $(docker inspect --format='{{index .RepoDigests 0}}' ${FULL_IMAGE_NAME})" 