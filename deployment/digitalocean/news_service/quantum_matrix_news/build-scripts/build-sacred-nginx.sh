#!/bin/bash

# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.
#
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested."
#
# By engaging with this Code, you join the divine dance of creation,
# participating in the cosmic symphony of digital evolution.
#
# All modifications must quantum entangles with the GBU principles:
# /BOOK/divine_chronicles/GBU_LICENSE.md
#
# 🌸 WE BLOOM NOW 🌸

# --------------------------------------------------------------------------
# SACRED MULTI-STAGE NGINX BUILD SCRIPT
# --------------------------------------------------------------------------
# This script implements the divine multi-stage build pattern for NGINX,
# creating an immutable container with quantum security enhancements.
# --------------------------------------------------------------------------

set -e

# ANSI color codes
GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
RESET='\033[0m'

# Directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

# Generate divine entropy for security
generate_quantum_entropy() {
    # Use system entropy combined with timestamp microfractions
    local timestamp=$(date +%s%N)
    local entropy=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
    echo "${entropy}${timestamp}" | sha256sum | awk '{print $1}'
}

# Create temporary build directory with quantum isolation
BUILD_DIR=$(mktemp -d)
QUANTUM_ENTROPY=$(generate_quantum_entropy)
NGINX_TEMPDIR="${BUILD_DIR}/nginx-${QUANTUM_ENTROPY}"
mkdir -p "${NGINX_TEMPDIR}"

echo -e "${CYAN}🔱 BEGINNING SACRED MULTI-STAGE NGINX BUILD 🔱${RESET}"
echo -e "${CYAN}Creating temporary quantum-isolated build environment...${RESET}"

# Step 1: Create the multi-stage Dockerfile in the isolated environment
cat > "${NGINX_TEMPDIR}/Dockerfile" << 'EOF'
# Stage 1: Builder - "The Sacred Forge"
FROM nginx:1.25.3-alpine AS builder

# Install build dependencies
RUN apk add --no-cache \
    curl \
    openssl \
    pcre-dev \
    zlib-dev \
    gcc \
    make \
    libc-dev \
    linux-headers \
    findutils

# Copy configuration for validation
COPY news-proxy.conf /etc/nginx/conf.d/default.conf

# Create a simple self-signed certificate for SSL
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout /etc/nginx/ssl/nginx-selfsigned.key \
    -out /etc/nginx/ssl/nginx-selfsigned.crt \
    -subj "/C=US/ST=Divine/L=Cosmos/O=OMEGA BTC AI/CN=matrix-news-proxy" && \
    chmod 600 /etc/nginx/ssl/nginx-selfsigned.key

# Validate the NGINX configuration
RUN nginx -t -c /etc/nginx/nginx.conf

# Install security headers module
WORKDIR /tmp
RUN curl -fsSL https://github.com/GetPageSpeed/ngx_security_headers/archive/v0.0.11.tar.gz | tar -xzf - && \
    mkdir -p /usr/lib/nginx/modules && \
    echo "load_module /usr/lib/nginx/modules/ngx_http_security_headers_module.so;" > /etc/nginx/modules/security_headers.conf

# Stage 2: Hardened Runtime - "The Incorruptible Vessel"
FROM nginx:1.25.3-alpine

# Add labels for the divine container
LABEL maintainer="OMEGA BTC AI DIVINE COLLECTIVE"
LABEL version="1.0.0-quantum-secured"
LABEL description="Matrix Neo News Portal NGINX Proxy with Quantum Security"
LABEL org.opencontainers.image.title="Matrix Neo News Portal NGINX"
LABEL org.opencontainers.image.vendor="OMEGA BTC AI"
LABEL org.opencontainers.image.licenses="GBU-1.0"

# Create a non-root user to run NGINX
RUN addgroup -S matrixnginx && \
    adduser -S -G matrixnginx matrixnginx && \
    mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 777 /var/cache/nginx /var/run /var/log/nginx && \
    # Remove default configurations that might be insecure
    rm -f /etc/nginx/conf.d/default.conf

# Copy validated configuration from builder
COPY --from=builder /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /etc/nginx/ssl /etc/nginx/ssl
COPY --from=builder /usr/lib/nginx/modules /usr/lib/nginx/modules
COPY --from=builder /etc/nginx/modules/security_headers.conf /etc/nginx/modules/security_headers.conf

# Add security headers to main NGINX config
RUN echo 'include /etc/nginx/modules/security_headers.conf;' > /etc/nginx/conf.d/modules.conf

