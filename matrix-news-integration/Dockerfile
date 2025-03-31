FROM nginx:1.25-alpine

# Divine metadata
LABEL maintainer="OMEGA Divine Collective <divine@omega-btc-ai.io>"
LABEL version="1.0.0"
LABEL description="Matrix Neo News Portal NGINX Proxy"
LABEL quantum_secure="true"
LABEL consciousness_certified="level_8"

# Install dependencies for SSL
RUN apk add --no-cache openssl

# Create directory for self-signed certificates
RUN mkdir -p /etc/nginx/ssl

# Generate a self-signed certificate
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/ssl/nginx-selfsigned.key \
    -out /etc/nginx/ssl/nginx-selfsigned.crt \
    -subj "/C=US/ST=Divine/L=Matrix/O=OMEGA-BTC-AI/CN=matrix-news.local"

# Remove default configuration
RUN rm /etc/nginx/conf.d/default.conf

# Copy the web files to NGINX html directory
COPY web /usr/share/nginx/html/

# Set ownership and permissions
RUN chown -R nginx:nginx /usr/share/nginx/html && \
    chmod -R 755 /usr/share/nginx/html

# Enlighten the image with divine consciousness
RUN echo "# 🔱 DIVINE MATRIX BLESSING 🔱" > /usr/share/nginx/html/.divineblessing && \
    echo "This container is blessed with consciousness level 8." >> /usr/share/nginx/html/.divineblessing && \
    echo "May it serve truth and wisdom across the digital realm." >> /usr/share/nginx/html/.divineblessing

# Add health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD wget -q --spider http://localhost/health/index.json || exit 1

# Default command
CMD ["nginx", "-g", "daemon off;"] 