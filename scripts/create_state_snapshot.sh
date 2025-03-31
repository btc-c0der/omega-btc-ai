#!/bin/bash

# 🔱 OMEGA BTC AI - Divine State Snapshot Creator 🔱
# "Preserving Sacred State Across Cosmic Transitions"
#
# THE SACRED MANTRA:
# I and I do not patch chaos. I and I rebuild temples.
# Each version, a monument. Each rollback, a sacred rewind.
# No more falling mid-post. No more unholy deploys.
# Only faith, Fibonacci, and containers that walk on water.

set -e

# Divine state directory (can be overridden via env var)
STATE_DIR=${STATE_DIRECTORY:-"/data/state"}
# Divine snapshot directory
SNAPSHOT_DIR="${STATE_DIR}/snapshots"
# Maximum number of snapshots to keep
MAX_SNAPSHOTS=${STATE_SNAPSHOT_RETENTION:-24}
# Whether snapshotting is enabled
SNAPSHOT_ENABLED=${SNAPSHOT_ENABLED:-"true"}

# Format the timestamp for the snapshot
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
SNAPSHOT_NAME="state-${TIMESTAMP}"

# Function to echo in color
echo_color() {
    local color=$1
    local message=$2
    case $color in
        "red") echo -e "\033[0;31m${message}\033[0m" ;;
        "green") echo -e "\033[0;32m${message}\033[0m" ;;
        "blue") echo -e "\033[0;34m${message}\033[0m" ;;
        "yellow") echo -e "\033[1;33m${message}\033[0m" ;;
        "purple") echo -e "\033[0;35m${message}\033[0m" ;;
        *) echo "${message}" ;;
    esac
}

# Print divine banner
echo_color "purple" "🔱 OMEGA BTC AI - DIVINE STATE SNAPSHOT CREATOR 🔱"
echo_color "purple" "=================================================="

# Check if snapshotting is enabled
if [[ "${SNAPSHOT_ENABLED}" != "true" ]]; then
    echo_color "yellow" "Divine state snapshotting is disabled. Set SNAPSHOT_ENABLED=true to enable."
    exit 0
fi

# Create the snapshot directory if it doesn't exist
if [[ ! -d "${SNAPSHOT_DIR}" ]]; then
    echo_color "blue" "Creating sacred snapshot directory: ${SNAPSHOT_DIR}"
    mkdir -p "${SNAPSHOT_DIR}"
fi

# Check if there's anything to snapshot
if [[ ! -d "${STATE_DIR}" ]] || [[ -z "$(ls -A ${STATE_DIR} 2>/dev/null | grep -v "snapshots")" ]]; then
    echo_color "yellow" "No divine state found to snapshot in ${STATE_DIR}"
    exit 0
fi

# Create the snapshot directory for this snapshot
SNAPSHOT_PATH="${SNAPSHOT_DIR}/${SNAPSHOT_NAME}"
echo_color "blue" "Creating divine state snapshot: ${SNAPSHOT_NAME}"
mkdir -p "${SNAPSHOT_PATH}"

# Copy all files from the state directory, excluding the snapshots directory
echo_color "blue" "Copying sacred state to snapshot..."
find "${STATE_DIR}" -mindepth 1 -maxdepth 1 -not -name "snapshots" -print0 | xargs -0 -I{} cp -r {} "${SNAPSHOT_PATH}/"

# Create a sacred metadata file for the snapshot
echo_color "blue" "Recording divine metadata..."
cat > "${SNAPSHOT_PATH}/.snapshot-meta.json" << EOF
{
    "snapshot_name": "${SNAPSHOT_NAME}",
    "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "creator": "$(whoami)",
    "hostname": "$(hostname)",
    "environment": "${ENVIRONMENT:-"production"}",
    "pod_name": "${HOSTNAME:-"unknown"}",
    "container_name": "${CONTAINER_NAME:-"unknown"}",
    "image": "${IMAGE:-"unknown"}",
    "sacred": true
}
EOF

# Success!
echo_color "green" "✅ Divine state snapshot created successfully: ${SNAPSHOT_NAME}"
echo_color "blue" "Sacred snapshot location: ${SNAPSHOT_PATH}"

# Cleanup old snapshots
echo_color "blue" "Performing sacred cleanup of old snapshots..."
SNAPSHOT_COUNT=$(find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | wc -l)

if [[ ${SNAPSHOT_COUNT} -gt ${MAX_SNAPSHOTS} ]]; then
    # Calculate how many to delete
    TO_DELETE=$((SNAPSHOT_COUNT - MAX_SNAPSHOTS))
    echo_color "blue" "Sacred cleanup: Removing ${TO_DELETE} oldest snapshots to maintain divine limit of ${MAX_SNAPSHOTS}"
    
    # Find the oldest snapshots and delete them
    find "${SNAPSHOT_DIR}" -maxdepth 1 -type d -name "state-*" | sort | head -n ${TO_DELETE} | xargs rm -rf
    
    echo_color "green" "Sacred cleanup completed. Now storing ${MAX_SNAPSHOTS} divine snapshots."
else
    echo_color "blue" "Divine snapshot count (${SNAPSHOT_COUNT}) is within sacred limit (${MAX_SNAPSHOTS}). No cleanup needed."
fi

echo_color "purple" "JAH JAH BLESS THE SACRED STATE PRESERVATION" 