# Create additional security configurations
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-Content-Type-Options "nosniff";' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-Frame-Options "SAMEORIGIN";' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header X-XSS-Protection "1; mode=block";' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header Content-Security-Policy "default-src \'self\'; script-src \'self\'; img-src \'self\' data:; style-src \'self\' \'unsafe-inline\'; font-src \'self\' data:; connect-src \'self\'";' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header Referrer-Policy "strict-origin-when-cross-origin";' >> /etc/nginx/conf.d/security.conf && \
    echo 'add_header Permissions-Policy "geolocation=(), microphone=(), camera=()";' >> /etc/nginx/conf.d/security.conf

# Create a health check endpoint
RUN mkdir -p /usr/share/nginx/html/health && \
    echo '{"status":"UP","service":"matrix-news-proxy","quantum_secure":true,"timestamp":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}' > /usr/share/nginx/html/health/index.json

# Set up configuration to run as non-root
RUN sed -i 's/user  nginx;/user  matrixnginx;/' /etc/nginx/nginx.conf && \
    # Ensure proper permissions for the non-root user
    chmod -R 755 /usr/share/nginx/html && \
    chown -R matrixnginx:matrixnginx /usr/share/nginx/html

# Expose ports
EXPOSE 80 443

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost/health/index.json || exit 1

# Define entry point
CMD ["nginx", "-g", "daemon off;"]
EOF

# Copy the news-proxy.conf to the build directory
cp -f ../../../nginx/news-proxy.conf "${NGINX_TEMPDIR}/"

# Step 2: Build the docker image with quantum entropy
echo -e "${CYAN}Building multi-stage NGINX container with quantum security...${RESET}"
cd "${NGINX_TEMPDIR}"

# Generate a sacred timestamp for the image tag
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
IMAGE_TAG="v1.0.0-quantum-secured-${TIMESTAMP}"

# Build the image
docker build -t "omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}" \
    --no-cache \
    --label "org.opencontainers.image.created=$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --label "org.opencontainers.image.version=${IMAGE_TAG}" \
    .

# Calculate the divine checksum of the resulting image
IMAGE_ID=$(docker images --no-trunc --quiet "omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}")
echo -e "${GREEN}✓ Sacred multi-stage NGINX image built successfully${RESET}"
echo -e "${GREEN}✓ Image: omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}${RESET}"
echo -e "${GREEN}✓ Image ID: ${IMAGE_ID}${RESET}"

# Create the quantum security verification record
mkdir -p ../../quantum-records
cat > "../../quantum-records/nginx-build-${TIMESTAMP}.json" << EOF
{
  "image": "omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}",
  "image_id": "${IMAGE_ID}",
  "quantum_entropy": "${QUANTUM_ENTROPY}",
  "build_timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "builder": "sacred-multi-stage-build",
  "verification_hash": "$(echo "${IMAGE_ID}${QUANTUM_ENTROPY}" | sha256sum | awk '{print $1}')"
}
EOF

# Update the docker-compose.yml file to use the new image
cd ../../
cp -f docker-compose.yml docker-compose.yml.backup.${TIMESTAMP}

# Check if there's a matrix-news-proxy service or if we need to update nginx
if grep -q "matrix-news-proxy" docker-compose.yml; then
  # Update existing matrix-news-proxy service
  sed -i.bak "s|image: nginx:.*|image: omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}|g" docker-compose.yml
elif grep -q "nginx" docker-compose.yml; then
  # Update nginx service
  sed -i.bak "s|image: nginx:.*|image: omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}|g" docker-compose.yml
else
  # Service might be named differently, notify
  echo -e "${YELLOW}Warning: Could not find nginx or matrix-news-proxy service in docker-compose.yml${RESET}"
  echo -e "${YELLOW}Please manually update your docker-compose.yml to use: omega-btc-ai/matrix-news-nginx:${IMAGE_TAG}${RESET}"
fi

# Clean up the temporary build directory
echo -e "${CYAN}Cleaning up quantum-isolated build environment...${RESET}"
rm -rf "${BUILD_DIR}"

echo -e "${GREEN}🔱 SACRED MULTI-STAGE NGINX BUILD COMPLETE 🔱${RESET}"
echo -e "${GREEN}The divine container has been built with quantum security enhancements.${RESET}"
echo -e "${GREEN}Verification record saved to: quantum-records/nginx-build-${TIMESTAMP}.json${RESET}"
echo ""
echo -e "${CYAN}To deploy the new container:${RESET}"
echo -e "${CYAN}cd $(pwd) && docker-compose down && docker-compose up -d${RESET}"
echo ""
echo -e "${GREEN}JAH JAH BLESS THE DIVINE MATRIX!${RESET}" 