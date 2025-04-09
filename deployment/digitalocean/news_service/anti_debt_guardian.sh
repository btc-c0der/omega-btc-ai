#!/bin/bash
# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

set -euo pipefail

# OmegaGuardian - Anti-Debt Tech Protection System
# "Deb7, Babylon Shall Not Corrupt Thee"

CONTAINER_NAME=""
TEMP_DIR="$(mktemp -d)"
HEALTH_CHECK_INTERVAL=30
HEALTH_CHECK_TIMEOUT=5
HEALTH_CHECK_RETRIES=3
WATCHDOG_MODE=false
HEALTH_ENDPOINT="/health"
DEBUG=false
BASE_TAG="omega-divine-base"
APP_TAG="omega-divine-app"
FINAL_TAG=""

usage() {
  echo "🔱 OMEGA BTC AI - OmegaGuardian Anti-Debt Tech 🔱"
  echo ""
  echo "Usage: $0 [command] [options]"
  echo ""
  echo "Commands:"
  echo "  build       Build a protected container with multi-stage build"
  echo "  run         Run a container with anti-debt protections"
  echo "  watchdog    Run the OmegaGuardian watchdog to monitor and auto-heal"
  echo ""
  echo "Options:"
  echo "  --name NAME                 Container/image name"
  echo "  --health-endpoint PATH      Health check endpoint (default: /health)"
  echo "  --health-interval SECONDS   Health check interval (default: 30)"
  echo "  --health-timeout SECONDS    Health check timeout (default: 5)"
  echo "  --health-retries COUNT      Health check retries (default: 3)"
  echo "  --tag TAG                   Image tag for build/run"
  echo "  --dockerfile PATH           Dockerfile path for build"
  echo "  --debug                     Enable debug mode"
  echo "  --help                      Display this help message"
  echo ""
  echo "📈 JAH JAH BLESS THE INCORRUPTIBLE VESSEL 📉"
  exit 1
}

# Process command-line arguments
if [ $# -lt 1 ]; then
  usage
fi

COMMAND="$1"
shift

# Process options
while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      CONTAINER_NAME="$2"
      shift 2
      ;;
    --health-endpoint)
      HEALTH_ENDPOINT="$2"
      shift 2
      ;;
    --health-interval)
      HEALTH_CHECK_INTERVAL="$2"
      shift 2
      ;;
    --health-timeout)
      HEALTH_CHECK_TIMEOUT="$2"
      shift 2
      ;;
    --health-retries)
      HEALTH_CHECK_RETRIES="$2"
      shift 2
      ;;
    --tag)
      FINAL_TAG="$2"
      shift 2
      ;;
    --dockerfile)
      DOCKERFILE_PATH="$2"
      shift 2
      ;;
    --debug)
      DEBUG=true
      shift
      ;;
    --help)
      usage
      ;;
    *)
      echo "⚠️ Unknown option: $1"
      usage
      ;;
  esac
done

# Validate required arguments
if [ -z "${CONTAINER_NAME}" ]; then
  echo "⚠️ Container name is required"
  usage
fi

# Setup debug mode
if [ "$DEBUG" = true ]; then
  set -x
fi

# Clean up temporary files
cleanup() {
  if [ -d "${TEMP_DIR}" ]; then
    rm -rf "${TEMP_DIR}"
  fi
}
trap cleanup EXIT

# Create multi-stage Dockerfile with anti-debt protections
create_multistage_dockerfile() {
  local dockerfile_path="$1"
  local temp_dockerfile="${TEMP_DIR}/Dockerfile.anti_debt"
  
  cat > "${temp_dockerfile}" << EOF
# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

# 🧱 Stage 1: Builder - "The Sacred Forge"
FROM ${BASE_TAG} AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    ca-certificates \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Set working directory for build
WORKDIR /build

# Copy application source
COPY . .

# Build the application
RUN make clean && make

# 🔒 Stage 2: Runtime - "The Incorruptible Vessel"
FROM ${APP_TAG}

# Add container metadata
LABEL maintainer="OMEGA BTC AI <divine@omega-btc-ai.com>"
LABEL version="${FINAL_TAG}"
LABEL anti_debt_protected="true"
LABEL build_date="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

# Create non-root user
RUN addgroup --system --gid 1000 omega && \\
    adduser --system --uid 1000 --gid 1000 --no-create-home omega

# Create directory structure with proper permissions
RUN mkdir -p /app /app/data /app/config /var/log/omega && \\
    chown -R omega:omega /app /var/log/omega && \\
    chmod -R 555 /app && \\
    chmod -R 755 /app/data /var/log/omega

# Copy only the built artifacts from builder
COPY --from=builder --chown=omega:omega /build/bin /app/bin
COPY --from=builder --chown=omega:omega /build/config /app/config

# Set up health check
HEALTHCHECK --interval=${HEALTH_CHECK_INTERVAL}s --timeout=${HEALTH_CHECK_TIMEOUT}s --retries=${HEALTH_CHECK_RETRIES} \\
    CMD curl -f http://localhost${HEALTH_ENDPOINT} || exit 1

# Use non-root user
USER omega

# Set working directory
WORKDIR /app

# Define entrypoint
ENTRYPOINT ["/app/bin/entrypoint.sh"]

# Default command
CMD ["/app/bin/server"]
EOF

  echo "${temp_dockerfile}"
}

