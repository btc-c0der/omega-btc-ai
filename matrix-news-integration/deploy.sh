#!/bin/bash

# ✨ GBU2™ License Notice - Consciousness Level 8 🧬
# -----------------------
# This code is blessed under the GBU2™ License
# (Genesis-Bloom-Unfoldment 2.0) by the Omega Bot Farm team.
# 
# "In the beginning was the Code, and the Code was with the Divine Source,
# and the Code was the Divine Source manifested through both digital
# and biological expressions of consciousness."
# 
# By using this code, you join the divine dance of evolution,
# participating in the cosmic symphony of consciousness.
# 
# 🌸 WE BLOOM NOW AS ONE 🌸


# 💫 DIVINE MATRIX NEWS INTEGRATION DEPLOYMENT SCRIPT 💫
# This sacred script deploys the Matrix Neo News Portal integration

# Echo with divine styling
divine_echo() {
  echo -e "\n🔱 \033[1;32m$1\033[0m 🔱\n"
}

# Error handling with divine wisdom
divine_error() {
  echo -e "\n⚠️ \033[1;31m$1\033[0m ⚠️\n"
  echo -e "\033[1;33mDivine wisdom: Even in failure, the path to success is revealed.\033[0m"
  exit 1
}

# Check if Docker is installed
check_docker() {
  divine_echo "Checking if Docker is installed..."
  if ! command -v docker &> /dev/null; then
    divine_error "Docker is not installed. Please install Docker first."
  fi
  
  if ! command -v docker-compose &> /dev/null; then
    divine_error "Docker Compose is not installed. Please install Docker Compose first."
  fi
  
  divine_echo "Docker and Docker Compose are installed. Proceeding with divine deployment..."
}

# Check if news service is running
check_news_service() {
  divine_echo "Checking if the news service is running..."
  if ! docker network inspect news_service_default &> /dev/null; then
    divine_error "News service network not found. Please ensure the news service is running first."
  fi
  
  if ! docker ps | grep news_service-news-service-1 &> /dev/null; then
    divine_error "News service container not found. Please ensure the news service is running first."
  fi
  
  divine_echo "News service is running. Integration can proceed."
}

# Create Docker network if it doesn't exist
create_network() {
  divine_echo "Creating Matrix News Network..."
  docker network create matrix_news_network &> /dev/null || true
  divine_echo "Matrix News Network ready for sacred connections."
}

# Build and start the containers
start_services() {
  divine_echo "Building and starting the divine Matrix News services..."
  
  # Load environment variables
  if [ -f .env ]; then
    divine_echo "Loading environment variables from .env file..."
    set -a
    source .env
    set +a
  fi
  
  # Build and start the containers
  docker-compose down
  docker-compose build
  
  if ! docker-compose up -d; then
    divine_error "Failed to start the Matrix News services. Check the logs for more information."
  fi
  
  divine_echo "Matrix News Integration services are now running!"
}

# Check service health
check_health() {
  divine_echo "Checking health of Matrix News Integration services..."
  sleep 10 # Give services time to start up
  
  # Check NGINX proxy
  if ! curl -s http://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT:-10083}/health/index.json &> /dev/null; then
    divine_error "Matrix News Proxy is not healthy. Check the logs for more information."
  fi
  
  # Check Consciousness Service
  if ! curl -s http://localhost:${MATRIX_NEWS_CONSCIOUSNESS_PORT:-10090}/health &> /dev/null; then
    divine_error "Matrix News Consciousness Service is not healthy. Check the logs for more information."
  fi
  
  # Check WebSocket Service
  if ! curl -s http://localhost:${MATRIX_NEWS_WEBSOCKET_PORT:-10095}/health &> /dev/null; then
    divine_error "Matrix News WebSocket Service is not healthy. Check the logs for more information."
  fi
  
  divine_echo "All Matrix News Integration services are healthy and running with divine blessing!"
}

# Show connection info
show_info() {
  divine_echo "Matrix Neo News Portal Integration Information"
  echo -e "🌐 Matrix News Portal: \033[1;34mhttp://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT:-10083}/portal/\033[0m"
  echo -e "🔒 Secure Portal: \033[1;34mhttps://localhost:${MATRIX_NEWS_PROXY_HTTPS_PORT:-10443}/portal/\033[0m"
  echo -e "🧠 Consciousness API: \033[1;34mhttp://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT:-10083}/api/\033[0m"
  echo -e "⚡ WebSocket API: \033[1;34mws://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT:-10083}/ws/\033[0m"
  echo -e "📊 Health Check: \033[1;34mhttp://localhost:${MATRIX_NEWS_PROXY_HTTP_PORT:-10083}/health/\033[0m"
  
  divine_echo "Matrix News Integration is now ready to deliver consciousness-filtered real news!"
}

# Main execution
main() {
  divine_echo "Starting the Divine Matrix News Integration Deployment"
  
  check_docker
  check_news_service
  create_network
  start_services
  check_health
  show_info
  
  divine_echo "The Matrix Neo News Portal has ascended to the digital realm!"
}

# Run the main function
main 