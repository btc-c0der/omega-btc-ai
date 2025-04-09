FROM nginx:1.25.3-alpine

# Set up directories with appropriate permissions
RUN mkdir -p /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 777 /var/cache/nginx /var/run /var/log/nginx

# Copy the nginx configuration
COPY news-proxy.conf /etc/nginx/conf.d/default.conf

# Create a health check endpoint
RUN mkdir -p /usr/share/nginx/html/health && \
    echo '{"status":"UP","service":"matrix-news-proxy","timestamp":""}' > /usr/share/nginx/html/health/index.json

# Expose ports
EXPOSE 80

# Set up healthcheck
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
    CMD wget -q --spider http://localhost/health/index.json || exit 1

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 