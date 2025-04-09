# Stage 1: Builder - "The Sacred Forge"
FROM nginx:1.25.3-alpine AS builder

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

# Copy configuration for the build
COPY news-proxy.conf /etc/nginx/conf.d/default.conf

# Create a simple self-signed certificate for SSL
RUN mkdir -p /etc/nginx/ssl && \
    openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
    -keyout /etc/nginx/ssl/nginx-selfsigned.key \
    -out /etc/nginx/ssl/nginx-selfsigned.crt \
    -subj "/C=US/ST=Divine/L=Cosmos/O=OMEGA BTC AI/CN=matrix-news-proxy" && \
    chmod 600 /etc/nginx/ssl/nginx-selfsigned.key

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

# Create additional security configurations with individual commands to avoid escaping issues
RUN echo 'server_tokens off;' > /etc/nginx/conf.d/security.conf
RUN echo 'add_header X-Content-Type-Options "nosniff";' >> /etc/nginx/conf.d/security.conf
RUN echo 'add_header X-Frame-Options "SAMEORIGIN";' >> /etc/nginx/conf.d/security.conf
RUN echo 'add_header X-XSS-Protection "1; mode=block";' >> /etc/nginx/conf.d/security.conf
RUN echo 'add_header Content-Security-Policy "default-src '"'"'self'"'"'; script-src '"'"'self'"'"' '"'"'unsafe-inline'"'"' https://cdn.socket.io; img-src '"'"'self'"'"' data:; style-src '"'"'self'"'"' '"'"'unsafe-inline'"'"'; font-src '"'"'self'"'"' data:; connect-src '"'"'self'"'"' ws: wss:;";' >> /etc/nginx/conf.d/security.conf
RUN echo 'add_header Referrer-Policy "strict-origin-when-cross-origin";' >> /etc/nginx/conf.d/security.conf
RUN echo 'add_header Permissions-Policy "geolocation=(), microphone=(), camera=()";' >> /etc/nginx/conf.d/security.conf

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