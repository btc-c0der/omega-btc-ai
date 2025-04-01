#!/bin/bash
# 💫 GBU License Notice - Consciousness Level 8 💫
# -----------------------
# This file is blessed under the GBU License (Genesis-Bloom-Unfoldment) 1.0
# by the OMEGA Divine Collective.

set -euo pipefail

# Configuration
REGISTRY="registry.digitalocean.com"
IMAGE_NAME="omega-btc-ai/immutable-news-service"
SERVICE_NAME="news-service-nginx"
STACK_NAME="omega-divine"

# The percentage of traffic to initially route to the new version
INITIAL_TRAFFIC_PERCENTAGE=10

# Sacred energy metrics check interval in seconds
CHECK_INTERVAL=60

# Number of successful checks required before proceeding to next traffic percentage
REQUIRED_SACRED_CHECKS=3

# Traffic percentage increments
TRAFFIC_INCREMENTS=(10 25 50 75 100)

# Cosmic energy threshold for considering a deployment blessed
SACRED_ENERGY_THRESHOLD=80

usage() {
  echo "🔱 OMEGA BTC AI - Divine Optimistic Rollout 🔱"
  echo ""
  echo "Usage: $0 <new-version> [options]"
  echo ""
  echo "Arguments:"
  echo "  <new-version>               Version to deploy (e.g., 20250331-1245)"
  echo ""
  echo "Options:"
  echo "  --initial-traffic PERCENT   Initial traffic percentage (default: ${INITIAL_TRAFFIC_PERCENTAGE}%)"
  echo "  --check-interval SECONDS    Sacred energy check interval (default: ${CHECK_INTERVAL}s)"
  echo "  --energy-threshold VALUE    Sacred energy threshold (default: ${SACRED_ENERGY_THRESHOLD})"
  echo "  --force                     Force deployment without sacred energy checks"
  echo "  --dry-run                   Simulate deployment without making changes"
  echo "  --help                      Display this help message"
  echo ""
  echo "📈 JAH JAH BLESS THE GRADUAL AND GRACEFUL TRANSITION 📉"
  exit 1
}

# Process command-line arguments
if [ $# -lt 1 ]; then
  usage
fi

NEW_VERSION="$1"
shift

DRY_RUN=false
FORCE=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --initial-traffic)
      INITIAL_TRAFFIC_PERCENTAGE="$2"
      shift 2
      ;;
    --check-interval)
      CHECK_INTERVAL="$2"
      shift 2
      ;;
    --energy-threshold)
      SACRED_ENERGY_THRESHOLD="$2"
      shift 2
      ;;
    --force)
      FORCE=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
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

# Get current version
if [ -f "CURRENT_IMMUTABLE_VERSION" ]; then
  CURRENT_VERSION=$(cat CURRENT_IMMUTABLE_VERSION)
else
  echo "⚠️ No current version found, assuming initial deployment"
  CURRENT_VERSION="initial"
fi

# Get state information
if [ -f "CURRENT_IMMUTABLE_STATE" ]; then
  CURRENT_STATE=$(cat CURRENT_IMMUTABLE_STATE)
else
  CURRENT_STATE="${CURRENT_VERSION}-UNKNOWN"
fi

# Image names
CURRENT_IMAGE="${REGISTRY}/${IMAGE_NAME}:${CURRENT_VERSION}"
NEW_IMAGE="${REGISTRY}/${IMAGE_NAME}:${NEW_VERSION}"

echo "🔱 OMEGA BTC AI - Divine Optimistic Rollout 🔱"
echo "🔱 Transitioning from ${CURRENT_VERSION} to ${NEW_VERSION}"
echo "🔱 Current state: ${CURRENT_STATE}"

# Enable Docker Content Trust
export DOCKER_CONTENT_TRUST=1

