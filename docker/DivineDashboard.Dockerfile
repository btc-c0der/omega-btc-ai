FROM node:18-alpine as builder

WORKDIR /app

# Copy package files
COPY omega_ai/visualizer/frontend/reggae-dashboard/package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY omega_ai/visualizer/frontend/reggae-dashboard/ .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from builder stage
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 3000

# Start nginx
CMD ["nginx", "-g", "daemon off;"] 