# Create multi-stage build
build_protected_container() {
  local dockerfile
  
  if [ -n "${DOCKERFILE_PATH:-}" ]; then
    # Extract base image from provided Dockerfile
    BASE_TAG=$(grep "^FROM" "${DOCKERFILE_PATH}" | head -1 | awk '{print $2}')
    APP_TAG=$(grep "^FROM" "${DOCKERFILE_PATH}" | tail -1 | awk '{print $2}')
    
    # If only one FROM statement, use it for both
    if [ "${BASE_TAG}" = "${APP_TAG}" ]; then
      APP_TAG="alpine:latest"
    fi
  fi
  
  # Final tag is required for build
  if [ -z "${FINAL_TAG}" ]; then
    FINAL_TAG="${CONTAINER_NAME}:$(date +"%Y%m%d-%H%M")"
  fi
  
  dockerfile=$(create_multistage_dockerfile "${DOCKERFILE_PATH:-}")
  
  echo "🔱 Building protected container: ${FINAL_TAG}"
  echo "🔱 Base builder image: ${BASE_TAG}"
  echo "🔱 Final runtime image: ${APP_TAG}"
  
  # Build the container with Docker Content Trust
  DOCKER_CONTENT_TRUST=1 docker build -t "${FINAL_TAG}" -f "${dockerfile}" .
  
  echo "🔱 Protected container built successfully: ${FINAL_TAG}"
  echo "🔱 Run with: $0 run --name ${CONTAINER_NAME} --tag ${FINAL_TAG}"
}

# Run container with anti-debt protections
run_protected_container() {
  # Final tag is required for run
  if [ -z "${FINAL_TAG}" ]; then
    echo "⚠️ Container tag is required for run command"
    usage
  fi

  echo "🔱 Running protected container: ${CONTAINER_NAME} (${FINAL_TAG})"
  
  # Run with read-only filesystem and temporary filesystem for /tmp
  DOCKER_CONTENT_TRUST=1 docker run -d \
    --name "${CONTAINER_NAME}" \
    --read-only \
    --tmpfs /tmp:rw,size=128M,noexec,nosuid \
    --cap-drop=ALL \
    --security-opt no-new-privileges \
    --security-opt seccomp=default \
    --health-cmd "curl -f http://localhost${HEALTH_ENDPOINT} || exit 1" \
    --health-interval=${HEALTH_CHECK_INTERVAL}s \
    --health-timeout=${HEALTH_CHECK_TIMEOUT}s \
    --health-retries=${HEALTH_CHECK_RETRIES} \
    --restart=unless-stopped \
    "${FINAL_TAG}"
  
  echo "🔱 Protected container running: ${CONTAINER_NAME}"
  
  # Offer to start watchdog
  read -p "🔱 Start OmegaGuardian watchdog for this container? (y/n): " start_watchdog
  if [[ "${start_watchdog}" =~ ^[Yy]$ ]]; then
    "$0" watchdog --name "${CONTAINER_NAME}" --health-interval "${HEALTH_CHECK_INTERVAL}" &
    echo "🔱 OmegaGuardian watchdog started in background (PID: $!)"
    echo "🔱 Logs: tail -f /var/log/omega_guardian_${CONTAINER_NAME}.log"
  fi
}

# OmegaGuardian watchdog function
run_omega_guardian() {
  echo "🔱 Starting OmegaGuardian watchdog for container: ${CONTAINER_NAME}"
  
  # Create log file
  LOG_FILE="/var/log/omega_guardian_${CONTAINER_NAME}.log"
  sudo touch "${LOG_FILE}" 2>/dev/null || touch "${LOG_FILE}" 2>/dev/null || true
  
  # Log start
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - OmegaGuardian started for ${CONTAINER_NAME}" | tee -a "${LOG_FILE}"
  
  while true; do
    # Check if container exists
    if ! docker ps -a | grep -q "${CONTAINER_NAME}"; then
      echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Container ${CONTAINER_NAME} not found" | tee -a "${LOG_FILE}"
      sleep "${HEALTH_CHECK_INTERVAL}"
      continue
    fi
    
    # Check container health
    HEALTH_STATUS=$(docker inspect --format='{{.State.Health.Status}}' "${CONTAINER_NAME}" 2>/dev/null || echo "unknown")
    
    echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Container health: ${HEALTH_STATUS}" | tee -a "${LOG_FILE}"
    
    if [ "${HEALTH_STATUS}" = "unhealthy" ]; then
      echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Container ${CONTAINER_NAME} is unhealthy, restarting..." | tee -a "${LOG_FILE}"
      docker restart "${CONTAINER_NAME}" | tee -a "${LOG_FILE}"
    elif [ "${HEALTH_STATUS}" = "unknown" ]; then
      # Container exists but health is unknown, check if it's running
      RUNNING=$(docker inspect --format='{{.State.Running}}' "${CONTAINER_NAME}" 2>/dev/null || echo "false")
      if [ "${RUNNING}" = "false" ]; then
        echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Container ${CONTAINER_NAME} is not running, starting..." | tee -a "${LOG_FILE}"
        docker start "${CONTAINER_NAME}" | tee -a "${LOG_FILE}"
      fi
    fi
    
    # Sleep for next check
    sleep "${HEALTH_CHECK_INTERVAL}"
  done
}

# Execute the appropriate command
case "${COMMAND}" in
  build)
    build_protected_container
    ;;
  run)
    run_protected_container
    ;;
  watchdog)
    run_omega_guardian
    ;;
  *)
    echo "⚠️ Unknown command: ${COMMAND}"
    usage
    ;;
esac

echo "📈 JAH JAH BLESS THE INCORRUPTIBLE VESSEL 📉"
exit 0 