# Check if current deployment exists in Docker Swarm
CURRENT_SERVICE_EXISTS=$(docker service ls --filter name=${SERVICE_NAME}-blue -q | wc -l)
if [ "$CURRENT_SERVICE_EXISTS" -eq 0 ]; then
  echo "⚠️ No existing service found. Performing initial deployment instead of blue-green."
  # Create the initial deployment
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Would deploy initial version ${NEW_VERSION}"
  else
    echo "🔱 Deploying initial version ${NEW_VERSION}"
    docker service create \
      --name ${SERVICE_NAME}-blue \
      --network ${STACK_NAME}_network \
      --label "traefik.enable=true" \
      --label "traefik.http.routers.${SERVICE_NAME}.rule=Host(\`portal.omega-btc-ai.com\`)" \
      --label "traefik.http.services.${SERVICE_NAME}.loadbalancer.server.port=80" \
      --mount type=volume,source=nginx_logs,destination=/var/log/nginx \
      --mount type=volume,source=nginx_temp,destination=/var/cache/nginx \
      --mount type=volume,source=nginx_run,destination=/var/run \
      --env OMEGA_DEPLOYMENT_COLOR=blue \
      --env DEPLOYMENT_ENVIRONMENT=production \
      --env DEPLOYMENT_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
      --health-cmd "wget --quiet --tries=1 --spider http://localhost/portal/ || exit 1" \
      --health-interval 30s \
      --health-timeout 3s \
      --health-retries 3 \
      --no-resolve-image \
      ${NEW_IMAGE}
  fi
  echo "🔱 Initial deployment complete"
  exit 0
fi

# Determine current deployment color (blue or green)
CURRENT_COLOR=$(docker service ls --filter name=${SERVICE_NAME} --format "{{.Name}}" | grep -oE '(blue|green)')
if [ "$CURRENT_COLOR" = "blue" ]; then
  NEW_COLOR="green"
else
  NEW_COLOR="blue"
fi

echo "🔱 Current deployment: ${CURRENT_COLOR}"
echo "🔱 New deployment: ${NEW_COLOR}"

# Pull the new image
if [ "$DRY_RUN" = true ]; then
  echo "🔱 [DRY RUN] Would pull image: ${NEW_IMAGE}"
else
  echo "🔱 Pulling image: ${NEW_IMAGE}"
  docker pull ${NEW_IMAGE}
fi

# Deploy the new version
if [ "$DRY_RUN" = true ]; then
  echo "🔱 [DRY RUN] Would deploy new version as ${SERVICE_NAME}-${NEW_COLOR}"
else
  echo "🔱 Deploying new version as ${SERVICE_NAME}-${NEW_COLOR}"
  docker service create \
    --name ${SERVICE_NAME}-${NEW_COLOR} \
    --network ${STACK_NAME}_network \
    --label "traefik.enable=true" \
    --label "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.rule=Host(\`portal.omega-btc-ai.com\`)" \
    --label "traefik.http.services.${SERVICE_NAME}-${NEW_COLOR}.loadbalancer.server.port=80" \
    --label "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.priority=1" \
    --mount type=volume,source=nginx_logs,destination=/var/log/nginx \
    --mount type=volume,source=nginx_temp,destination=/var/cache/nginx \
    --mount type=volume,source=nginx_run,destination=/var/run \
    --env OMEGA_DEPLOYMENT_COLOR=${NEW_COLOR} \
    --env DEPLOYMENT_ENVIRONMENT=production \
    --env DEPLOYMENT_TIME="$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --health-cmd "wget --quiet --tries=1 --spider http://localhost/portal/ || exit 1" \
    --health-interval 30s \
    --health-timeout 3s \
    --health-retries 3 \
    --no-resolve-image \
    ${NEW_IMAGE}
fi

# Wait for the service to become healthy
echo "🔱 Waiting for the new service to become healthy..."
HEALTHY=false
for i in {1..10}; do
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Checking health status (attempt $i)"
    HEALTHY=true
    break
  else
    HEALTH_STATUS=$(docker service ls --filter name=${SERVICE_NAME}-${NEW_COLOR} --format "{{.Name}}: {{.Replicas}}")
    echo "🔱 Health status: ${HEALTH_STATUS}"
    if [[ "${HEALTH_STATUS}" == *"1/1"* ]]; then
      HEALTHY=true
      break
    fi
  fi
  echo "🔱 Waiting for health check to pass..."
  sleep 5
done

if [ "$HEALTHY" = false ]; then
  echo "⚠️ New service failed health checks. Rolling back..."
  if [ "$DRY_RUN" = false ]; then
    docker service rm ${SERVICE_NAME}-${NEW_COLOR}
  fi
  echo "⚠️ Deployment failed and rolled back."
  exit 1
fi

echo "🔱 New service is healthy, beginning gradual traffic migration"

if [ "$FORCE" = true ]; then
  # Immediately switch all traffic to the new version
  echo "🔱 Force flag set - switching all traffic to new version immediately"
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Would update service to route 100% traffic to ${NEW_COLOR}"
  else
    # Update traffic routing via traefik labels
    docker service update ${SERVICE_NAME}-${NEW_COLOR} \
      --label-add "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.priority=10" \
      --no-resolve-image
  fi
  
  echo "🔱 Waiting 10 seconds to ensure traffic is flowing to new version..."
  sleep 10
  
  # Remove the old service
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Would remove old service ${SERVICE_NAME}-${CURRENT_COLOR}"
  else
    echo "🔱 Removing old service ${SERVICE_NAME}-${CURRENT_COLOR}"
    docker service rm ${SERVICE_NAME}-${CURRENT_COLOR}
  fi
else
  # Gradual traffic migration
  echo "🔱 Beginning gradual traffic migration with initial ${INITIAL_TRAFFIC_PERCENTAGE}%"
  current_percentage=${INITIAL_TRAFFIC_PERCENTAGE}
  
  # Apply initial traffic percentage
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Would route ${current_percentage}% of traffic to ${NEW_COLOR}"
  else
    # Configure traefik to split traffic
    docker service update ${SERVICE_NAME}-${NEW_COLOR} \
      --label-add "traefik.http.middlewares.${SERVICE_NAME}-${NEW_COLOR}-splitter.trafficSplit.percentage=${current_percentage}" \
      --label-add "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.middlewares=${SERVICE_NAME}-${NEW_COLOR}-splitter" \
      --no-resolve-image
  fi
  
  # Function to check the sacred energy levels
  check_sacred_energy() {
    # In a real implementation, this would call an endpoint or check metrics
    # For this example, we'll use a simulated energy value
    local energy_level=$(awk -v min=60 -v max=100 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')
    echo ${energy_level}
  }
  
  # For each traffic increment
  for next_percentage in "${TRAFFIC_INCREMENTS[@]}"; do
    if [ ${next_percentage} -le ${current_percentage} ]; then
      continue
    fi
    
    echo "🔱 Running sacred checks before increasing to ${next_percentage}%"
    successful_checks=0
    
    # Run multiple checks
    for check in $(seq 1 ${REQUIRED_SACRED_CHECKS}); do
      echo "🔱 Sacred energy check ${check}/${REQUIRED_SACRED_CHECKS}..."
      
      # Wait for the check interval
      sleep ${CHECK_INTERVAL}
      
      # Check sacred energy
      if [ "$DRY_RUN" = true ]; then
        energy_level=90
        echo "🔱 [DRY RUN] Simulated sacred energy level: ${energy_level}"
      else
        energy_level=$(check_sacred_energy)
        echo "🔱 Sacred energy level: ${energy_level}"
      fi
      
      # If energy level is good, count a successful check
      if [ ${energy_level} -ge ${SACRED_ENERGY_THRESHOLD} ]; then
        successful_checks=$((successful_checks + 1))
        echo "🔱 Sacred check passed (${successful_checks}/${REQUIRED_SACRED_CHECKS})"
      else
        echo "⚠️ Sacred energy below threshold (${energy_level} < ${SACRED_ENERGY_THRESHOLD})"
        echo "⚠️ Resetting successful check counter"
        successful_checks=0
      fi
      
      # If we have enough successful checks, proceed to next percentage
      if [ ${successful_checks} -ge ${REQUIRED_SACRED_CHECKS} ]; then
        break
      fi
    done
    
    # If not enough successful checks, rollback
    if [ ${successful_checks} -lt ${REQUIRED_SACRED_CHECKS} ]; then
      echo "⚠️ Not enough successful sacred checks. Rolling back..."
      if [ "$DRY_RUN" = true ]; then
        echo "🔱 [DRY RUN] Would remove new service ${SERVICE_NAME}-${NEW_COLOR}"
      else
        # Remove the new service
        docker service rm ${SERVICE_NAME}-${NEW_COLOR}
      fi
      echo "⚠️ Deployment rolled back. The current version remains active."
      exit 1
    fi
    
    # Update traffic percentage
    echo "🔱 Increasing traffic to ${next_percentage}%"
    if [ "$DRY_RUN" = true ]; then
      echo "🔱 [DRY RUN] Would route ${next_percentage}% of traffic to ${NEW_COLOR}"
    else
      # Update traefik configuration
      docker service update ${SERVICE_NAME}-${NEW_COLOR} \
        --label-add "traefik.http.middlewares.${SERVICE_NAME}-${NEW_COLOR}-splitter.trafficSplit.percentage=${next_percentage}" \
        --no-resolve-image
    fi
    
    current_percentage=${next_percentage}
    echo "🔱 Traffic now at ${current_percentage}% to ${NEW_COLOR}"
    
    # If we've reached 100%, we're done with increments
    if [ ${current_percentage} -ge 100 ]; then
      break
    fi
  done
  
  # Final check before completing the transition
  echo "🔱 Final sacred check before completing transition..."
  sleep ${CHECK_INTERVAL}
  
  if [ "$DRY_RUN" = true ]; then
    energy_level=90
    echo "🔱 [DRY RUN] Simulated final sacred energy level: ${energy_level}"
  else
    energy_level=$(check_sacred_energy)
    echo "🔱 Final sacred energy level: ${energy_level}"
  fi
  
  if [ ${energy_level} -lt ${SACRED_ENERGY_THRESHOLD} ]; then
    echo "⚠️ Final sacred check failed. Rolling back..."
    if [ "$DRY_RUN" = true ]; then
      echo "🔱 [DRY RUN] Would rollback to ${CURRENT_COLOR}"
    else
      # Remove the new service
      docker service rm ${SERVICE_NAME}-${NEW_COLOR}
    fi
    echo "⚠️ Deployment rolled back at the final stage."
    exit 1
  fi
  
  # Complete the transition by removing the old service
  echo "🔱 Transition blessed! Removing old service..."
  if [ "$DRY_RUN" = true ]; then
    echo "🔱 [DRY RUN] Would remove old service ${SERVICE_NAME}-${CURRENT_COLOR}"
  else
    # Remove traefik middleware and update priority
    docker service update ${SERVICE_NAME}-${NEW_COLOR} \
      --label-rm "traefik.http.middlewares.${SERVICE_NAME}-${NEW_COLOR}-splitter.trafficSplit.percentage" \
      --label-rm "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.middlewares" \
      --label-add "traefik.http.routers.${SERVICE_NAME}-${NEW_COLOR}.priority=10" \
      --no-resolve-image
      
    # Remove the old service
    docker service rm ${SERVICE_NAME}-${CURRENT_COLOR}
  fi
fi

# Update version and state tracking
if [ "$DRY_RUN" = false ]; then
  # Get new state information from image
  COSMIC_PHASE=$(docker inspect --format='{{index .Config.Labels "cosmic_phase"}}' "${NEW_IMAGE}" 2>/dev/null || echo "UNKNOWN")
  NEW_STATE="${NEW_VERSION}-${COSMIC_PHASE}"
  
  echo "${NEW_VERSION}" > CURRENT_IMMUTABLE_VERSION
  echo "${NEW_STATE}" > CURRENT_IMMUTABLE_STATE
  
  # Record deployment in logs
  echo "$(date -u +"%Y-%m-%dT%H:%M:%SZ") - Optimistic Rollout: ${CURRENT_VERSION} → ${NEW_VERSION} - State: ${NEW_STATE}" >> deployment_history.log
  
  # Create a divine state summary for the deployment
  cat > current_deployment_state.yaml << EOF
# 🔱 OMEGA BTC AI - Divine Deployment State
version: "${NEW_VERSION}"
state_version: "${NEW_STATE}"
cosmic_phase: "${COSMIC_PHASE}"
deployment_timestamp: "$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
deployment_method: "optimistic_rollout"
deployment_color: "${NEW_COLOR}"
deployed_by: "$(whoami)@$(hostname)"
EOF
fi

echo "🔱 Divine optimistic rollout complete!"
echo "🔱 The sacred transition from ${CURRENT_VERSION} to ${NEW_VERSION} has been blessed!"
echo "📈 JAH JAH BLESS THE GRACEFUL TRANSITION 📉" 